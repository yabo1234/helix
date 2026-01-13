import { Router } from "express";
import type { Deps } from "../deps.js";
import { requireAuth, type AuthedRequest } from "../middleware/auth.js";

export function gdprRouter(deps: Deps) {
  const r = Router();

  // Best-effort deletion endpoint.
  r.delete("/me", requireAuth, async (req: AuthedRequest, res) => {
    await deps.store.deleteUserData({ userId: req.auth!.userId });
    return res.status(204).send();
  });

  return r;
}

