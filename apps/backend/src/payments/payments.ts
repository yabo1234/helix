import { env } from "../config/env.js";
import { MockPayments } from "./mockPayments.js";
import { StripePayments } from "./stripePayments.js";
import type { Payments } from "./types.js";

export function createPayments(): Payments {
  if (env.PAYMENTS_MODE === "stripe") return new StripePayments();
  return new MockPayments();
}

