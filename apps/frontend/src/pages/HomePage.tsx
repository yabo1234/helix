import { ChatWidget } from "../ui/ChatWidget";
import { ProductFinder } from "../ui/ProductFinder";

export function HomePage() {
  return (
    <main className="grid">
      <section className="panel">
        <h2>Chat agent</h2>
        <p className="muted">
          Ask about outcomes, pricing, delivery/refunds, or compatibility. The agent will recommend 1–3 products and
          provide buy links.
        </p>
        <ChatWidget />
      </section>

      <section className="panel">
        <h2>Fallback product finder</h2>
        <p className="muted">Prefer forms? Fill this out and we’ll suggest products.</p>
        <ProductFinder />
      </section>
    </main>
  );
}

