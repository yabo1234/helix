import crypto from "crypto";
import type { CreateCheckoutSessionInput, CreateCheckoutSessionResult, PaymentEvent, Payments } from "./types.js";

export class MockPayments implements Payments {
  mode: "mock" = "mock";

  async createCheckoutSession(input: CreateCheckoutSessionInput): Promise<CreateCheckoutSessionResult> {
    const checkoutSessionId = `mock_cs_${crypto.randomBytes(8).toString("hex")}`;
    const paymentIntentId = `mock_pi_${crypto.randomBytes(8).toString("hex")}`;
    // In mock mode, we "redirect" back to success immediately.
    const url = `${input.successUrl}?orderId=${encodeURIComponent(input.orderId)}&mock=1&cs=${encodeURIComponent(
      checkoutSessionId
    )}`;
    return { checkoutSessionId, paymentIntentId, url };
  }

  async parseWebhook(params: { rawBody: Buffer; signatureHeader: string | undefined }): Promise<PaymentEvent[]> {
    // Expect JSON: { type: "checkout.session.completed", checkoutSessionId, paymentIntentId? }
    // No signature validation in mock mode.
    const parsed = JSON.parse(params.rawBody.toString("utf8")) as any;
    if (!parsed?.type) return [];
    if (!parsed?.orderId) return [];
    return [parsed as PaymentEvent];
  }
}

