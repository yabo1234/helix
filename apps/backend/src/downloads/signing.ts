import crypto from "crypto";
import { env } from "../config/env.js";

export type DownloadTokenPayload = {
  assetId: string;
  userId: string;
  exp: number; // unix seconds
};

function b64url(buf: Buffer) {
  return buf
    .toString("base64")
    .replace(/=/g, "")
    .replace(/\+/g, "-")
    .replace(/\//g, "_");
}

function unb64url(s: string) {
  s = s.replace(/-/g, "+").replace(/_/g, "/");
  while (s.length % 4) s += "=";
  return Buffer.from(s, "base64");
}

export function signDownloadToken(payload: DownloadTokenPayload) {
  const body = Buffer.from(JSON.stringify(payload), "utf8");
  const mac = crypto.createHmac("sha256", env.DOWNLOAD_SIGNING_SECRET ?? "missing").update(body).digest();
  return `${b64url(body)}.${b64url(mac)}`;
}

export function verifyDownloadToken(token: string): DownloadTokenPayload | null {
  const [p, sig] = token.split(".");
  if (!p || !sig) return null;
  const body = unb64url(p);
  const mac = crypto.createHmac("sha256", env.DOWNLOAD_SIGNING_SECRET ?? "missing").update(body).digest();
  const ok = crypto.timingSafeEqual(unb64url(sig), mac);
  if (!ok) return null;
  const payload = JSON.parse(body.toString("utf8")) as DownloadTokenPayload;
  if (typeof payload?.exp !== "number") return null;
  if (Date.now() / 1000 > payload.exp) return null;
  return payload;
}

