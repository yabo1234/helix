import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // @ts-expect-error Vitest config (type augmentation can be flaky across toolchains)
  test: {
    environment: "jsdom",
    setupFiles: ["./src/test/setup.ts"]
  }
});
