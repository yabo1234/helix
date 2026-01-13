import { createApp } from "./app.js";
import { env, requireEnvKeys } from "./config/env.js";

requireEnvKeys(["DATABASE_URL", "JWT_SECRET", "DOWNLOAD_SIGNING_SECRET"]);

const app = createApp();

app.listen(env.PORT, () => {
  // eslint-disable-next-line no-console
  console.log(`helix-backend listening on :${env.PORT}`);
});

