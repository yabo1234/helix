import { Router } from "express";
import { z } from "zod";
import type { Deps } from "../deps.js";
import { env } from "../config/env.js";

const LeadSchema = z.object({
  name: z.string().optional().nullable(),
  email: z.string().email(),
  message: z.string().min(1).max(2000),
  source: z.string().optional().default("chat")
});

export function leadsRouter(deps: Deps) {
  const r = Router();

  r.post("/", async (req, res) => {
    const parsed = LeadSchema.safeParse(req.body);
    if (!parsed.success) return res.status(400).json({ error: "invalid_input" });

    const lead = await deps.store.createLead(parsed.data);

    // Best-effort integrations
    const payload = { ...parsed.data, id: lead.id, createdAt: lead.createdAt.toISOString() };

    if (env.LEAD_WEBHOOK_URL) {
      fetch(env.LEAD_WEBHOOK_URL, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(payload)
      }).catch(() => {});
    }
    if (env.SLACK_WEBHOOK_URL) {
      fetch(env.SLACK_WEBHOOK_URL, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          text: `New lead: ${payload.email}\n${payload.message}`
        })
      }).catch(() => {});
    }

    return res.status(201).json({ ok: true, leadId: lead.id });
  });

  return r;
}

