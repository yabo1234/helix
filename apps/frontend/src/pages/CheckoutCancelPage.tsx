import { Link } from "react-router-dom";

export function CheckoutCancelPage() {
  return (
    <main className="panel">
      <h2>Checkout cancelled</h2>
      <div className="muted">No worries — you can return to the chat agent and pick a different option.</div>
      <div className="row">
        <Link to="/">Back to chat</Link>
      </div>
    </main>
  );
}

