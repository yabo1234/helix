import type { Store } from "./store/types.js";
import { PrismaStore } from "./store/prismaStore.js";
import type { Payments } from "./payments/types.js";
import { createPayments } from "./payments/payments.js";

export type Deps = {
  store: Store;
  payments: Payments;
};

export function createDefaultDeps(): Deps {
  const store = new PrismaStore();
  const payments = createPayments();
  return { store, payments };
}

