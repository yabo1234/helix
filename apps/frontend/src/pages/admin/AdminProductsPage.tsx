import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiFetch } from "../../api";
import { useAuthToken } from "../../auth";
import { useMe } from "../../hooks/useMe";

type Product = {
  id: string;
  title: string;
  type: "digital" | "consulting";
  currency: string;
  priceCents: number;
  active: boolean;
};

export function AdminProductsPage() {
  const { token } = useAuthToken();
  const { me } = useMe(token);
  const nav = useNavigate();

  const [products, setProducts] = useState<Product[]>([]);
  const [error, setError] = useState<string | null>(null);

  const [id, setId] = useState("");
  const [title, setTitle] = useState("");
  const [type, setType] = useState<"digital" | "consulting">("digital");
  const [priceCents, setPriceCents] = useState(4999);
  const [assetUrl, setAssetUrl] = useState("https://example.com/sample.pdf");

  useEffect(() => {
    if (!me) return;
    if (me.role !== "ADMIN") nav("/admin");
  }, [me, nav]);

  async function refresh() {
    const ps = await apiFetch<Product[]>("/api/products");
    setProducts(ps);
  }

  useEffect(() => {
    void refresh().catch((e) => setError(e.message));
  }, []);

  async function create() {
    setError(null);
    try {
      await apiFetch<Product>("/api/products", {
        method: "POST",
        token,
        body: {
          id,
          title,
          type,
          currency: "USD",
          priceCents,
          assets: type === "digital" ? [{ label: "PDF", url: assetUrl }] : []
        }
      });
      setId("");
      setTitle("");
      await refresh();
    } catch (e: any) {
      setError(e.message);
    }
  }

  return (
    <main className="panel">
      <h2>Admin · Products</h2>
      <div className="row">
        <Link to="/admin/orders">Orders</Link>
        <Link to="/admin/promos">Promo codes</Link>
        <Link to="/">Back to chat</Link>
      </div>

      <h3>Create product</h3>
      <div className="grid2">
        <label>
          ID
          <input value={id} onChange={(e) => setId(e.target.value)} placeholder="prod_001" />
        </label>
        <label>
          Title
          <input value={title} onChange={(e) => setTitle(e.target.value)} />
        </label>
        <label>
          Type
          <select value={type} onChange={(e) => setType(e.target.value as any)}>
            <option value="digital">digital</option>
            <option value="consulting">consulting</option>
          </select>
        </label>
        <label>
          Price (cents)
          <input
            type="number"
            value={priceCents}
            onChange={(e) => setPriceCents(parseInt(e.target.value || "0", 10))}
          />
        </label>
        {type === "digital" ? (
          <label className="span2">
            Asset URL (demo)
            <input value={assetUrl} onChange={(e) => setAssetUrl(e.target.value)} />
          </label>
        ) : null}
      </div>
      <button disabled={!token || !id || !title} onClick={() => void create()}>
        Create
      </button>

      {error && <div className="error">Error: {error}</div>}

      <h3>Catalog</h3>
      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Type</th>
            <th>Price</th>
            <th>Active</th>
          </tr>
        </thead>
        <tbody>
          {products.map((p) => (
            <tr key={p.id}>
              <td>{p.id}</td>
              <td>{p.title}</td>
              <td>{p.type}</td>
              <td>
                {(p.priceCents / 100).toFixed(2)} {p.currency}
              </td>
              <td>{p.active ? "yes" : "no"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}

