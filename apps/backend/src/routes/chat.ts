import { Router } from "express";
import { z } from "zod";
import type { Deps } from "../deps.js";
import { env } from "../config/env.js";
import { recommendProducts } from "../chat/recommender.js";
import { sampleProducts } from "../sampleCatalog.js";

const ChatSchema = z.object({
  message: z.string().min(1).max(4000)
});

export function chatRouter(deps: Deps) {
  const r = Router();

  r.post("/recommend", async (req, res) => {
    const parsed = ChatSchema.safeParse(req.body);
    if (!parsed.success) return res.status(400).json({ error: "invalid_input" });

    const products = await deps.store.listProducts({ activeOnly: true });
    const catalog = products.length ? products : sampleProducts;
    const rec = recommendProducts({ message: parsed.data.message, products: catalog, max: 3 });

    return res.json({
      ...rec,
      recommendations: rec.recommendations.map((x) => ({
        ...x,
        productUrl: `${env.PUBLIC_APP_URL}/products/${x.productId}`,
        checkoutUrl: `${env.PUBLIC_APP_URL}/checkout?productId=${encodeURIComponent(x.productId)}`
      }))
    });
  });

  return r;
}

