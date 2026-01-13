import { useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { apiFetch } from "../api";
import { useAuthToken } from "../auth";

type Product = {
  id: string;
  title: string;
  currency: string;
  priceCents: number;
  type: "digital" | "consulting";
};

type CheckoutSessionResponse = {
  order: {
    id: string;
    status: string;
    subtotalCents: number;
    discountCents: number;
    totalCents: number;
    checkoutSessionId?: string | null;
    paymentIntentId?: string | null;
  };
  checkoutUrl: string;
};

export function CheckoutPage() {
  const [params] = useSearchParams();
  const productId = params.get("productId");
  const { token } = useAuthToken();

  const [product, setProduct] = useState<Product | null>(null);
  const [email, setEmail] = useState("");
  const [promoCode, setPromoCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const priceLabel = useMemo(() => {
    if (!product) return "";
    return `${(product.priceCents / 100).toFixed(2)} ${product.currency}`;
  }, [product]);

  useEffect(() => {
    if (!productId) return;
    apiFetch<Product>(`/api/products/${productId}`)
      .then((p) => setProduct(p))
      .catch((e) => setError(e.message));
  }, [productId]);

  async function startCheckout() {
    if (!productId) return;
    setLoading(true);
    setError(null);
    try {
      const r = await apiFetch<CheckoutSessionResponse>("/api/checkout/session", {
        method: "POST",
        token,
        body: {
          email,
          currency: product?.currency ?? "USD",
          promoCode: promoCode.trim() ? promoCode.trim() : null,
          items: [{ productId, quantity: 1 }]
        }
      });
      window.location.href = r.checkoutUrl;
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  if (!productId) {
    return (
      <main className="panel">
        <h2>Checkout</h2>
        <div className="error">Missing productId</div>
        <Link to="/">Back</Link>
      </main>
    );
  }

  return (
    <main className="panel">
      <h2>Checkout</h2>
      {product ? (
        <div className="muted">
          Buying <strong>{product.title}</strong> · {priceLabel}
        </div>
      ) : (
        <div className="muted">Loading product…</div>
      )}

      <div className="stack">
        <label>
          Email
          <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@company.com" />
        </label>
        <label>
          Promo code (optional)
          <input value={promoCode} onChange={(e) => setPromoCode(e.target.value)} placeholder="SAVE20" />
        </label>

        <button disabled={loading || !email.trim()} onClick={() => void startCheckout()}>
          {loading ? "Starting…" : "Continue to payment"}
        </button>

        {error && <div className="error">Error: {error}</div>}

        <div className="row">
          <Link to={`/products/${encodeURIComponent(productId)}`}>View product</Link>
          <Link to="/">Back</Link>
        </div>
      </div>
    </main>
  );
}

