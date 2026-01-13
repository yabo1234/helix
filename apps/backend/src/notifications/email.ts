import sgMail from "@sendgrid/mail";
import { env } from "../config/env.js";
import type { Order } from "../domain/models.js";

export async function sendOrderConfirmationEmail(order: Order) {
  // If not configured, log and return (dev-friendly).
  if (!env.SENDGRID_API_KEY) {
    // eslint-disable-next-line no-console
    console.log(`[email] (mock) order confirmation to=${order.email} orderId=${order.id}`);
    return;
  }

  sgMail.setApiKey(env.SENDGRID_API_KEY);

  // NOTE: For real production, use a verified sender domain.
  const from = env.SUPPORT_ESCALATION_EMAIL || "support@example.com";

  await sgMail.send({
    to: order.email,
    from,
    subject: `Your Helix order ${order.id} receipt`,
    text: `Thanks for your purchase.\n\nOrder ID: ${order.id}\nTotal: ${(order.totalCents / 100).toFixed(
      2
    )} ${order.currency}\nStatus: ${order.status}\n\nIf you need help, reply to this email.`,
    html: `<p>Thanks for your purchase.</p>
<p><strong>Order ID:</strong> ${order.id}</p>
<p><strong>Total:</strong> ${(order.totalCents / 100).toFixed(2)} ${order.currency}</p>
<p><strong>Status:</strong> ${order.status}</p>
<p>If you need help, reply to this email.</p>`
  });
}

