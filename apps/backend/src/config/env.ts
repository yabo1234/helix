import dotenv from "dotenv";
import { z } from "zod";

dotenv.config();

const EnvSchema = z.object({
  NODE_ENV: z.string().optional().default("development"),
  PORT: z.coerce.number().optional().default(3001),
  DATABASE_URL: z.string().min(1, "DATABASE_URL is required").optional(),
  JWT_SECRET: z.string().min(16, "JWT_SECRET must be at least 16 chars").optional(),
  DOWNLOAD_SIGNING_SECRET: z
    .string()
    .min(16, "DOWNLOAD_SIGNING_SECRET must be at least 16 chars")
    .optional(),
  PAYMENTS_MODE: z.enum(["mock", "stripe"]).optional().default("mock"),
  STRIPE_SECRET_KEY: z.string().optional().default(""),
  STRIPE_WEBHOOK_SECRET: z.string().optional().default(""),
  PUBLIC_APP_URL: z.string().url().optional().default("http://localhost:5173"),
  SENDGRID_API_KEY: z.string().optional().default(""),
  SUPPORT_ESCALATION_EMAIL: z.union([z.string().email(), z.literal("")]).optional().default(""),
  LEAD_WEBHOOK_URL: z.union([z.string().url(), z.literal("")]).optional().default(""),
  SLACK_WEBHOOK_URL: z.union([z.string().url(), z.literal("")]).optional().default("")
});

export type Env = z.infer<typeof EnvSchema>;

function withTestDefaults(input: NodeJS.ProcessEnv) {
  if (input.NODE_ENV !== "test") return input;
  return {
    ...input,
    DATABASE_URL: input.DATABASE_URL ?? "postgresql://test:test@localhost:5432/test?schema=public",
    JWT_SECRET: input.JWT_SECRET ?? "test_secret_which_is_long_enough",
    DOWNLOAD_SIGNING_SECRET: input.DOWNLOAD_SIGNING_SECRET ?? "test_download_secret_long_enough"
  };
}

export const env: Env = EnvSchema.parse(withTestDefaults(process.env));

export function requireEnvKeys(keys: Array<keyof Env>) {
  for (const key of keys) {
    const val = env[key];
    if (val == null || val === "") throw new Error(`Missing required env: ${String(key)}`);
  }
}

