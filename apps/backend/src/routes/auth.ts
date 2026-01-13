import { Router } from "express";
import { z } from "zod";
import type { Deps } from "../deps.js";
import { hashPassword, verifyPassword } from "../auth/password.js";
import { signAccessToken } from "../auth/jwt.js";
import { requireAuth, type AuthedRequest } from "../middleware/auth.js";

const SignupSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(200)
});

const LoginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1)
});

export function authRouter(deps: Deps) {
  const r = Router();

  r.post("/signup", async (req, res) => {
    const parsed = SignupSchema.safeParse(req.body);
    if (!parsed.success) return res.status(400).json({ error: "invalid_input" });
    const { email, password } = parsed.data;

    const existing = await deps.store.findUserByEmail(email);
    if (existing) return res.status(409).json({ error: "email_exists" });

    const passwordHash = await hashPassword(password);
    const user = await deps.store.createUser({ email, passwordHash, role: "CUSTOMER" });
    const token = signAccessToken({ sub: user.id, role: user.role });
    return res.status(201).json({ token, user: { id: user.id, email: user.email, role: user.role } });
  });

  r.post("/login", async (req, res) => {
    const parsed = LoginSchema.safeParse(req.body);
    if (!parsed.success) return res.status(400).json({ error: "invalid_input" });
    const { email, password } = parsed.data;

    const user = await deps.store.findUserByEmail(email);
    if (!user) return res.status(401).json({ error: "invalid_credentials" });
    const ok = await verifyPassword(password, user.passwordHash);
    if (!ok) return res.status(401).json({ error: "invalid_credentials" });

    const token = signAccessToken({ sub: user.id, role: user.role });
    return res.json({ token, user: { id: user.id, email: user.email, role: user.role } });
  });

  r.get("/me", requireAuth, async (req: AuthedRequest, res) => {
    const user = await deps.store.findUserById(req.auth!.userId);
    if (!user) return res.status(404).json({ error: "not_found" });
    return res.json({ id: user.id, email: user.email, role: user.role });
  });

  return r;
}

