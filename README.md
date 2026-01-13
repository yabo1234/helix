## Helix: Business-Analysis Agent Storefront (Chat + Admin + Checkout)

This repo implements a **full-stack agent system** to market and sell business-analysis products (templates, reports, training, and consulting).

### What’s included

- **Chat agent**: guided product discovery + pricing/compatibility/policy Q&A + buy links
- **Fallback UI**: form-based product finder (for visitors who prefer forms)
- **Admin dashboard**: manage products, promo codes, and orders
- **Catalog API**: CRUD products + assets + BA-specific metadata
- **Checkout**: order creation + promo discounts + payment webhooks (Stripe or mock mode)
- **Digital downloads**: **expiring signed URLs** for purchased assets (demo signing; S3 signing placeholder)
- **Leads**: capture lead details and optionally send to webhook/Slack
- **Security basics**: bcrypt password hashing, JWT auth, input validation (Zod), rate limiting
- **GDPR**: best-effort “delete my data” endpoint
- **Tests**: backend API tests (chat intents, checkout+webhook, signed downloads) + frontend smoke test

### Repo layout

- `apps/backend`: Node.js + TypeScript + Express + Prisma schema (Postgres)
- `apps/frontend`: React + TypeScript + Vite (chat UI + admin UI)
- `docker-compose.yml`: Postgres + Redis + backend + frontend containers (for deployment)

---

## Quickstart (local)

### 1) Install dependencies

```bash
npm install
```

### 2) Configure env

- Copy `.env.example` to `.env` and set values (at minimum `DATABASE_URL`, `JWT_SECRET`, `DOWNLOAD_SIGNING_SECRET`)
- Backend also has `apps/backend/.env.example`
- Frontend has `apps/frontend/.env.example`

### 3) Run services

This project is designed to run with Postgres. If you have Docker available:

```bash
docker compose up --build
```

If you don’t have Docker, run Postgres locally and then:

```bash
# terminal 1
npm run dev -w @helix/backend

# terminal 2
npm run dev -w @helix/frontend
```

Frontend: `http://localhost:5173`  
Backend: `http://localhost:3001`

---

## Payments

### Mock mode (default)

Set:

- `PAYMENTS_MODE=mock`

Checkout will redirect to `/checkout/success` and the UI will mark the order paid via the webhook endpoint.

### Stripe mode

Set:

- `PAYMENTS_MODE=stripe`
- `STRIPE_SECRET_KEY=...`
- `STRIPE_WEBHOOK_SECRET=...`
- Configure your Stripe webhook to POST to `POST /api/webhooks/payments`

---

## Digital downloads (expiring signed URLs)

1. User purchases a digital product
2. Frontend requests a **signed URL**:
   - `GET /api/downloads/signed/:assetId?ttlSeconds=900`
3. Backend returns a time-limited URL:
   - `/api/downloads/serve?token=...`

If an asset URL starts with `s3://`, the backend returns a **placeholder response** (intended to be replaced with S3 pre-signed URL logic in production).

---

## Admin dashboard

Frontend routes:

- `/admin` login
- `/admin/products` create/list products
- `/admin/promos` create promo codes
- `/admin/orders` view orders

Note: the API currently does **not** expose “create admin” via public endpoints. For production, create an admin via DB migration/seed tooling.

---

## API endpoints (high level)

### Auth

- `POST /api/auth/signup`
- `POST /api/auth/login`
- `GET /api/auth/me`

### Products

- `GET /api/products`
- `GET /api/products/:id`
- `POST /api/products` (admin)
- `PATCH /api/products/:id` (admin)
- `DELETE /api/products/:id` (admin)

### Promo codes

- `POST /api/promos` (admin)
- `GET /api/promos/:code` (admin)

### Checkout & orders

- `POST /api/checkout/session` (creates order + payment session)
- `POST /api/webhooks/payments` (payment webhooks)
- `GET /api/orders/me` (customer)
- `GET /api/orders/:id` (customer/admin)
- `GET /api/orders` (admin)

### Chat + leads + GDPR

- `POST /api/chat/recommend`
- `POST /api/leads`
- `DELETE /api/gdpr/me`

## OpenAPI

- `apps/backend/openapi.yml`

---

## Curl examples

### Create checkout session

```bash
curl -sS -X POST "http://localhost:3001/api/checkout/session" \
  -H "content-type: application/json" \
  -d '{
    "email": "buyer@example.com",
    "currency": "USD",
    "promoCode": "SAVE20",
    "items": [{"productId":"prod_001","quantity":1}]
  }' | jq .
```

### Trigger mock webhook (mark paid)

```bash
curl -sS -X POST "http://localhost:3001/api/webhooks/payments" \
  -H "content-type: application/json" \
  -d '{
    "type": "checkout.session.completed",
    "orderId": "ORDER_ID_HERE",
    "checkoutSessionId": "mock_cs_..."
  }' | jq .
```

---

## Database schema & migrations

- Prisma schema: `apps/backend/prisma/schema.prisma`
- Generated SQL migration: `apps/backend/migrations/001_init.sql`

## Postman collection

- `docs/postman_collection.json`

---

## Tests

```bash
# backend
npm test -w @helix/backend

# frontend
npm test -w @helix/frontend
```

Backend tests cover:

- Chat recommendations across 3 intent scenarios
- Checkout creates an order; webhook marks it paid
- Signed download link flow

