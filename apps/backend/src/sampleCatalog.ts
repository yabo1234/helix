import type { Product } from "./domain/models.js";

export const sampleProducts: Product[] = [
  {
    id: "prod_001",
    title: "Business Analysis Template Pack",
    description:
      "Templates for stakeholder mapping, ROI modeling, requirements elicitation, and change impact analysis.",
    type: "digital",
    industry: "finance",
    priceCents: 4999,
    currency: "USD",
    stock: null,
    active: true,
    assets: [
      { id: "asset_pdf_001", label: "PDF", url: "https://example.com/sample-template-pack.pdf", mimeType: "application/pdf" }
    ],
    metadata: { difficulty: "intermediate", estimated_hours: 10, template_type: "general" }
  },
  {
    id: "prod_002",
    title: "BA Industry Report: Finance (2026)",
    description: "A practical industry report covering KPIs, regulatory trends, and opportunity sizing.",
    type: "digital",
    industry: "finance",
    priceCents: 7999,
    currency: "USD",
    stock: null,
    active: true,
    assets: [{ id: "asset_pdf_002", label: "PDF", url: "https://example.com/sample-finance-report.pdf", mimeType: "application/pdf" }],
    metadata: { difficulty: "beginner", estimated_hours: 6 }
  },
  {
    id: "prod_003",
    title: "1:1 Consulting Session (60 minutes)",
    description: "Book a live session to tailor a BA approach, review templates, or validate ROI models.",
    type: "consulting",
    industry: null,
    priceCents: 15000,
    currency: "USD",
    stock: null,
    active: true,
    assets: [],
    metadata: { difficulty: "all-levels", estimated_hours: 1 }
  }
];

