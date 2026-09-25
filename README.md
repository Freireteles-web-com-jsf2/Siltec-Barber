# Siltec-Barber

Sistema SaaS de agendamento online para barbearias — **Next.js 16** (App Router), **Prisma 7** com **PostgreSQL (Neon)**, **NextAuth v4** (Google) e **Tailwind CSS v4**.

## 📚 Documentação

- [Documentação do projeto — setup, login de teste, verificações e testes E2E](docs/README.md)
- [PRD — requisitos, arquitetura, riscos e roadmap](docs/PRD-Siltec-Barber.md)
- [Relatório de testes TestSprite (E2E) — 95,7% aprovados](testsprite_tests/testsprite-mcp-test-report.md)
- [Plano de testes — 45 cenários](testsprite_tests/testsprite_frontend_test_plan.json)
- [Histórico de migrações PostgreSQL](docs/migrations-postgresql.md)

## 🚀 Início rápido

```bash
pnpm install
pnpm exec prisma migrate deploy
pnpm exec prisma generate
pnpm exec prisma db seed
pnpm dev
```

Copie `.env.example` para `.env.local` e configure as credenciais do Google — ou habilite o **login de teste** (`TEST_LOGIN_ENABLED`) para desenvolver sem o OAuth. Instruções em [docs/README.md](docs/README.md).

## ✅ Status

- **E2E (TestSprite):** 45 cenários planejados; 23 executados em 24–25/09/2026 com **22 aprovados (95,7%)**, cobrindo cliente, páginas públicas e todo o painel admin.
- **Pendências conhecidas:** TC013 (sessão client-side defasada pós-login), TC001 (asserção fraca), ausência de suíte unitária/CI — detalhes no [PRD §17–19](docs/PRD-Siltec-Barber.md).

## 📄 Licença

Apache License 2.0
