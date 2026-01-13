import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiFetch } from "../../api";
import { useAuthToken } from "../../auth";
import { useMe } from "../../hooks/useMe";

type Order = {
  id: string;
  email: string;
  status: string;
  subtotalCents: number;
  discountCents: number;
  totalCents: number;
  createdAt?: string;
};

export function AdminOrdersPage() {
  const { token } = useAuthToken();
  const { me } = useMe(token);
  const nav = useNavigate();

  const [orders, setOrders] = useState<Order[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!me) return;
    if (me.role !== "ADMIN") nav("/admin");
  }, [me, nav]);

  useEffect(() => {
    if (!token) return;
    apiFetch<Order[]>("/api/orders", { token })
      .then(setOrders)
      .catch((e) => setError(e.message));
  }, [token]);

  return (
    <main className="panel">
      <h2>Admin · Orders</h2>
      <div className="row">
        <Link to="/admin/products">Products</Link>
        <Link to="/admin/promos">Promo codes</Link>
      </div>

      {error && <div className="error">Error: {error}</div>}

      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Email</th>
            <th>Status</th>
            <th>Total</th>
          </tr>
        </thead>
        <tbody>
          {orders.map((o) => (
            <tr key={o.id}>
              <td className="mono">{o.id}</td>
              <td>{o.email}</td>
              <td>{o.status}</td>
              <td>${(o.totalCents / 100).toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}

