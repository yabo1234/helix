import { useMemo, useState } from "react";
import { apiFetch } from "../api";

type ChatResponse = {
  intent: string;
  reply: string;
  recommendations: Array<{
    productId: string;
    title: string;
    reason: string;
    productUrl: string;
    checkoutUrl: string;
  }>;
  followUps: string[];
};

type Msg = { role: "user" | "bot"; text: string };

export function ChatWidget() {
  const [messages, setMessages] = useState<Msg[]>([
    { role: "bot", text: "What business analysis outcome are you looking for?" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const lastUserText = useMemo(() => [...messages].reverse().find((m) => m.role === "user")?.text ?? "", [messages]);

  async function send(text: string) {
    setLoading(true);
    setMessages((m) => [...m, { role: "user", text }]);
    try {
      const r = await apiFetch<ChatResponse>("/api/chat/recommend", { method: "POST", body: { message: text } });
      const recLines =
        r.recommendations.length === 0
          ? ""
          : "\n\nTop picks:\n" +
            r.recommendations
              .map((p) => `- ${p.title} (${(p.productId ?? "").toString()}): ${p.reason}`)
              .join("\n");
      const follow = r.followUps?.length ? `\n\nNext: ${r.followUps[0]}` : "";
      setMessages((m) => [...m, { role: "bot", text: `${r.reply}${recLines}${follow}` }]);
      setRecommendations(r.recommendations);
    } catch (e: any) {
      setMessages((m) => [...m, { role: "bot", text: `Sorry — I couldn't answer that (${e.message}).` }]);
    } finally {
      setLoading(false);
    }
  }

  const [recommendations, setRecommendations] = useState<ChatResponse["recommendations"]>([]);

  return (
    <div>
      <div className="chatBox" aria-label="chat">
        {messages.map((m, idx) => (
          <div key={idx} className={`msg ${m.role}`}>
            <div className="bubble">
              <pre className="pre">{m.text}</pre>
            </div>
          </div>
        ))}
      </div>

      <form
        className="row"
        onSubmit={(e) => {
          e.preventDefault();
          const t = input.trim();
          if (!t) return;
          setInput("");
          void send(t);
        }}
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="e.g., I need templates for stakeholder mapping and ROI modeling"
        />
        <button disabled={loading}>{loading ? "Sending…" : "Send"}</button>
      </form>

      {recommendations.length > 0 && (
        <div className="recommendations">
          <h3>Recommended</h3>
          <ul>
            {recommendations.map((r) => (
              <li key={r.productId}>
                <strong>{r.title}</strong>
                <div className="muted">{r.reason}</div>
                <div className="row">
                  <a href={r.productUrl}>View</a>
                  <a href={r.checkoutUrl}>Buy</a>
                </div>
              </li>
            ))}
          </ul>
          <div className="muted">Last message: {lastUserText}</div>
        </div>
      )}
    </div>
  );
}

