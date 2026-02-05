import { GetObjectCommand, S3Client } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

const DEFAULT_REGION = "us-east-1";
const MAX_PRESIGN_SECONDS = 7 * 24 * 60 * 60;

function resolveRegion() {
  return process.env.AWS_REGION || process.env.AWS_DEFAULT_REGION || DEFAULT_REGION;
}

const s3Client = new S3Client({
  region: resolveRegion(),
  endpoint: process.env.S3_ENDPOINT || undefined,
  forcePathStyle: Boolean(process.env.S3_ENDPOINT)
});

export function parseS3Url(url: string) {
  if (!url.startsWith("s3://")) return null;
  const withoutScheme = url.slice("s3://".length);
  const slashIndex = withoutScheme.indexOf("/");
  if (slashIndex <= 0 || slashIndex === withoutScheme.length - 1) return null;
  const bucket = withoutScheme.slice(0, slashIndex);
  const key = withoutScheme.slice(slashIndex + 1);
  if (!bucket || !key) return null;
  return { bucket, key };
}

export async function presignS3GetObject(url: string, params: { expiresInSeconds: number }) {
  const parsed = parseS3Url(url);
  if (!parsed) return null;
  const expiresInSeconds = Math.min(
    Math.max(1, params.expiresInSeconds),
    MAX_PRESIGN_SECONDS
  );
  const command = new GetObjectCommand({ Bucket: parsed.bucket, Key: parsed.key });
  try {
    return await getSignedUrl(s3Client, command, { expiresIn: expiresInSeconds });
  } catch {
    return null;
  }
}
