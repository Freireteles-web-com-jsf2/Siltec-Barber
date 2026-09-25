# AGENTS.md

## Runtime and verification

- This is one root Next.js 16 App Router package: there is no `src/`, workspace package, test script, or source test suite. Prisma accepts Node `^20.19`, `^22.12`, or `>=24`, but `npm-check-updates` requires `^22.22.2`, `^24.15.0`, or `>=26`; use Node 24.15+ unless checking every tool. Use `pnpm@10.34.5`; `pnpm-workspace.yaml` only allowlists native builds.
- Set `DATABASE_URL` before `pnpm install`: `prepare` runs Husky and `prisma generate`, and the Prisma config validates the URL. For a fresh database, run `pnpm exec prisma migrate deploy`, then `pnpm exec prisma generate`; use `pnpm dev`, `pnpm build`, and `pnpm start` for the app.
- Verify with `pnpm lint` or focused `pnpm exec eslint <path>`, `pnpm exec next typegen` before `pnpm exec tsc --noEmit`, and `pnpm exec prisma validate` for schema work. There is no format script; use `pnpm exec prettier --write <files>` (2 spaces, no semicolons).
- `pnpm analyze` uses POSIX environment syntax and does not work in a Windows shell; set `$env:ANALYZE='true'` and run `pnpm build` instead.
- `tsconfig.json` includes both `.next/types` and `.next/dev/types`. Never edit `.next` or `next-env.d.ts`; if generated route types are corrupt, stop `next dev`, remove `.next`, and regenerate them.

## Database, environment, and access

- PostgreSQL hosted on Neon is the only configured provider: `prisma/schema.prisma` declares `provider = "postgresql"` and `prisma.config.ts` rejects any `DATABASE_URL` that is not `postgres://`/`postgresql://`. Runtime uses the HTTP driver adapter `PrismaNeonHttp` (`@prisma/adapter-neon`, fetch-based — no WebSocket/`ws`) through the lazy `db`/`getPrisma` wrapper, with `prisma/seed.ts` as the only direct-client exception; `$transaction` is used only in batch (array) form, which the HTTP adapter supports. `better-sqlite3` and `@prisma/adapter-better-sqlite3` were removed; `serverExternalPackages` now lists `@prisma/adapter-neon` and `@neondatabase/serverless`.
- Prisma 7 does not auto-load env files. `prisma.config.ts` uses a small parser for simple `KEY=value` lines, loads only `.env` and then `.env.local`, and fills missing values; process variables win, and `.env` wins over `.env.local` for duplicates. Multiline and `export` syntax are unsupported.
- `prisma/migrations` is the active PostgreSQL history (one baseline: `20260925000000_init_postgres`, applied to Neon); use `pnpm exec prisma migrate dev --name <name>` for schema changes and `pnpm exec prisma migrate deploy` for deploys. `prisma/migrations-sqlite` (archived SQLite history) and `prisma/migrations-postgresql` (stale pre-migration reference) are **not** read by Prisma — never apply either.
- Auth is NextAuth v4 with Google and Prisma/database sessions, not Auth.js v5. Runtime needs `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, and preferably a 32+ character `NEXT_AUTH_SECRET` (the minimum is a project diagnostic, not NextAuth enforcement). If it is absent, NextAuth can fall back to `NEXTAUTH_SECRET` or `AUTH_SECRET`, but diagnostics only recognize the first two. Production also needs a public, non-localhost `NEXTAUTH_URL`; `instrumentation.ts` only logs advisories.
- A test-only `/login` route (`app/(customer)/login`) accepts e-mail/password only when `TEST_LOGIN_ENABLED=true` (password comes from `TEST_LOGIN_PASSWORD`, set only in `.env.local`): it creates a database `Session` directly and redirects admins to `/dashboard`, customers to `/bookings`. The page itself always renders (the flag only hides the form; `export const dynamic = "force-dynamic"` keeps the env read at runtime) and always shows the Google button — `app/_components/sign-in-dialog.tsx` is the only place calling `signIn("google")`, and every unauthenticated login entry point (header icon, mobile sheet, "Reservar") links to `/login`. Never enable it in production — `checkDeployment` does NOT flag the variable (PRD RISK-021) and the action has no rate limit of its own.
- `DEMO_MODE=true` requires `DEMO_BARBERSHOP_ID` and makes every authenticated session an admin of that shop; never enable it in production. `SINGLE_BARBERSHOP_ID` changes routing/UI only, not tenant isolation; keep both IDs aligned when both flags are used.
- `pnpm exec prisma db seed` tops the catalog up to 10 shops with 6 services each (idempotent loop; services are only created for NEW shops) and creates no admin, so no application flow assigns `role`/`barbershopId` — except when `TEST_LOGIN_ENABLED=true`, where it also upserts the test users `cliente@teste.dev` (3 bookings), `vazio@teste.dev` (zero bookings) and `admin@teste.dev` (admin of the first shop). Keep that flag out of production and avoid rerunning the seed on a shared database.

## Architecture and authorization

- `app/(customer)` is customer-facing; `app/(admin)` owns `/dashboard`, `/schedule`, `/services`, and `/settings`. Underscore directories are private: root `app/_actions`, `_data`, `_lib`, `_components`, `_providers`, and `_constants` are shared across routes, while admin-specific code is colocated under `app/(admin)`.
- Loaders return domain data. Server actions generally return discriminated `{ ok: true }` / `{ ok: false, error }` results and call `revalidatePath` manually; audit every affected route because those lists are not centralized or guaranteed complete.
- `app/api` contains only NextAuth. Admin pages/actions use the server-side `requireBarbershopAdmin` gate (`Role.BARBER_ADMIN` plus a shop ID), not `proxy.ts`; admin `_data` loaders trust their caller and do not authorize, so never invoke them with an untrusted shop ID. The proxy only redirects `/barbershops/**` in single-tenant mode and does not authenticate.
- `Booking` has no `barbershopId` or barber/provider ID. Scope every shop-level booking query through `service: { barbershopId }`; all services in one shop share a single capacity, and `createBooking` derives the shop from the submitted `serviceId`.

## Scheduling and data invariants

- `app/_lib/opening-hours.ts` uses weekday `0` for Sunday, defaults missing rows to 09:00–19:00 with Sunday closed, and starts slots every 30 minutes only when the service duration fits before close. Hours must end on the same day; overnight schedules are unsupported. No timezone is stored, so use `app/(admin)/_lib/format.ts` instead of UTC date-string conversion.
- `app/_actions/create-booking.ts` is authoritative for authentication, future time, active service, opening hours, blocks, overlaps, and a global limit of three future `CONFIRMED` bookings per user. Availability/conflict queries exclude only `CANCELED`; `COMPLETED` and `NO_SHOW` still occupy intervals. Direct action input is not fully strict: slot comparison ignores seconds, time regexes accept values such as `99:99`, and opening-hour weekdays need not be distinct.
- Conflict detection and the three-booking cap are non-atomic check-then-insert operations with no database exclusion constraint. Schedule-block creation rejects only bookings whose start is inside the block, allows overlapping blocks, and does not validate every admin edit against the existing schedule; service-duration/opening-hour changes and reopening bookings are not rechecked.
- Services with bookings cannot be deleted. The detail loader still returns inactive services, service-name search can return a shop because an inactive service matched, and booking creation rejects inactive services; audit all public loaders when fixing visibility.
- `Booking` stores no price or duration snapshot, so service edits retroactively change history, agenda totals, and overlap calculations. Customer lists split future/past rows by date rather than status, and `deleteBooking` hard-deletes instead of setting `CANCELED`.
- `createBooking` only writes the database; confirmation and reminder WhatsApp messages are client-generated `wa.me` links. Service prices are Prisma `Decimal` values converted with `Number(...)` at boundaries, and shop phones are JSON strings parsed by `app/_lib/barbershop-phones.ts`.
- Rate limiting uses `RateLimiterPrisma` and the `RateLimit` table; keep `expire` as `DateTime`. Creation is 5/minute per user, schedule reads are 30/minute per user or derived IP, and admin writes share 20/minute per shop. Read denials return empty arrays, and unexpected store errors fall back/fail open.

## Tooling gotchas

- Next 16 request APIs are promises: await server-side `params`, `searchParams`, `headers`, and `cookies`; `revalidateTag` requires a cache profile, and `proxy.ts` replaces deprecated `middleware.ts`.
- ESLint 9 uses `eslint.config.mjs`; `.eslintrc.json` is legacy. Tailwind v4 is CSS-first in `app/globals.css`; there is no `tailwind.config.ts`, and `components.json` still contains nonexistent `@/lib`/`@/hooks` aliases, so fix aliases before using shadcn generators.
- In a Git checkout, the intended Husky hooks run `npx lint-staged` and a commit-message validator; lint-staged config is duplicated and divergent in `package.json` and `.lintstagedrc.json`. The `commit-msg` hook hard-codes the `commit-msg-linter@1.1.0` virtual-store path and reads the pt-BR, 100-character rules from `commitlinterrc.json`.
- `opencode.jsonc` launches an unpinned external TestSprite MCP, so do not assume capabilities from the package name. Versioned artifacts now live in `testsprite_tests/`: the 45-case plan (`testsprite_frontend_test_plan.json`), the generated `TC*.py` scripts and the consolidated report (`testsprite-mcp-test-report.md`, 95,7% across three batches). Execution is two-step: the `testsprite_generate_code_and_execute` tool writes `testsprite_tests/tmp/config.json` (+ a credential handoff file under `~/.testsprite/mcp/`), then the CLI `node <npx-cache>/.../dist/index.js generateCodeAndExecute` runs from the project root. The config contains a plaintext API key: never print it, and rotate/environment-wire it if the repository is shared.

<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
