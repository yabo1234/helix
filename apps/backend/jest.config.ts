import type { Config } from "jest";

const config: Config = {
  testEnvironment: "node",
  transform: {
    "^.+\\.(t|j)sx?$": [
      "ts-jest",
      {
        tsconfig: "tsconfig.json",
        useESM: true
      }
    ]
  },
  moduleNameMapper: {
    "^(\\.{1,2}/.*)\\.js$": "$1"
  },
  extensionsToTreatAsEsm: [".ts"],
  testMatch: ["**/test/**/*.test.ts"]
};

export default config;

