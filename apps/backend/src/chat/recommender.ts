import type { Product } from "../domain/models.js";

export type ChatIntent = "discovery" | "price_inquiry" | "technical_compatibility" | "policy";

export type ChatRecommendation = {
  intent: ChatIntent;
  reply: string;
  recommendations: Array<{
    productId: string;
    title: string;
    reason: string;
  }>;
  followUps: string[];
};

function norm(s: string) {
  return s.toLowerCase();
}

function includesAny(haystack: string, needles: string[]) {
  return needles.some((n) => haystack.includes(n));
}

export function detectIntent(message: string): ChatIntent {
  const m = norm(message);
  if (includesAny(m, ["price", "cost", "how much", "pricing", "discount", "promo"])) return "price_inquiry";
  if (includesAny(m, ["compatible", "format", "pdf", "excel", "sheets", "google", "mac", "windows"]))
    return "technical_compatibility";
  if (includesAny(m, ["refund", "return", "cancellation", "policy", "sample", "preview"])) return "policy";
  return "discovery";
}

function scoreProduct(message: string, p: Product) {
  const m = norm(message);
  let score = 0;
  const title = norm(p.title);
  const desc = norm(p.description ?? "");
  const industry = norm(p.industry ?? "");
  const templateType = norm((p.metadata as any)?.template_type ?? "");

  const keywords = [
    "stakeholder",
    "roi",
    "requirements",
    "mapping",
    "model",
    "template",
    "report",
    "consulting",
    "session",
    "training",
    "course",
    "finance",
    "healthcare",
    "retail"
  ];
  for (const k of keywords) {
    if (m.includes(k)) {
      if (title.includes(k)) score += 4;
      if (desc.includes(k)) score += 2;
      if (industry.includes(k)) score += 2;
      if (templateType.includes(k)) score += 1;
      if (p.type === "consulting" && (k === "consulting" || k === "session")) score += 3;
      if (p.type === "digital" && (k === "template" || k === "report")) score += 2;
    }
  }

  // Soft preference: digital for templates, consulting for "help me"
  if (includesAny(m, ["template", "pack"]) && p.type === "digital") score += 3;
  if (includesAny(m, ["help", "review", "audit", "custom", "tailor"]) && p.type === "consulting") score += 3;

  return score;
}

export function recommendProducts(params: {
  message: string;
  products: Product[];
  max?: number;
}): ChatRecommendation {
  const intent = detectIntent(params.message);
  const products = params.products.filter((p) => p.active);
  const ranked = products
    .map((p) => ({ p, score: scoreProduct(params.message, p) }))
    .sort((a, b) => b.score - a.score)
    .filter((x) => x.score > 0);

  const picks = (ranked.length ? ranked : products.map((p) => ({ p, score: 1 }))).slice(
    0,
    params.max ?? 3
  );

  if (intent === "price_inquiry") {
    const recs = picks.slice(0, 2).map(({ p }) => ({
      productId: p.id,
      title: p.title,
      reason: `Current price is ${(p.priceCents / 100).toFixed(2)} ${p.currency}.`
    }));
    return {
      intent,
      reply:
        "Here are the current prices for the most relevant options. If you share your budget and timeline, I can narrow to the best fit.",
      recommendations: recs,
      followUps: ["What’s your budget range?", "Do you need delivery today or within a week?"]
    };
  }

  if (intent === "technical_compatibility") {
    const recs = picks.slice(0, 2).map(({ p }) => ({
      productId: p.id,
      title: p.title,
      reason:
        p.type === "digital"
          ? "Digital products include common formats (PDF; spreadsheets when listed) and work on Mac/Windows."
          : "Consulting sessions are delivered via video call; no special software required."
    }));
    return {
      intent,
      reply:
        "Compatibility depends on the format you prefer (PDF vs spreadsheet) and your tools. Here are the closest matches and what you’ll get.",
      recommendations: recs,
      followUps: ["Do you need Excel, Google Sheets, or PDF only?", "Any constraints like Mac-only or offline access?"]
    };
  }

  if (intent === "policy") {
    const recs = picks.slice(0, 2).map(({ p }) => ({
      productId: p.id,
      title: p.title,
      reason: "I can also share a sample preview and outline refund/cancellation terms."
    }));
    return {
      intent,
      reply:
        "We can provide a sample preview for most digital products. Refunds/cancellations depend on whether the download link was accessed and whether a session was booked—ask and I’ll summarize the policy for your case.",
      recommendations: recs,
      followUps: ["Do you want a sample preview?", "Is this a digital download or a booked session?"]
    };
  }

  // discovery
  const recs = picks.slice(0, 3).map(({ p }) => {
    const reason =
      p.type === "digital"
        ? "Matches your requested outcome with reusable assets you can apply immediately."
        : "Great if you want tailored guidance and quick iteration on your specific ROI/stakeholder approach.";
    return { productId: p.id, title: p.title, reason };
  });
  return {
    intent,
    reply:
      "To recommend the best option, I’ll narrow by your outcome, budget, and timeline. Based on what you said, these are the top matches:",
    recommendations: recs,
    followUps: ["What outcome are you targeting?", "What’s your budget range?", "When do you need it by?"]
  };
}

