import dotenv from "dotenv";
import { z } from "zod";

dotenv.config();

const EnvSchema = z.object({
  NODE_ENV: z.string().optional().default("development"),
  PORT: z.coerce.number().optional().default(3001),
  DATABASE_URL: z.string().min(1, "DATABASE_URL is required"),
  JWT_SECRET: z.string().min(16, "JWT_SECRET must be at least 16 chars"),
  DOWNLOAD_SIGNING_SECRET: z
    .string()
    .min(16, "DOWNLOAD_SIGNING_SECRET must be at least 16 chars"),
  PAYMENTS_MODE: z.enum(["mock", "stripe"]).optional().default("mock"),
  STRIPE_SECRET_KEY: z.string().optional().default(""),
  STRIPE_WEBHOOK_SECRET: z.string().optional().default(""),
  PUBLIC_APP_URL: z.string().url().optional().default("http://localhost:5173"),
  SENDGRID_API_KEY: z.string().optional().default(""),
  SUPPORT_ESCALATION_EMAIL: z.string().email().optional().default(""),
  LEAD_WEBHOOK_URL: z.string().url().optional().default(""),
  SLACK_WEBHOOK_URL: z.string().url().optional().default("")
});

export type Env = z.infer<typeof EnvSchema>;

export const env: Env = EnvSchema.parse(process.env);

