import type { Prisma } from "@prisma/client";
import { prisma } from "../db/prisma.js";
import type { Order, Product, PromoCode } from "../domain/models.js";
import type {
  CreateOrderInput,
  CreateProductInput,
  CreatePromoInput,
  CreateUserInput,
  Store,
  UpdateProductInput,
  UserRecord
} from "./types.js";

function toProduct(p: Prisma.ProductGetPayload<{ include: { assets: true } }>): Product {
  return {
    id: p.id,
    title: p.title,
    description: p.description,
    type: p.type as any,
    industry: p.industry ?? null,
    currency: p.currency,
    priceCents: p.priceCents,
    stock: p.stock ?? null,
    active: p.active,
    metadata: (p.metadata ?? null) as any,
    assets: p.assets.map((a) => ({
      id: a.id,
      label: a.label,
      url: a.url,
      mimeType: a.mimeType ?? null
    }))
  };
}

function toPromo(p: Prisma.PromoCodeGetPayload<{}>): PromoCode {
  return {
    code: p.code,
    type: p.type as any,
    amount: p.amount,
    currency: p.currency ?? null,
    active: p.active,
    startsAt: p.startsAt ?? null,
    endsAt: p.endsAt ?? null,
    maxRedemptions: p.maxRedemptions ?? null,
    redemptionsCount: p.redemptionsCount
  };
}

function toOrder(
  o: Prisma.OrderGetPayload<{ include: { items: true } }>
): Order {
  return {
    id: o.id,
    userId: o.userId ?? null,
    email: o.email,
    status: o.status as any,
    currency: o.currency,
    subtotalCents: o.subtotalCents,
    discountCents: o.discountCents,
    totalCents: o.totalCents,
    promoCode: o.promoCode ?? null,
    paymentProvider: o.paymentProvider,
    checkoutSessionId: o.checkoutSessionId ?? null,
    paymentIntentId: o.paymentIntentId ?? null,
    items: o.items.map((it) => ({
      productId: it.productId,
      titleSnapshot: it.titleSnapshot,
      unitPriceCents: it.unitPriceCents,
      quantity: it.quantity
    }))
  };
}

export class PrismaStore implements Store {
  async createUser(input: CreateUserInput): Promise<UserRecord> {
    const u = await prisma.user.create({
      data: {
        email: input.email.toLowerCase(),
        passwordHash: input.passwordHash,
        role: input.role ?? "CUSTOMER"
      }
    });
    return { id: u.id, email: u.email, passwordHash: u.passwordHash, role: u.role as any };
  }

  async findUserByEmail(email: string): Promise<UserRecord | null> {
    const u = await prisma.user.findUnique({ where: { email: email.toLowerCase() } });
    if (!u) return null;
    return { id: u.id, email: u.email, passwordHash: u.passwordHash, role: u.role as any };
  }

  async findUserById(id: string): Promise<UserRecord | null> {
    const u = await prisma.user.findUnique({ where: { id } });
    if (!u) return null;
    return { id: u.id, email: u.email, passwordHash: u.passwordHash, role: u.role as any };
  }

  async createProduct(input: CreateProductInput): Promise<Product> {
    const p = await prisma.product.create({
      data: {
        id: input.id,
        title: input.title,
        description: input.description ?? "",
        type: input.type as any,
        industry: input.industry ?? null,
        currency: input.currency,
        priceCents: input.priceCents,
        stock: input.stock ?? null,
        active: input.active ?? true,
        metadata: (input.metadata ?? undefined) as any,
        assets: input.assets
          ? {
              create: input.assets.map((a) => ({
                label: a.label,
                url: a.url,
                mimeType: a.mimeType ?? null
              }))
            }
          : undefined
      },
      include: { assets: true }
    });
    return toProduct(p);
  }

  async updateProduct(productId: string, input: UpdateProductInput): Promise<Product> {
    const p = await prisma.product.update({
      where: { id: productId },
      data: {
        title: input.title,
        description: input.description,
        type: input.type as any,
        industry: input.industry,
        currency: input.currency,
        priceCents: input.priceCents,
        stock: input.stock as any,
        active: input.active,
        metadata: input.metadata as any,
        assets: input.assets
          ? {
              deleteMany: {},
              create: input.assets.map((a) => ({
                label: a.label,
                url: a.url,
                mimeType: a.mimeType ?? null
              }))
            }
          : undefined
      },
      include: { assets: true }
    });
    return toProduct(p);
  }

  async getProduct(productId: string): Promise<Product | null> {
    const p = await prisma.product.findUnique({
      where: { id: productId },
      include: { assets: true }
    });
    return p ? toProduct(p) : null;
  }

  async listProducts(params?: { activeOnly?: boolean }): Promise<Product[]> {
    const ps = await prisma.product.findMany({
      where: params?.activeOnly ? { active: true } : undefined,
      include: { assets: true },
      orderBy: { createdAt: "desc" }
    });
    return ps.map(toProduct);
  }

  async deleteProduct(productId: string): Promise<void> {
    await prisma.product.delete({ where: { id: productId } });
  }

  async upsertPromo(input: CreatePromoInput): Promise<PromoCode> {
    const p = await prisma.promoCode.upsert({
      where: { code: input.code.toUpperCase() },
      update: {
        type: input.type as any,
        amount: input.amount,
        currency: input.currency ?? null,
        active: input.active ?? true,
        startsAt: input.startsAt ?? null,
        endsAt: input.endsAt ?? null,
        maxRedemptions: input.maxRedemptions ?? null
      },
      create: {
        code: input.code.toUpperCase(),
        type: input.type as any,
        amount: input.amount,
        currency: input.currency ?? null,
        active: input.active ?? true,
        startsAt: input.startsAt ?? null,
        endsAt: input.endsAt ?? null,
        maxRedemptions: input.maxRedemptions ?? null
      }
    });
    return toPromo(p);
  }

  async getPromo(code: string): Promise<PromoCode | null> {
    const p = await prisma.promoCode.findUnique({ where: { code: code.toUpperCase() } });
    return p ? toPromo(p) : null;
  }

  async createOrder(input: CreateOrderInput): Promise<Order> {
    const products = await prisma.product.findMany({
      where: { id: { in: input.items.map((i) => i.productId) } }
    });
    const byId = new Map(products.map((p) => [p.id, p]));
    for (const it of input.items) {
      if (!byId.get(it.productId)) throw new Error("INVALID_PRODUCT");
    }

    const orderItems = input.items.map((it) => {
      const p = byId.get(it.productId)!;
      return {
        productId: p.id,
        titleSnapshot: p.title,
        unitPriceCents: p.priceCents,
        quantity: it.quantity
      };
    });
    const subtotalCents = orderItems.reduce((s, it) => s + it.unitPriceCents * it.quantity, 0);
    const promo = input.promoCode ? await this.getPromo(input.promoCode) : null;
    const discountCents = promo ? computeDiscount(subtotalCents, promo) : 0;
    const totalCents = Math.max(0, subtotalCents - discountCents);

    const o = await prisma.order.create({
      data: {
        userId: input.userId ?? null,
        email: input.email.toLowerCase(),
        status: "pending",
        currency: input.currency,
        subtotalCents,
        discountCents,
        totalCents,
        promoCode: promo?.code ?? null,
        paymentProvider: input.paymentProvider,
        checkoutSessionId: input.checkoutSessionId ?? null,
        paymentIntentId: input.paymentIntentId ?? null,
        items: { create: orderItems }
      },
      include: { items: true }
    });
    return toOrder(o);
  }

  async getOrder(orderId: string): Promise<Order | null> {
    const o = await prisma.order.findUnique({ where: { id: orderId }, include: { items: true } });
    return o ? toOrder(o) : null;
  }

  async listOrders(params?: { email?: string; userId?: string }): Promise<Order[]> {
    const os = await prisma.order.findMany({
      where: {
        email: params?.email ? params.email.toLowerCase() : undefined,
        userId: params?.userId
      },
      include: { items: true },
      orderBy: { createdAt: "desc" }
    });
    return os.map(toOrder);
  }

  async updateOrderStatus(params: {
    orderId: string;
    status: "pending" | "paid" | "failed" | "refunded";
    checkoutSessionId?: string | null;
    paymentIntentId?: string | null;
  }): Promise<Order> {
    const o = await prisma.order.update({
      where: { id: params.orderId },
      data: {
        status: params.status as any,
        checkoutSessionId: params.checkoutSessionId ?? undefined,
        paymentIntentId: params.paymentIntentId ?? undefined
      },
      include: { items: true }
    });
    return toOrder(o);
  }

  async userOwnsProduct(params: { userId: string; productId: string }): Promise<boolean> {
    const count = await prisma.order.count({
      where: {
        userId: params.userId,
        status: "paid",
        items: { some: { productId: params.productId } }
      }
    });
    return count > 0;
  }

  async getAsset(params: { assetId: string }) {
    const asset = await prisma.productAsset.findUnique({ where: { id: params.assetId } });
    if (!asset) return null;
    return {
      id: asset.id,
      productId: asset.productId,
      label: asset.label,
      url: asset.url,
      mimeType: asset.mimeType ?? null
    };
  }

  async createLead(input: { name?: string | null; email: string; message: string; source?: string }) {
    const lead = await prisma.lead.create({
      data: {
        name: input.name ?? null,
        email: input.email.toLowerCase(),
        message: input.message,
        source: input.source ?? "chat"
      }
    });
    return { id: lead.id, email: lead.email, createdAt: lead.createdAt };
  }

  async deleteUserData(params: { userId: string }): Promise<void> {
    // Best-effort removal. For a real system: export user data + remove PII from orders.
    await prisma.order.updateMany({
      where: { userId: params.userId },
      data: { email: "deleted@example.com", userId: null }
    });
    await prisma.user.delete({ where: { id: params.userId } });
  }
}

function computeDiscount(subtotalCents: number, promo: PromoCode) {
  if (!promo.active) return 0;
  const now = new Date();
  if (promo.startsAt && now < promo.startsAt) return 0;
  if (promo.endsAt && now > promo.endsAt) return 0;
  if (promo.maxRedemptions != null && promo.redemptionsCount >= promo.maxRedemptions) return 0;
  if (promo.type === "fixed") return Math.min(subtotalCents, promo.amount);
  return Math.min(subtotalCents, Math.round((subtotalCents * promo.amount) / 100));
}

