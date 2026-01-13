import { Router } from "express";
import { z } from "zod";
import type { Deps } from "../deps.js";
import { env } from "../config/env.js";
import type { AuthedRequest } from "../middleware/auth.js";

const CreateSessionSchema = z.object({
  email: z.string().email(),
  currency: z.string().default("USD"),
  promoCode: z.string().optional().nullable(),
  items: z
    .array(
      z.object({
        productId: z.string().min(1),
        quantity: z.number().int().positive().default(1)
      })
    )
    .min(1)
});

export function checkoutRouter(deps: Deps) {
  const r = Router();

  r.post("/session", async (req: AuthedRequest, res) => {
    const parsed = CreateSessionSchema.safeParse(req.body);
    if (!parsed.success) return res.status(400).json({ error: "invalid_input" });

    const order = await deps.store.createOrder({
      userId: req.auth?.userId ?? null,
      email: parsed.data.email,
      currency: parsed.data.currency,
      items: parsed.data.items,
      promoCode: parsed.data.promoCode ?? null,
      paymentProvider: deps.payments.mode
    });

    const successUrl = `${env.PUBLIC_APP_URL}/checkout/success`;
    const cancelUrl = `${env.PUBLIC_APP_URL}/checkout/cancel`;

    const session = await deps.payments.createCheckoutSession({
      orderId: order.id,
      currency: order.currency,
      amountCents: order.totalCents,
      customerEmail: order.email,
      successUrl,
      cancelUrl
    });

    const updatedOrder = await deps.store.updateOrderStatus({
      orderId: order.id,
      status: "pending",
      checkoutSessionId: session.checkoutSessionId,
      paymentIntentId: session.paymentIntentId ?? null
    });

    return res.status(201).json({
      order: updatedOrder,
      checkoutUrl: session.url,
      tax: { mode: "placeholder", amountCents: 0 }
    });
  });

  return r;
}

