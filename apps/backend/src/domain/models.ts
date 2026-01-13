import { z } from "zod";

export const ProductTypeSchema = z.enum(["digital", "consulting"]);
export type ProductType = z.infer<typeof ProductTypeSchema>;

export const PromoTypeSchema = z.enum(["percent", "fixed"]);
export type PromoType = z.infer<typeof PromoTypeSchema>;

export const OrderStatusSchema = z.enum(["pending", "paid", "failed", "refunded"]);
export type OrderStatus = z.infer<typeof OrderStatusSchema>;

export const ProductMetadataSchema = z
  .object({
    template_type: z.string().optional(),
    industry: z.string().optional(),
    difficulty: z.string().optional(),
    estimated_hours: z.number().int().positive().optional()
  })
  .passthrough();

export const ProductAssetSchema = z.object({
  id: z.string(),
  label: z.string(),
  url: z.string(),
  mimeType: z.string().nullable().optional()
});

export const ProductSchema = z.object({
  id: z.string(),
  title: z.string(),
  description: z.string(),
  type: ProductTypeSchema,
  industry: z.string().nullable().optional(),
  currency: z.string(),
  priceCents: z.number().int().nonnegative(),
  stock: z.number().int().nonnegative().nullable().optional(),
  active: z.boolean(),
  metadata: ProductMetadataSchema.nullable().optional(),
  assets: z.array(ProductAssetSchema).default([])
});

export type Product = z.infer<typeof ProductSchema>;

export const PromoCodeSchema = z.object({
  code: z.string(),
  type: PromoTypeSchema,
  amount: z.number().int().positive(),
  currency: z.string().nullable().optional(),
  active: z.boolean(),
  startsAt: z.date().nullable().optional(),
  endsAt: z.date().nullable().optional(),
  maxRedemptions: z.number().int().positive().nullable().optional(),
  redemptionsCount: z.number().int().nonnegative()
});
export type PromoCode = z.infer<typeof PromoCodeSchema>;

export const OrderItemSchema = z.object({
  productId: z.string(),
  titleSnapshot: z.string(),
  unitPriceCents: z.number().int().nonnegative(),
  quantity: z.number().int().positive()
});
export type OrderItem = z.infer<typeof OrderItemSchema>;

export const OrderSchema = z.object({
  id: z.string(),
  userId: z.string().nullable().optional(),
  email: z.string().email(),
  status: OrderStatusSchema,
  currency: z.string(),
  subtotalCents: z.number().int().nonnegative(),
  discountCents: z.number().int().nonnegative(),
  totalCents: z.number().int().nonnegative(),
  promoCode: z.string().nullable().optional(),
  paymentProvider: z.string(),
  checkoutSessionId: z.string().nullable().optional(),
  paymentIntentId: z.string().nullable().optional(),
  items: z.array(OrderItemSchema)
});
export type Order = z.infer<typeof OrderSchema>;

