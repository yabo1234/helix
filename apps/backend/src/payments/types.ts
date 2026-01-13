export type CreateCheckoutSessionInput = {
  orderId: string;
  currency: string;
  amountCents: number;
  customerEmail: string;
  successUrl: string;
  cancelUrl: string;
};

export type CreateCheckoutSessionResult = {
  checkoutSessionId: string;
  paymentIntentId?: string | null;
  url: string;
};

export type PaymentEvent =
  | {
      type: "checkout.session.completed";
      orderId: string;
      checkoutSessionId: string;
      paymentIntentId?: string | null;
    }
  | { type: "payment.failed"; orderId: string; checkoutSessionId: string }
  | { type: "refund"; orderId: string; paymentIntentId: string };

export type Payments = {
  mode: "mock" | "stripe";
  createCheckoutSession(input: CreateCheckoutSessionInput): Promise<CreateCheckoutSessionResult>;
  parseWebhook(params: { rawBody: Buffer; signatureHeader: string | undefined }): Promise<PaymentEvent[]>;
};

