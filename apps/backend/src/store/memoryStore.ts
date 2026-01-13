import crypto from "crypto";
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

function uuid() {
  return crypto.randomUUID();
}

export class MemoryStore implements Store {
  private users = new Map<string, UserRecord>();
  private usersByEmail = new Map<string, string>();
  private products = new Map<string, Product>();
  private assets = new Map<
    string,
    { id: string; productId: string; label: string; url: string; mimeType?: string | null }
  >();
  private promos = new Map<string, PromoCode>();
  private orders = new Map<string, Order>();
  private leads = new Map<string, { id: string; name?: string | null; email: string; message: string; source: string; createdAt: Date }>();

  async createUser(input: CreateUserInput): Promise<UserRecord> {
    const id = uuid();
    const user: UserRecord = {
      id,
      email: input.email.toLowerCase(),
      passwordHash: input.passwordHash,
      role: input.role ?? "CUSTOMER"
    };
    if (this.usersByEmail.has(user.email)) throw new Error("EMAIL_EXISTS");
    this.users.set(id, user);
    this.usersByEmail.set(user.email, id);
    return user;
  }

  async findUserByEmail(email: string): Promise<UserRecord | null> {
    const id = this.usersByEmail.get(email.toLowerCase());
    if (!id) return null;
    return this.users.get(id) ?? null;
  }

  async findUserById(id: string): Promise<UserRecord | null> {
    return this.users.get(id) ?? null;
  }

  async createProduct(input: CreateProductInput): Promise<Product> {
    if (this.products.has(input.id)) throw new Error("PRODUCT_EXISTS");
    const assets = (input.assets ?? []).map((a) => ({
      id: uuid(),
      label: a.label,
      url: a.url,
      mimeType: a.mimeType ?? null
    }));
    const product: Product = {
      id: input.id,
      title: input.title,
      description: input.description ?? "",
      type: input.type,
      industry: input.industry ?? null,
      currency: input.currency,
      priceCents: input.priceCents,
      stock: input.stock ?? null,
      active: input.active ?? true,
      metadata: (input.metadata ?? null) as any,
      assets
    };
    this.products.set(product.id, product);
    for (const asset of assets) {
      this.assets.set(asset.id, { ...asset, productId: product.id });
    }
    return product;
  }

  async updateProduct(productId: string, input: UpdateProductInput): Promise<Product> {
    const existing = this.products.get(productId);
    if (!existing) throw new Error("NOT_FOUND");
    const next: Product = {
      ...existing,
      ...input,
      assets: existing.assets
    } as Product;
    if (input.assets) {
      // Replace assets (simple)
      for (const a of existing.assets) this.assets.delete(a.id);
      const assets = input.assets.map((a) => ({
        id: uuid(),
        label: a.label,
        url: a.url,
        mimeType: a.mimeType ?? null
      }));
      next.assets = assets as any;
      for (const a of assets) this.assets.set(a.id, { ...a, productId });
    }
    this.products.set(productId, next);
    return next;
  }

  async getProduct(productId: string): Promise<Product | null> {
    return this.products.get(productId) ?? null;
  }

  async listProducts(params?: { activeOnly?: boolean }): Promise<Product[]> {
    const all = [...this.products.values()];
    if (params?.activeOnly) return all.filter((p) => p.active);
    return all;
  }

  async deleteProduct(productId: string): Promise<void> {
    const p = this.products.get(productId);
    if (!p) return;
    for (const a of p.assets) this.assets.delete(a.id);
    this.products.delete(productId);
  }

  async upsertPromo(input: CreatePromoInput): Promise<PromoCode> {
    const promo: PromoCode = {
      code: input.code.toUpperCase(),
      type: input.type,
      amount: input.amount,
      currency: input.currency ?? null,
      active: input.active ?? true,
      startsAt: input.startsAt ?? null,
      endsAt: input.endsAt ?? null,
      maxRedemptions: input.maxRedemptions ?? null,
      redemptionsCount: this.promos.get(input.code.toUpperCase())?.redemptionsCount ?? 0
    };
    this.promos.set(promo.code, promo);
    return promo;
  }

  async getPromo(code: string): Promise<PromoCode | null> {
    return this.promos.get(code.toUpperCase()) ?? null;
  }

  async createOrder(input: CreateOrderInput): Promise<Order> {
    const items = input.items.map((i) => {
      const p = this.products.get(i.productId);
      if (!p) throw new Error("INVALID_PRODUCT");
      return {
        productId: p.id,
        titleSnapshot: p.title,
        unitPriceCents: p.priceCents,
        quantity: i.quantity
      };
    });
    const subtotalCents = items.reduce((sum, it) => sum + it.unitPriceCents * it.quantity, 0);
    const promo = input.promoCode ? await this.getPromo(input.promoCode) : null;
    const discountCents = promo ? this.computeDiscount(subtotalCents, promo) : 0;
    const totalCents = Math.max(0, subtotalCents - discountCents);
    const order: Order = {
      id: uuid(),
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
      items
    };
    this.orders.set(order.id, order);
    return order;
  }

  async getOrder(orderId: string): Promise<Order | null> {
    return this.orders.get(orderId) ?? null;
  }

  async listOrders(params?: { email?: string; userId?: string }): Promise<Order[]> {
    const all = [...this.orders.values()];
    return all.filter((o) => {
      if (params?.email && o.email !== params.email.toLowerCase()) return false;
      if (params?.userId && o.userId !== params.userId) return false;
      return true;
    });
  }

  async updateOrderStatus(params: {
    orderId: string;
    status: "pending" | "paid" | "failed" | "refunded";
    checkoutSessionId?: string | null;
    paymentIntentId?: string | null;
  }): Promise<Order> {
    const existing = this.orders.get(params.orderId);
    if (!existing) throw new Error("NOT_FOUND");
    const next: Order = {
      ...existing,
      status: params.status,
      checkoutSessionId: params.checkoutSessionId ?? existing.checkoutSessionId ?? null,
      paymentIntentId: params.paymentIntentId ?? existing.paymentIntentId ?? null
    };
    this.orders.set(params.orderId, next);
    return next;
  }

  async userOwnsProduct(params: { userId: string; productId: string }): Promise<boolean> {
    for (const o of this.orders.values()) {
      if (o.userId !== params.userId) continue;
      if (o.status !== "paid") continue;
      if (o.items.some((it) => it.productId === params.productId)) return true;
    }
    return false;
  }

  async getAsset(params: { assetId: string }) {
    return this.assets.get(params.assetId) ?? null;
  }

  async createLead(input: { name?: string | null; email: string; message: string; source?: string }) {
    const id = uuid();
    const rec = {
      id,
      name: input.name ?? null,
      email: input.email.toLowerCase(),
      message: input.message,
      source: input.source ?? "chat",
      createdAt: new Date()
    };
    this.leads.set(id, rec);
    return { id: rec.id, email: rec.email, createdAt: rec.createdAt };
  }

  async deleteUserData(params: { userId: string }): Promise<void> {
    const user = this.users.get(params.userId);
    if (!user) return;
    // delete orders + anonymize email
    for (const [id, o] of this.orders.entries()) {
      if (o.userId === params.userId) {
        this.orders.set(id, { ...o, email: "deleted@example.com" });
      }
    }
    this.users.delete(params.userId);
    this.usersByEmail.delete(user.email);
  }

  private computeDiscount(subtotalCents: number, promo: PromoCode) {
    if (!promo.active) return 0;
    const now = new Date();
    if (promo.startsAt && now < promo.startsAt) return 0;
    if (promo.endsAt && now > promo.endsAt) return 0;
    if (promo.maxRedemptions != null && promo.redemptionsCount >= promo.maxRedemptions) return 0;
    if (promo.type === "fixed") return Math.min(subtotalCents, promo.amount);
    // percent
    return Math.min(subtotalCents, Math.round((subtotalCents * promo.amount) / 100));
  }
}

