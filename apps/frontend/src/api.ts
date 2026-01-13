export const API_BASE_URL =
  (import.meta as any).env?.VITE_API_BASE_URL?.toString?.() || "http://localhost:3001";

export type ApiError = { error: string };

export async function apiFetch<T>(
  path: string,
  opts?: { method?: string; body?: unknown; token?: string | null }
): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    method: opts?.method ?? "GET",
    headers: {
      "content-type": "application/json",
      ...(opts?.token ? { authorization: `Bearer ${opts.token}` } : {})
    },
    body: opts?.body ? JSON.stringify(opts.body) : undefined
  });
  if (!res.ok) {
    const t = (await res.json().catch(() => null)) as ApiError | null;
    throw new Error(t?.error ?? `http_${res.status}`);
  }
  return (await res.json()) as T;
}

