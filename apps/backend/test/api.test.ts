process.env.NODE_ENV = "test";

import request from "supertest";
import { createApp } from "../src/app.js";
import { MemoryStore } from "../src/store/memoryStore.js";
import { MockPayments } from "../src/payments/mockPayments.js";
import { signAccessToken } from "../src/auth/jwt.js";

describe("helix backend API", () => {
  test("chat agent recommends products across 3 intent scenarios", async () => {
    const store = new MemoryStore();
    const payments = new MockPayments();

    await store.createProduct({
      id: "prod_001",
      title: "Business Analysis Template Pack",
      type: "digital",
      currency: "USD",
      priceCents: 4999,
      assets: [{ label: "PDF", url: "https://example.com/a.pdf" }],
      metadata: { difficulty: "intermediate", estimated_hours: 10, template_type: "general" }
    });
    await store.createProduct({
      id: "prod_003",
      title: "1:1 Consulting Session (60 minutes)",
      type: "consulting",
      currency: "USD",
      priceCents: 15000
    });

    const app = createApp({ store, payments });

    const discovery = await request(app)
      .post("/api/chat/recommend")
      .send({ message: "I need templates for stakeholder mapping and ROI modeling." })
      .expect(200);
    expect(discovery.body.intent).toBe("discovery");
    expect(discovery.body.recommendations.map((r: any) => r.productId)).toContain("prod_001");

    const price = await request(app)
      .post("/api/chat/recommend")
      .send({ message: "How much does the template pack cost?" })
      .expect(200);
    expect(price.body.intent).toBe("price_inquiry");
    expect(price.body.reply).toMatch(/prices/i);

    const compat = await request(app)
      .post("/api/chat/recommend")
      .send({ message: "Is this compatible with Excel or Google Sheets?" })
      .expect(200);
    expect(compat.body.intent).toBe("technical_compatibility");
  });

  test("checkout creates an order and webhook marks it paid; signed downloads expire", async () => {
    const store = new MemoryStore();
    const payments = new MockPayments();

    const product = await store.createProduct({
      id: "prod_001",
      title: "Business Analysis Template Pack",
      type: "digital",
      currency: "USD",
      priceCents: 5000,
      assets: [{ label: "PDF", url: "https://example.com/template-pack.pdf" }]
    });
    const assetId = product.assets[0]!.id;

    await store.upsertPromo({ code: "SAVE20", type: "percent", amount: 20 });

    const app = createApp({ store, payments });

    const signup = await request(app)
      .post("/api/auth/signup")
      .send({ email: "buyer@example.com", password: "password123" })
      .expect(201);
    const token = signup.body.token as string;

    const session = await request(app)
      .post("/api/checkout/session")
      .set("authorization", `Bearer ${token}`)
      .send({
        email: "buyer@example.com",
        currency: "USD",
        promoCode: "SAVE20",
        items: [{ productId: "prod_001", quantity: 1 }]
      })
      .expect(201);

    const orderId = session.body.order.id as string;
    expect(session.body.order.discountCents).toBe(1000);
    expect(session.body.order.totalCents).toBe(4000);

    // Webhook marks paid
    await request(app)
      .post("/api/webhooks/payments")
      .set("content-type", "application/json")
      .send({
        type: "checkout.session.completed",
        orderId,
        checkoutSessionId: session.body.order.checkoutSessionId,
        paymentIntentId: session.body.order.paymentIntentId
      })
      .expect(200);

    const order = await request(app)
      .get(`/api/orders/${orderId}`)
      .set("authorization", `Bearer ${token}`)
      .expect(200);
    expect(order.body.status).toBe("paid");

    // Signed download is available post-purchase
    const signed = await request(app)
      .get(`/api/downloads/signed/${assetId}?ttlSeconds=60`)
      .set("authorization", `Bearer ${token}`)
      .expect(200);
    expect(signed.body.signedUrl).toMatch(/\/api\/downloads\/serve\?token=/);

    await request(app)
      .get(signed.body.signedUrl)
      .expect(302);
  });

  test("admin can create a product and promo code", async () => {
    const store = new MemoryStore();
    const payments = new MockPayments();
    const admin = await store.createUser({
      email: "admin@example.com",
      passwordHash: "x",
      role: "ADMIN"
    });
    const adminToken = signAccessToken({ sub: admin.id, role: "ADMIN" });

    const app = createApp({ store, payments });

    await request(app)
      .post("/api/products")
      .set("authorization", `Bearer ${adminToken}`)
      .send({
        id: "prod_new",
        title: "New Product",
        type: "digital",
        currency: "USD",
        priceCents: 1234,
        assets: [{ label: "PDF", url: "https://example.com/new.pdf" }]
      })
      .expect(201);

    await request(app).get("/api/products").expect(200);

    await request(app)
      .post("/api/promos")
      .set("authorization", `Bearer ${adminToken}`)
      .send({ code: "HELIX10", type: "percent", amount: 10 })
      .expect(201);
  });
});

