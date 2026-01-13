import { useEffect, useState } from "react";
import { apiFetch } from "../api";

export type Me = { id: string; email: string; role: "ADMIN" | "CUSTOMER" };

export function useMe(token: string | null) {
  const [me, setMe] = useState<Me | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) {
      setMe(null);
      return;
    }
    setLoading(true);
    setError(null);
    apiFetch<Me>("/api/auth/me", { token })
      .then(setMe)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [token]);

  return { me, loading, error };
}

