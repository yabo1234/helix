import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiFetch } from "../../api";
import { useAuthToken } from "../../auth";
import { useMe } from "../../hooks/useMe";

type LoginResponse = {
  token: string;
  user: { id: string; email: string; role: "ADMIN" | "CUSTOMER" };
};

export function AdminLoginPage() {
  const { token, setToken } = useAuthToken();
  const { me } = useMe(token);
  const nav = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (me?.role === "ADMIN") nav("/admin/products");
  }, [me, nav]);

  async function login() {
    setLoading(true);
    setError(null);
    try {
      const r = await apiFetch<LoginResponse>("/api/auth/login", {
        method: "POST",
        body: { email, password }
      });
      setToken(r.token);
      if (r.user.role !== "ADMIN") {
        setError("This account is not an admin.");
        return;
      }
      nav("/admin/products");
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="panel">
      <h2>Admin</h2>
      <div className="muted">Sign in with an admin account to manage products, promos, and orders.</div>

      <div className="stack">
        <label>
          Email
          <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="admin@example.com" />
        </label>
        <label>
          Password
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </label>

        <button disabled={loading || !email || !password} onClick={() => void login()}>
          {loading ? "Signing in…" : "Sign in"}
        </button>

        {error && <div className="error">Error: {error}</div>}

        <div className="row">
          <Link to="/">Back</Link>
        </div>
      </div>
    </main>
  );
}

