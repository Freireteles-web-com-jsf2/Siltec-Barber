## 🧱 Siltec-Barber

Siltec-Barber é um sistema SaaS de agendamento online para barbearias. Usuários podem escolher serviços, visualizar barbearias disponíveis e reservar horários — tudo de forma rápida e intuitiva, diretamente pelo site.

## Documentação do projeto

- [PRD — Siltec-Barber](./PRD-Siltec-Barber.md)
- [Histórico de migrações PostgreSQL](./migrations-postgresql.md)
- [Relatório de testes TestSprite (E2E)](../testsprite_tests/testsprite-mcp-test-report.md)
- [Plano de testes — 45 cenários](../testsprite_tests/testsprite_frontend_test_plan.json)

Projeto full‑stack com **Next.js**.

- 🔍 Busca por barbearias e serviços
- 📅 Agendamento com escolha de data e horário
- 📱 Design responsivo
- 🧾 Visualização de reservas
- 🔐 Login e autenticação

## 🧩 Tech Stack

[![Next.js](https://img.shields.io/badge/Next.js-000000?logo=nextdotjs&logoColor=white&style=for-the-badge)](https://nextjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white&style=for-the-badge)](https://neon.tech)
[![Node.js](https://img.shields.io/badge/Node.js-339933?logo=node.js&logoColor=white&style=for-the-badge)](https://nodejs.org/)
[![React](https://img.shields.io/badge/React-20232A?logo=react&logoColor=61DAFB&style=for-the-badge)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white&style=for-the-badge)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?logo=tailwind-css&logoColor=white&style=for-the-badge)](https://tailwindcss.com/)
[![shadcn/ui](https://img.shields.io/badge/shadcn%2Fui-2.7-000000?logo=shadcnui&logoColor=white&style=for-the-badge)](https://ui.shadcn.com)
[![Prisma](https://img.shields.io/badge/Prisma-2D3748?logo=prisma&logoColor=blue&style=for-the-badge)](https://www.prisma.io/)

```text
🗂️ Estrutura do Projeto
`/`
├─ app/               → App Router: rotas, actions e componentes
│  ├─ (customer)/     → Área do cliente (/, /barbershops, /bookings, /perfil, /login)
│  ├─ (admin)/        → Painel (/dashboard, /schedule, /services, /settings)
│  ├─ _actions/       → Server Actions compartilhadas
│  ├─ _data/          → Carregadores de dados
│  └─ _components/    → Componentes compartilhados
├─ prisma/            → Schema, migrações (PostgreSQL) e seed
├─ docs/              → PRD e documentação
├─ testsprite_tests/  → Plano e relatório de testes E2E (TestSprite)
├─ public/            → Arquivos estáticos (imagens, fontes etc.)
├─ .husky/            → Hooks do Git
├─ eslint.config.mjs  → Configuração do ESLint 9
├─ .prettierrc        → Configuração do Prettier
├─ proxy.ts           → Proxy/rewrites (substitui middleware.ts no Next 16)
├─ next.config.mjs    → Configurações personalizadas do Next.js
├─ tsconfig.json      → Configurações do TypeScript
├─ package.json       → Scripts e dependências
└─ ...                → Outros arquivos de configuração
```

## 📸 Demonstrações

https://github.com/user-attachments/assets/3da5f7be-be67-4594-ab43-8a73d076399a

#### Figma

https://www.figma.com/design/KKq1t6YEm0WtAlOJbLLe5h/BarberLaB?node-id=1-9&t=ffjK4bbnBSixEejh-1

### Desktop

#### Início

![screencapture-barber-lab-vercel-app-2025-07-09-15_08_50](https://github.com/user-attachments/assets/48bbc5dc-9ea2-4257-8b2c-1cc69f2a4bd3)

#### Barbearias

![screencapture-barber-lab-vercel-app-barbershops-2025-07-09-15_11_01](https://github.com/user-attachments/assets/1fc8e1ed-6a81-48e3-ae68-05d1646265a2)

#### Agendamentos

![screencapture-barber-lab-vercel-app-bookings-2025-07-09-15_12_31](https://github.com/user-attachments/assets/fd9b32cb-677b-4918-a916-93d0c80df5c6)

#### Barbearia e Serviços

![screencapture-barber-lab-vercel-app-barbershops-8052c7e2-df2d-4966-a766-79e5f30d6c13-2025-07-09-15_13_28](https://github.com/user-attachments/assets/2e667385-1251-4e75-b58c-f03b26c098d4)

### Mobile

#### Início

![Home Page 02](https://github.com/user-attachments/assets/369fc544-64ce-4a54-b62e-5a1b0150c1ba)

#### Barbearias

![Buscar Categoria](https://github.com/user-attachments/assets/6caeff8d-31ee-4e3a-9c97-013f12772bce)

#### Agendamentos

![Agendamentos 01](https://github.com/user-attachments/assets/6a1cf25d-1219-4567-bd23-dd8e38a3e256)
![Fazer Reserva](https://github.com/user-attachments/assets/ab275df5-64cd-4871-a86b-8a643013b26c)

#### Barbearia e Serviços

![Barbearia](https://github.com/user-attachments/assets/4bbb7e82-1b25-4090-9208-cc27d71a528b)

## 🚀 Pré‑requisitos

- Node.js `^20.19`, `^22.12` ou `>=24`
- pnpm `10.34.5`
- PostgreSQL (Neon) via Prisma
- Configuração do Google Developer Console para autenticação

## ⚙️ Configuração local

1. Copie `.env.example` para `.env.local` e preencha as credenciais do Google.
2. Instale as dependências e gere o Prisma Client:

   ```bash
   pnpm install
   ```

3. Aplique as migrações no banco Postgres apontado por `DATABASE_URL`:

   ```bash
   pnpm exec prisma migrate deploy
   pnpm exec prisma generate
   ```

4. Inicie a aplicação:

   ```bash
   pnpm dev
   ```

O banco fica no Neon (não há arquivo local versionável); a `DATABASE_URL` é obrigatória até no build — sem ela o `prisma.config.ts` falha de propósito. Para cadastrar dados de demonstração, execute `pnpm exec prisma db seed` — o seed é idempotente (preenche até 10 barbearias com 6 serviços cada e não duplica o que já existe).

### 🔐 Login de teste (opcional, apenas ambiente local)

Para testar autenticação sem configurar o OAuth do Google, descomente no `.env.local`:

```bash
TEST_LOGIN_ENABLED=true
TEST_LOGIN_PASSWORD=<senha-de-teste-escolhida>
```

Com a flag ligada, o seed cria 3 contas de teste e o formulário de e-mail/senha da rota [`/login`](<../app/(customer)/login/page.tsx>) é habilitado (a senha é definida por `TEST_LOGIN_PASSWORD` e não fica no repositório). Sem a flag, a página continua existindo e mostra apenas o botão **Entrar com Google**:

| Conta               | Perfil                | Dados                                                         |
| ------------------- | --------------------- | ------------------------------------------------------------- |
| `cliente@teste.dev` | Cliente               | 3 reservas (dia do seed às 18:30, uma futura e uma concluída) |
| `vazio@teste.dev`   | Cliente               | **Zero reservas** — alimenta o teste de estado vazio          |
| `admin@teste.dev`   | Admin da 1ª barbearia | Painel, agenda, serviços e configurações                      |

⚠️ Nunca habilite `TEST_LOGIN_ENABLED` em produção: a action é inerte sem a flag, mas não tem rate limit próprio e é um bypass do Google OAuth. A flag apenas esconde/exibe o formulário — ela não é o que protege a action. Mais detalhes no [PRD §13](./PRD-Siltec-Barber.md).

## 🌐 Produção (Vercel + Neon)

Aplicação em execução: **<https://siltec-barber.vercel.app>**

| Item         | Valor                                                                                                          |
| ------------ | -------------------------------------------------------------------------------------------------------------- |
| Hospedagem   | Vercel — projeto `siltec-barber` (equipe `luciano-teles-freires-projects`), deploy automático da branch `main` |
| Repositório  | GitHub — `Freireteles-web-com-jsf2/Siltec-Barber`                                                              |
| Banco        | Neon (PostgreSQL) — mesmo banco do ambiente local                                                              |
| Domínio      | `siltec-barber.vercel.app`                                                                                     |
| Autenticação | Google OAuth — client `Cliente Web Barber` no projeto Cloud `siltec-braber`                                    |

### Variáveis de ambiente na Vercel

O projeto tem 5 variáveis configuradas (tipo **sensitive**, graváveis mas não legíveis de volta): `DATABASE_URL`, `NEXT_AUTH_SECRET`, `NEXTAUTH_URL`, `GOOGLE_CLIENT_ID` e `GOOGLE_CLIENT_SECRET`. Três cuidados:

1. **Alterações só valem para novos deployments** — depois de editar uma variável, faça um _Redeploy_.
2. **Sem `DATABASE_URL` o build falha de propósito** no `pnpm install` (`prepare` → `prisma generate` → `PrismaConfigEnvError`), em ~30 s.
3. **Nunca** defina `TEST_LOGIN_ENABLED`, `TEST_LOGIN_PASSWORD` ou `DEMO_MODE` na Vercel (RISK-021). As variáveis `silecbarber_*` vêm da integração Neon e são ignoradas pelo app — ele lê apenas `DATABASE_URL`.

### Redirect URIs do Google

Cadastradas no Console do Google (APIs e serviços → Credenciais → _Cliente Web Barber_):

```text
http://localhost:3000/api/auth/callback/google
https://siltec-barber.vercel.app/api/auth/callback/google
```

Sem a URI de produção o login falha com `redirect_uri_mismatch`. O Google avisa que a propagação pode levar de 5 minutos a algumas horas.

### Fluxo de deploy

1. Push na branch `main` → a Vercel instala dependências (`pnpm install`, que roda `prepare`), executa `next build` e publica.
2. Mudanças de schema exigem `pnpm exec prisma migrate deploy` no banco (Neon) **antes** do deploy que usa o schema novo.
3. O seed (`prisma db seed`) foi executado uma única vez no Neon; não reexecute em banco compartilhado com a flag de teste ligada.

## ✅ Verificações

```bash
pnpm lint                              # ESLint 9 (1 warning conhecido em barbershop-profile-form.tsx)
pnpm exec next typegen                 # tipos de rota do App Router
pnpm exec tsc --noEmit                 # TypeScript
pnpm exec prisma validate              # schema Prisma
pnpm exec prettier --check <arquivos>  # formatação (sem script global)
```

## 🧪 Testes E2E (TestSprite)

- **Plano:** [`testsprite_tests/testsprite_frontend_test_plan.json`](../testsprite_tests/testsprite_frontend_test_plan.json) — 45 cenários (TC001–TC035 cliente/público + TC036–TC045 admin).
- **Relatório:** [`testsprite_tests/testsprite-mcp-test-report.md`](../testsprite_tests/testsprite-mcp-test-report.md) — 3 lotes executados em 24–25/09/2026: **22 de 23 testes aprovados (95,7%)**.
- **Cobertura atual:** fluxo de reserva, perfil, lista de agendamentos (populado e vazio), páginas institucionais/busca/404 e as 4 telas do painel admin (`/dashboard`, `/schedule`, `/services`, `/settings`).
- **Pendência conhecida:** TC013 falha por sessão client-side defasada após o login de teste (causa raiz documentada no relatório); TC001 é provável falso-positivo por asserção fraca.
- Não há suíte de testes unitários/integração nem CI — ver [PRD §17](./PRD-Siltec-Barber.md).
