import { Router } from "express";
import { z } from "zod";
import type { Deps } from "../deps.js";
import { requireAdmin } from "../middleware/auth.js";

const PromoUpsertSchema = z.object({
  code: z.string().min(3),
  type: z.enum(["percent", "fixed"]),
  amount: z.number().int().positive(),
  currency: z.string().optional().nullable(),
  active: z.boolean().optional(),
  startsAt: z.string().datetime().optional().nullable(),
  endsAt: z.string().datetime().optional().nullable(),
  maxRedemptions: z.number().int().positive().optional().nullable()
});

export function promosRouter(deps: Deps) {
  const r = Router();

  r.post("/", requireAdmin, async (req, res) => {
    const parsed = PromoUpsertSchema.safeParse(req.body);
    if (!parsed.success) return res.status(400).json({ error: "invalid_input" });
    const promo = await deps.store.upsertPromo({
      ...parsed.data,
      startsAt: parsed.data.startsAt ? new Date(parsed.data.startsAt) : null,
      endsAt: parsed.data.endsAt ? new Date(parsed.data.endsAt) : null
    });
    return res.status(201).json(promo);
  });

  r.get("/:code", requireAdmin, async (req, res) => {
    const promo = await deps.store.getPromo(req.params.code);
    if (!promo) return res.status(404).json({ error: "not_found" });
    return res.json(promo);
  });

  return r;
}

