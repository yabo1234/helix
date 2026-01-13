import { Router } from "express";
import type { Deps } from "../deps.js";
import { sendOrderConfirmationEmail } from "../notifications/email.js";

export function paymentsWebhookRouter(deps: Deps) {
  const r = Router();

  r.post("/", async (req, res) => {
    const rawBody = Buffer.isBuffer(req.body) ? (req.body as Buffer) : Buffer.from("");
    const signatureHeader = req.header("stripe-signature") ?? req.header("x-signature") ?? undefined;

    const events = await deps.payments.parseWebhook({ rawBody, signatureHeader });
    for (const evt of events) {
      if (evt.type === "checkout.session.completed") {
        const updated = await deps.store.updateOrderStatus({
          orderId: evt.orderId,
          status: "paid",
          checkoutSessionId: evt.checkoutSessionId,
          paymentIntentId: evt.paymentIntentId ?? null
        });
        // Best-effort order confirmation email
        void sendOrderConfirmationEmail(updated).catch(() => {});
      }
      if (evt.type === "payment.failed") {
        await deps.store.updateOrderStatus({
          orderId: evt.orderId,
          status: "failed",
          checkoutSessionId: evt.checkoutSessionId
        });
      }
      if (evt.type === "refund") {
        await deps.store.updateOrderStatus({
          orderId: evt.orderId,
          status: "refunded",
          paymentIntentId: evt.paymentIntentId
        });
      }
    }

    return res.json({ received: true });
  });

  return r;
}

