import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { API_BASE_URL } from "../api";

export function CheckoutSuccessPage() {
  const [params] = useSearchParams();
  const orderId = params.get("orderId") ?? "";
  const mock = params.get("mock") === "1";
  const cs = params.get("cs") ?? "";
  const [marked, setMarked] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!mock || !orderId || !cs) return;
    // In mock mode, we trigger the backend webhook to mark the order paid.
    fetch(`${API_BASE_URL}/api/webhooks/payments`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        type: "checkout.session.completed",
        orderId,
        checkoutSessionId: cs
      })
    })
      .then(async (r) => {
        if (!r.ok) throw new Error(`http_${r.status}`);
        setMarked(true);
      })
      .catch((e) => setError(e.message));
  }, [mock, orderId, cs]);

  return (
    <main className="panel">
      <h2>Payment success</h2>
      {orderId ? <div className="muted">Order: {orderId}</div> : null}
      {mock ? (
        <div className="muted">{error ? `Mock webhook failed: ${error}` : marked ? "Mock payment confirmed." : "Confirming mock payment…"}</div>
      ) : (
        <div className="muted">Thanks! We’ll process your payment and email your receipt.</div>
      )}
      <div className="row">
        <Link to="/">Back to chat</Link>
      </div>
    </main>
  );
}

