import { useState } from "react";
import { apiFetch } from "../api";

type ChatResponse = {
  reply: string;
  recommendations: Array<{
    productId: string;
    title: string;
    reason: string;
    productUrl: string;
    checkoutUrl: string;
  }>;
};

export function ProductFinder() {
  const [objectives, setObjectives] = useState("");
  const [budget, setBudget] = useState("");
  const [timeline, setTimeline] = useState("");
  const [result, setResult] = useState<ChatResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function submit() {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const message = `Outcome: ${objectives}\nBudget: ${budget}\nTimeline: ${timeline}`;
      const r = await apiFetch<ChatResponse>("/api/chat/recommend", { method: "POST", body: { message } });
      setResult(r);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="stack">
      <label>
        Objective
        <textarea value={objectives} onChange={(e) => setObjectives(e.target.value)} placeholder="What outcome do you want?" />
      </label>
      <label>
        Budget
        <input value={budget} onChange={(e) => setBudget(e.target.value)} placeholder="e.g., under $100" />
      </label>
      <label>
        Timeline
        <input value={timeline} onChange={(e) => setTimeline(e.target.value)} placeholder="e.g., today / next week" />
      </label>

      <button disabled={loading || !objectives.trim()} onClick={() => void submit()}>
        {loading ? "Finding…" : "Find products"}
      </button>

      {error && <div className="error">Error: {error}</div>}

      {result && (
        <div className="panel subtle">
          <div className="muted">{result.reply}</div>
          <ul>
            {result.recommendations.map((r) => (
              <li key={r.productId}>
                <strong>{r.title}</strong> — {r.reason}{" "}
                <a href={r.checkoutUrl} style={{ marginLeft: 8 }}>
                  Buy
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

