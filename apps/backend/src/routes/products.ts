import { Router } from "express";
import { z } from "zod";
import type { Deps } from "../deps.js";
import { requireAdmin } from "../middleware/auth.js";

const AssetInputSchema = z.object({
  label: z.string().min(1),
  url: z.string().min(1),
  mimeType: z.string().min(1).optional().nullable()
});

const ProductCreateSchema = z.object({
  id: z.string().min(3),
  title: z.string().min(1),
  description: z.string().optional(),
  type: z.enum(["digital", "consulting"]),
  industry: z.string().optional().nullable(),
  currency: z.string().default("USD"),
  priceCents: z.number().int().nonnegative(),
  stock: z.number().int().nonnegative().optional().nullable(),
  active: z.boolean().optional(),
  metadata: z.record(z.unknown()).optional().nullable(),
  assets: z.array(AssetInputSchema).optional()
});

const ProductUpdateSchema = ProductCreateSchema.omit({ id: true }).partial();

export function productsRouter(deps: Deps) {
  const r = Router();

  // Public
  r.get("/", async (req, res) => {
    const activeOnly = req.query.activeOnly === "true";
    const products = await deps.store.listProducts({ activeOnly });
    return res.json(products);
  });

  r.get("/:id", async (req, res) => {
    const p = await deps.store.getProduct(req.params.id);
    if (!p) return res.status(404).json({ error: "not_found" });
    return res.json(p);
  });

  // Admin
  r.post("/", requireAdmin, async (req, res) => {
    const parsed = ProductCreateSchema.safeParse(req.body);
    if (!parsed.success) return res.status(400).json({ error: "invalid_input" });
    try {
      const p = await deps.store.createProduct(parsed.data);
      return res.status(201).json(p);
    } catch (e: any) {
      if (e?.message === "PRODUCT_EXISTS") return res.status(409).json({ error: "product_exists" });
      throw e;
    }
  });

  r.patch("/:id", requireAdmin, async (req, res) => {
    const parsed = ProductUpdateSchema.safeParse(req.body);
    if (!parsed.success) return res.status(400).json({ error: "invalid_input" });
    try {
      const p = await deps.store.updateProduct(req.params.id, parsed.data);
      return res.json(p);
    } catch (e: any) {
      if (e?.message === "NOT_FOUND") return res.status(404).json({ error: "not_found" });
      throw e;
    }
  });

  r.delete("/:id", requireAdmin, async (req, res) => {
    await deps.store.deleteProduct(req.params.id);
    return res.status(204).send();
  });

  return r;
}

