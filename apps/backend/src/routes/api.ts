import { Router } from "express";
import type { Deps } from "../deps.js";
import { authRouter } from "./auth.js";
import { productsRouter } from "./products.js";
import { promosRouter } from "./promos.js";
import { checkoutRouter } from "./checkout.js";
import { ordersRouter } from "./orders.js";
import { chatRouter } from "./chat.js";
import { leadsRouter } from "./leads.js";
import { gdprRouter } from "./gdpr.js";
import { downloadsRouter } from "./downloads.js";
import { paymentsWebhookRouter } from "./webhooks.js";

export function createApiRouter(deps: Deps) {
  const r = Router();

  r.use("/webhooks/payments", paymentsWebhookRouter(deps));

  r.use("/auth", authRouter(deps));
  r.use("/products", productsRouter(deps));
  r.use("/promos", promosRouter(deps));
  r.use("/checkout", checkoutRouter(deps));
  r.use("/orders", ordersRouter(deps));
  r.use("/chat", chatRouter(deps));
  r.use("/leads", leadsRouter(deps));
  r.use("/gdpr", gdprRouter(deps));
  r.use("/downloads", downloadsRouter(deps));

  return r;
}

