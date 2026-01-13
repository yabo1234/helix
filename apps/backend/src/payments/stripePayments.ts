import Stripe from "stripe";
import { env, requireEnvKeys } from "../config/env.js";
import type { CreateCheckoutSessionInput, CreateCheckoutSessionResult, PaymentEvent, Payments } from "./types.js";

export class StripePayments implements Payments {
  mode: "stripe" = "stripe";
  private stripe: Stripe;

  constructor() {
    requireEnvKeys(["STRIPE_SECRET_KEY", "STRIPE_WEBHOOK_SECRET"]);
    this.stripe = new Stripe(env.STRIPE_SECRET_KEY!, {
      apiVersion: "2024-11-20.acacia"
    });
  }

  async createCheckoutSession(input: CreateCheckoutSessionInput): Promise<CreateCheckoutSessionResult> {
    const session = await this.stripe.checkout.sessions.create({
      mode: "payment",
      customer_email: input.customerEmail,
      success_url: input.successUrl,
      cancel_url: input.cancelUrl,
      metadata: { orderId: input.orderId },
      line_items: [
        {
          quantity: 1,
          price_data: {
            currency: input.currency.toLowerCase(),
            unit_amount: input.amountCents,
            product_data: { name: "Helix order" }
          }
        }
      ]
    });
    return {
      checkoutSessionId: session.id,
      paymentIntentId: typeof session.payment_intent === "string" ? session.payment_intent : null,
      url: session.url ?? input.cancelUrl
    };
  }

  async parseWebhook(params: { rawBody: Buffer; signatureHeader: string | undefined }): Promise<PaymentEvent[]> {
    const sig = params.signatureHeader;
    if (!sig) return [];
    const evt = this.stripe.webhooks.constructEvent(
      params.rawBody,
      sig,
      env.STRIPE_WEBHOOK_SECRET!
    );

    if (evt.type === "checkout.session.completed") {
      const s = evt.data.object as Stripe.Checkout.Session;
      const orderId = (s.metadata?.orderId as string | undefined) ?? "";
      if (!orderId) return [];
      return [
        {
          type: "checkout.session.completed",
          orderId,
          checkoutSessionId: s.id,
          paymentIntentId: typeof s.payment_intent === "string" ? s.payment_intent : null
        }
      ];
    }
    return [];
  }
}

