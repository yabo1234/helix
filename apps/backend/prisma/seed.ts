import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
  // Admin user (password is placeholder; set via manual hash in a real setup)
  const adminEmail = "admin@example.com";
  const existingAdmin = await prisma.user.findUnique({ where: { email: adminEmail } });
  if (!existingAdmin) {
    await prisma.user.create({
      data: {
        email: adminEmail,
        // NOTE: Replace with a real bcrypt hash if you intend to use this.
        passwordHash: "CHANGE_ME",
        role: "ADMIN"
      }
    });
  }

  await prisma.product.upsert({
    where: { id: "prod_001" },
    update: {},
    create: {
      id: "prod_001",
      title: "Business Analysis Template Pack",
      description:
        "Templates for stakeholder mapping, ROI modeling, requirements elicitation, and change impact analysis.",
      type: "digital",
      industry: "finance",
      currency: "USD",
      priceCents: 4999,
      stock: null,
      metadata: { difficulty: "intermediate", estimated_hours: 10, template_type: "general" },
      assets: {
        create: [{ label: "PDF", url: "s3://example-bucket/template-pack.pdf", mimeType: "application/pdf" }]
      }
    }
  });

  await prisma.product.upsert({
    where: { id: "prod_003" },
    update: {},
    create: {
      id: "prod_003",
      title: "1:1 Consulting Session (60 minutes)",
      description: "Book a live session to tailor a BA approach, review templates, or validate ROI models.",
      type: "consulting",
      currency: "USD",
      priceCents: 15000,
      stock: null,
      metadata: { difficulty: "all-levels", estimated_hours: 1 }
    }
  });

  await prisma.promoCode.upsert({
    where: { code: "SAVE20" },
    update: {},
    create: { code: "SAVE20", type: "percent", amount: 20, active: true }
  });
}

main()
  .then(async () => prisma.$disconnect())
  .catch(async (e) => {
    console.error(e);
    await prisma.$disconnect();
    process.exit(1);
  });

