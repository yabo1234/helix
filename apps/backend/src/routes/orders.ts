import { Router } from "express";
import type { Deps } from "../deps.js";
import { requireAdmin, requireAuth, type AuthedRequest } from "../middleware/auth.js";

export function ordersRouter(deps: Deps) {
  const r = Router();

  r.get("/me", requireAuth, async (req: AuthedRequest, res) => {
    const orders = await deps.store.listOrders({ userId: req.auth!.userId });
    return res.json(orders);
  });

  r.get("/:id", requireAuth, async (req: AuthedRequest, res) => {
    const order = await deps.store.getOrder(req.params.id);
    if (!order) return res.status(404).json({ error: "not_found" });
    if (req.auth!.role !== "ADMIN" && order.userId !== req.auth!.userId) {
      return res.status(403).json({ error: "forbidden" });
    }
    return res.json(order);
  });

  r.get("/", requireAdmin, async (req, res) => {
    const email = typeof req.query.email === "string" ? req.query.email : undefined;
    const orders = await deps.store.listOrders({ email });
    return res.json(orders);
  });

  return r;
}

