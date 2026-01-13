import express from "express";
import cors from "cors";
import helmet from "helmet";
import morgan from "morgan";
import rateLimit from "express-rate-limit";

import { healthRouter } from "./routes/health.js";
import { authMiddleware } from "./middleware/auth.js";
import { createDefaultDeps, type Deps } from "./deps.js";
import { createApiRouter } from "./routes/api.js";

export function createApp(deps: Deps = createDefaultDeps()) {
  const app = express();

  app.use(helmet());
  app.use(
    cors({
      origin: true,
      credentials: true
    })
  );
  app.use(morgan("dev"));
  app.use(
    rateLimit({
      windowMs: 60_000,
      limit: 120,
      standardHeaders: "draft-7",
      legacyHeaders: false
    })
  );
  app.use(authMiddleware);

  // Stripe webhooks need the *raw* request body.
  app.use("/api/webhooks/payments", express.raw({ type: "*/*" }));
  app.use(express.json({ limit: "1mb" }));

  app.get("/", (_req, res) => res.json({ ok: true, service: "helix-backend" }));
  app.use("/api/health", healthRouter);
  app.use("/api", createApiRouter(deps));

  // Basic error boundary
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  app.use((err: any, _req: express.Request, res: express.Response, _next: express.NextFunction) => {
    // eslint-disable-next-line no-console
    console.error(err);
    res.status(500).json({ error: "internal_error" });
  });

  return app;
}

