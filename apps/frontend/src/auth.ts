import { useEffect, useState } from "react";

const TOKEN_KEY = "helix_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string | null) {
  if (!token) localStorage.removeItem(TOKEN_KEY);
  else localStorage.setItem(TOKEN_KEY, token);
}

export function useAuthToken() {
  const [token, setTok] = useState<string | null>(() => getToken());
  useEffect(() => {
    const onStorage = () => setTok(getToken());
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, []);
  return {
    token,
    setToken: (t: string | null) => {
      setToken(t);
      setTok(t);
    }
  };
}

