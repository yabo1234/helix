import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiFetch } from "../../api";
import { useAuthToken } from "../../auth";
import { useMe } from "../../hooks/useMe";

export function AdminPromosPage() {
  const { token } = useAuthToken();
  const { me } = useMe(token);
  const nav = useNavigate();

  const [code, setCode] = useState("SAVE10");
  const [type, setType] = useState<"percent" | "fixed">("percent");
  const [amount, setAmount] = useState(10);
  const [error, setError] = useState<string | null>(null);
  const [created, setCreated] = useState(false);

  useEffect(() => {
    if (!me) return;
    if (me.role !== "ADMIN") nav("/admin");
  }, [me, nav]);

  async function create() {
    setError(null);
    setCreated(false);
    try {
      await apiFetch("/api/promos", { method: "POST", token, body: { code, type, amount } });
      setCreated(true);
    } catch (e: any) {
      setError(e.message);
    }
  }

  return (
    <main className="panel">
      <h2>Admin · Promo codes</h2>
      <div className="row">
        <Link to="/admin/products">Products</Link>
        <Link to="/admin/orders">Orders</Link>
      </div>

      <div className="grid2">
        <label>
          Code
          <input value={code} onChange={(e) => setCode(e.target.value)} />
        </label>
        <label>
          Type
          <select value={type} onChange={(e) => setType(e.target.value as any)}>
            <option value="percent">percent</option>
            <option value="fixed">fixed (cents)</option>
          </select>
        </label>
        <label>
          Amount
          <input type="number" value={amount} onChange={(e) => setAmount(parseInt(e.target.value || "0", 10))} />
        </label>
      </div>

      <button disabled={!token || !code} onClick={() => void create()}>
        Create promo
      </button>

      {created && <div className="ok">Promo created.</div>}
      {error && <div className="error">Error: {error}</div>}
    </main>
  );
}

