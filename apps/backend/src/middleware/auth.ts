import type { Request, Response, NextFunction } from "express";
import { verifyAccessToken } from "../auth/jwt.js";

export type AuthedRequest = Request & {
  auth?: { userId: string; role: "ADMIN" | "CUSTOMER" };
};

export function authMiddleware(req: AuthedRequest, _res: Response, next: NextFunction) {
  const h = req.header("authorization");
  if (!h?.startsWith("Bearer ")) return next();
  const token = h.slice("Bearer ".length);
  try {
    const payload = verifyAccessToken(token);
    req.auth = { userId: payload.sub, role: payload.role };
  } catch {
    // ignore invalid token
  }
  next();
}

export function requireAuth(req: AuthedRequest, res: Response, next: NextFunction) {
  if (!req.auth) return res.status(401).json({ error: "unauthorized" });
  next();
}

export function requireAdmin(req: AuthedRequest, res: Response, next: NextFunction) {
  if (!req.auth) return res.status(401).json({ error: "unauthorized" });
  if (req.auth.role !== "ADMIN") return res.status(403).json({ error: "forbidden" });
  next();
}

