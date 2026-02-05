import { Router } from "express";
import { z } from "zod";
import type { Deps } from "../deps.js";
import { requireAuth, type AuthedRequest } from "../middleware/auth.js";
import { signDownloadToken, verifyDownloadToken } from "../downloads/signing.js";
import { presignS3GetObject } from "../downloads/s3.js";

const SignedUrlQuerySchema = z.object({
  ttlSeconds: z.coerce.number().int().positive().max(60 * 60).optional().default(15 * 60)
});

export function downloadsRouter(deps: Deps) {
  const r = Router();

  r.get("/signed/:assetId", requireAuth, async (req: AuthedRequest, res) => {
    const q = SignedUrlQuerySchema.safeParse(req.query);
    if (!q.success) return res.status(400).json({ error: "invalid_input" });

    const asset = await deps.store.getAsset({ assetId: req.params.assetId });
    if (!asset) return res.status(404).json({ error: "not_found" });

    const owns = await deps.store.userOwnsProduct({ userId: req.auth!.userId, productId: asset.productId });
    if (!owns) return res.status(403).json({ error: "not_purchased" });

    const token = signDownloadToken({
      assetId: asset.id,
      userId: req.auth!.userId,
      exp: Math.floor(Date.now() / 1000) + q.data.ttlSeconds
    });
    return res.json({
      signedUrl: `/api/downloads/serve?token=${encodeURIComponent(token)}`,
      expiresInSeconds: q.data.ttlSeconds
    });
  });

  r.get("/serve", async (req, res) => {
    const token = typeof req.query.token === "string" ? req.query.token : "";
    const payload = verifyDownloadToken(token);
    if (!payload) return res.status(401).json({ error: "invalid_or_expired" });

    const asset = await deps.store.getAsset({ assetId: payload.assetId });
    if (!asset) return res.status(404).json({ error: "not_found" });

    // Optional: enforce ownership at time of download too.
    const owns = await deps.store.userOwnsProduct({ userId: payload.userId, productId: asset.productId });
    if (!owns) return res.status(403).json({ error: "not_purchased" });

    if (asset.url.startsWith("s3://")) {
      const remainingSeconds = Math.max(1, Math.floor(payload.exp - Date.now() / 1000));
      const signedUrl = await presignS3GetObject(asset.url, { expiresInSeconds: remainingSeconds });
      if (!signedUrl) return res.status(500).json({ error: "s3_signing_failed" });
      return res.redirect(signedUrl);
    }

    return res.redirect(asset.url);
  });

  return r;
}

