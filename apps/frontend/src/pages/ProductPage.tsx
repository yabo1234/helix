import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { apiFetch } from "../api";

type Product = {
  id: string;
  title: string;
  description: string;
  type: "digital" | "consulting";
  industry?: string | null;
  currency: string;
  priceCents: number;
  assets: Array<{ id: string; label: string; url: string }>;
  metadata?: Record<string, unknown> | null;
};

export function ProductPage() {
  const { id } = useParams();
  const [product, setProduct] = useState<Product | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    apiFetch<Product>(`/api/products/${id}`)
      .then(setProduct)
      .catch((e) => setError(e.message));
  }, [id]);

  if (error) return <div className="panel error">Error: {error}</div>;
  if (!product) return <div className="panel">Loading…</div>;

  return (
    <main className="panel">
      <h2>{product.title}</h2>
      <div className="muted">
        {(product.priceCents / 100).toFixed(2)} {product.currency} · {product.type}
      </div>
      <p>{product.description}</p>

      {product.assets?.length ? (
        <>
          <h3>Assets</h3>
          <ul>
            {product.assets.map((a) => (
              <li key={a.id}>
                {a.label}: <span className="muted">{a.url}</span>
              </li>
            ))}
          </ul>
        </>
      ) : null}

      <div className="row">
        <Link to={`/checkout?productId=${encodeURIComponent(product.id)}`}>Buy now</Link>
        <Link to="/">Back</Link>
      </div>
    </main>
  );
}

