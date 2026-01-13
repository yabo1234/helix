import type { Order, Product, PromoCode } from "../domain/models.js";

export type CreateUserInput = {
  email: string;
  passwordHash: string;
  role?: "ADMIN" | "CUSTOMER";
};

export type UserRecord = {
  id: string;
  email: string;
  passwordHash: string;
  role: "ADMIN" | "CUSTOMER";
};

export type CreateProductInput = Omit<
  Product,
  "assets" | "active" | "description" | "industry" | "metadata" | "stock"
> & {
  description?: string;
  active?: boolean;
  industry?: string | null;
  stock?: number | null;
  metadata?: Record<string, unknown> | null;
  assets?: Array<{ label: string; url: string; mimeType?: string | null }>;
};

export type UpdateProductInput = Partial<Omit<CreateProductInput, "id">> & {
  assets?: Array<{ label: string; url: string; mimeType?: string | null }>;
};

export type CreatePromoInput = Omit<
  PromoCode,
  "active" | "startsAt" | "endsAt" | "maxRedemptions" | "redemptionsCount"
> & {
  active?: boolean;
  startsAt?: Date | null;
  endsAt?: Date | null;
  maxRedemptions?: number | null;
};

export type CreateOrderInput = {
  userId?: string | null;
  email: string;
  currency: string;
  items: Array<{
    productId: string;
    quantity: number;
  }>;
  promoCode?: string | null;
  paymentProvider: string;
  checkoutSessionId?: string | null;
  paymentIntentId?: string | null;
};

export type Store = {
  // Users
  createUser(input: CreateUserInput): Promise<UserRecord>;
  findUserByEmail(email: string): Promise<UserRecord | null>;
  findUserById(id: string): Promise<UserRecord | null>;

  // Products
  createProduct(input: CreateProductInput): Promise<Product>;
  updateProduct(productId: string, input: UpdateProductInput): Promise<Product>;
  getProduct(productId: string): Promise<Product | null>;
  listProducts(params?: { activeOnly?: boolean }): Promise<Product[]>;
  deleteProduct(productId: string): Promise<void>;

  // Promos
  upsertPromo(input: CreatePromoInput): Promise<PromoCode>;
  getPromo(code: string): Promise<PromoCode | null>;

  // Orders
  createOrder(input: CreateOrderInput): Promise<Order>;
  getOrder(orderId: string): Promise<Order | null>;
  listOrders(params?: { email?: string; userId?: string }): Promise<Order[]>;
  updateOrderStatus(params: {
    orderId: string;
    status: "pending" | "paid" | "failed" | "refunded";
    checkoutSessionId?: string | null;
    paymentIntentId?: string | null;
  }): Promise<Order>;

  // Ownership checks for downloads
  userOwnsProduct(params: { userId: string; productId: string }): Promise<boolean>;
  getAsset(params: { assetId: string }): Promise<{
    id: string;
    productId: string;
    label: string;
    url: string;
    mimeType?: string | null;
  } | null>;

  // Leads / support escalation
  createLead(input: { name?: string | null; email: string; message: string; source?: string }): Promise<{
    id: string;
    email: string;
    createdAt: Date;
  }>;

  // GDPR deletion (best-effort: delete personal data we own)
  deleteUserData(params: { userId: string }): Promise<void>;
};

