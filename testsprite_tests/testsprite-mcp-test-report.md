# Relatório de Testes TestSprite AI (MCP)

---

## 1️⃣ Metadados do Documento

- **Nome do Projeto:** Siltec-Barber
- **Data:** 2026-09-25 (última atualização)
- **Preparado por:** Equipe TestSprite AI

**Contexto das execuções (reexecução com autenticação de teste + lote administrativo + correção do TC018)**

| Item               | Valor                                                                                                             |
| ------------------ | ----------------------------------------------------------------------------------------------------------------- |
| Tipo de teste      | Frontend (Playwright)                                                                                             |
| Modo do servidor   | Produção (`pnpm build` + `pnpm start`)                                                                            |
| URL base           | `http://localhost:3000`                                                                                           |
| Login no plano     | Habilitado (`needLogin=true`), rota de teste `/login` com credenciais de e-mail/senha                             |
| Lote 1 (24/09)     | 8 testes reexecutados (TC001, TC013, TC015, TC018, TC019, TC021, TC022, TC023) — status: 6 ✅ / 1 ❌ / 1 ⛔ (75%) |
| Lote 2 (24/09)     | 15 testes (TC031–TC035 públicos + TC036–TC045 administrativos novos) — status: 15 ✅ (100%)                       |
| Lote 3 (25/09)     | Reexecução do TC018 com conta isolada sem reservas (`vazio@teste.dev`) — status: 1 ✅ (100%)                      |
| Total              | 24 execuções / 23 testes únicos: 22 aprovados, 1 falha, 0 bloqueados (95,7%)                                      |
| Créditos restantes | 125 (plano Free)                                                                                                  |

> A senha de teste não é reproduzida neste relatório; as credenciais ficam em `.env.local` (flags `TEST_LOGIN_ENABLED`/`TEST_LOGIN_PASSWORD`) e a página `/login` exibe apenas os usuários como dica.

---

## 2️⃣ Resumo de Validação dos Requisitos

### Requisito: Fluxo de reserva (cliente autenticado)

- **Descrição:** O cliente entra pela rota de teste, escolhe barbearia/serviço, data e horário futuros e confirma a reserva.

#### Teste TC001 Criar uma reserva a partir da página de detalhe da barbearia

- **Código do Teste:** [TC001_Create_a_booking_from_a_barbershop_detail_page.py](./TC001_Create_a_booking_from_a_barbershop_detail_page.py)
- **Visualização e Resultado:** https://www.testsprite.com/dashboard/mcp/tests/1d908d08-75c7-5ac1-ba41-996ea6ee73eb/test/6d867f00-efe3-44d0-b44e-e444dd7bba86
- **Status:** ✅ Aprovado (com ressalva)
- **Severidade:** MÉDIA
- **Análise / Constatações:** Aprovado pelo juiz de IA, mas com asserção fraca (apenas "a página carregou com uma URL"). O código do teste registra a mesma luta contra o modal "Faça login na plataforma" vista no TC013, e a verificação posterior no banco confirma que **nenhuma reserva foi criada por este teste** (a contagem de confirmados só mudou quando o TC022 removeu a reserva semeada de hoje). Provável falso-positivo — reexecutar com asserção de sucesso real (toast "Reserva criada com sucesso!" ou linha nova em "Próximos Agendamentos").

---

### Requisito: Entrada no fluxo de reserva

- **Descrição:** Após autenticar, clicar em "Reservar" deve abrir a folha de reserva, não o diálogo de login.

#### Teste TC013 Abrir o fluxo de reserva após login a partir da página da barbearia

- **Código do Teste:** [TC013_Open_the_booking_flow_after_login_from_a_barbershop_page.py](./TC013_Open_the_booking_flow_after_login_from_a_barbershop_page.py)
- **Erro do Teste:** TEST FAILURE — modal "Faça login na plataforma" persistiu e bloqueou o botão "Reservar"; tentativas de fechar (botão Close e Escape) não resolveram.
- **Visualização e Resultado:** https://www.testsprite.com/dashboard/mcp/tests/1d908d08-75c7-5ac1-ba41-996ea6ee73eb/test/0bbefae5-30be-4734-a555-ebc712fd641e
- **Status:** ❌ Falhou
- **Severidade:** MÉDIA
- **Análise / Constatações:** Causa raiz identificada por reprodução manual: o login `/login` (server action) redireciona por navegação soft, e o `SessionProvider` do NextAuth client não refetcha imediatamente — em ambiente headless (sem eventos de focus) `useSession()` segue com `data` undefined, e `ServiceItem.handleBookingClick` trata isso como "sem sessão", abrindo o diálogo que só oferece Google. No navegador desktop o mesmo fluxo funciona (o focus dispara o refetch e a folha "Fazer Reserva" abre). O OAuth real do Google não sofre desse problema (redirect cross-origin recarrega a página). Correção sugerida: forçar navegação full-page após o login de teste e/ou tratar `status === "loading"` em `handleBookingClick` em vez de apenas `data?.user`.

---

### Requisito: Perfil do cliente

- **Descrição:** O cliente visualiza e salva o telefone de contato no perfil.

#### Teste TC015 Ver e salvar telefone de contato no perfil

- **Código do Teste:** [TC015_View_and_save_contact_phone_on_profile.py](./TC015_View_and_save_contact_phone_on_profile.py)
- **Visualização e Resultado:** https://www.testsprite.com/dashboard/mcp/tests/1d908d08-75c7-5ac1-ba41-996ea6ee73eb/test/cde29767-416a-43dc-a87c-788dd95013f2
- **Status:** ✅ Aprovado
- **Severidade:** BAIXA
- **Análise / Constatações:** Login, navegação ao perfil e salvamento funcionam; o toast exato "Telefone salvo." foi verificado.

---

#### Teste TC023 Atualizar o telefone de contato no perfil

- **Código do Teste:** [TC023_Update_the_contact_phone_in_the_profile.py](./TC023_Update_the_contact_phone_in_the_profile.py)
- **Visualização e Resultado:** https://www.testsprite.com/dashboard/mcp/tests/1d908d08-75c7-5ac1-ba41-996ea6ee73eb/test/ff284735-5ff5-4e6d-bc5d-be78725ed5fb
- **Status:** ✅ Aprovado
- **Severidade:** BAIXA
- **Análise / Constatações:** Atualização persiste: o campo "Telefone com WhatsApp" mostra o novo valor após o salvamento.

---

### Requisito: Lista de agendamentos do cliente

- **Descrição:** Estados vazio e populado de "Meus Agendamentos", com resumo de futuros/passados.

#### Teste TC018 Ver estado vazio de agendamentos após login

- **Código do Teste:** [TC018_See_empty_bookings_state_when_there_are_no_bookings.py](./TC018_See_empty_bookings_state_when_there_are_no_bookings.py)
- **Visualização e Resultado:** https://www.testsprite.com/dashboard/mcp/tests/1d908d08-75c7-5ac1-ba41-996ea6ee73eb/test/8de5e3aa-2bdb-425c-bb70-d1e471ab8de0
- **Status:** ✅ Aprovado (reexecutado em 2026-09-25)
- **Severidade:** BAIXA
- **Análise / Constatações:** Na primeira execução (24/09) o teste ficou **Bloqueado** porque exigia uma conta sem reservas e a conta semeada tinha reservas. **Correção aplicada:** o seed (sob a flag `TEST_LOGIN_ENABLED`) passou a criar a conta isolada `vazio@teste.dev` (cliente, zero reservas) e o passo de login do teste foi apontado para ela. Reexecutado, o teste autenticou em `/login`, acessou `/bookings` e validou o estado vazio: heading "Nenhum agendamento encontrado", ausência do painel de estatísticas e das seções "Próximos Agendamentos"/"Histórico de Agendamentos", e o CTA "Agendar Agora" visível com `href="/barbershops"` — link que **só é renderizado dentro do cartão de estado vazio**, o que torna a asserção forte. Observação de qualidade: a asserção do heading no código gerado usou um seletor de classe (`.bg-primary\/10`) em vez do texto, sendo fraca por si só; as asserções do CTA compensam. Verificação manual prévia no navegador desktop confirmou o mesmo resultado.

---

#### Teste TC019 Ver agendamentos quando autenticado

- **Código do Teste:** [TC019_View_bookings_when_signed_in.py](./TC019_View_bookings_when_signed_in.py)
- **Visualização e Resultado:** https://www.testsprite.com/dashboard/mcp/tests/1d908d08-75c7-5ac1-ba41-996ea6ee73eb/test/864112c5-52bc-4ab2-bec8-79cd26aca03f
- **Status:** ✅ Aprovado
- **Severidade:** BAIXA
- **Análise / Constatações:** Redireciona para `/bookings` e exibe a reserva confirmada ("Corte de Cabelo") e a finalizada ("Pézinho") corretamente.

---

#### Teste TC021 Revisar resumo de agendamentos futuros e passados

- **Código do Teste:** [TC021_Review_upcoming_and_past_bookings_summary.py](./TC021_Review_upcoming_and_past_bookings_summary.py)
- **Visualização e Resultado:** https://www.testsprite.com/dashboard/mcp/tests/1d908d08-75c7-5ac1-ba41-996ea6ee73eb/test/62b3de56-d62b-41ab-945e-d8dcf57cc62e
- **Status:** ✅ Aprovado
- **Severidade:** BAIXA
- **Análise / Constatações:** Cartões de futuros ("Corte de Cabelo", "Barba"), histórico ("Pézinho") e o cartão "Total Investido" estão visíveis.

---

#### Teste TC022 Remover um agendamento da lista

- **Código do Teste:** [TC022_Remove_a_booking_from_bookings.py](./TC022_Remove_a_booking_from_bookings.py)
- **Visualização e Resultado:** https://www.testsprite.com/dashboard/mcp/tests/1d908d08-75c7-5ac1-ba41-996ea6ee73eb/test/7b39c723-ecd9-4b30-b23a-691080fe6fdb
- **Status:** ✅ Aprovado
- **Severidade:** MÉDIA
- **Análise / Constatações:** O cancelamento via diálogo ("Cancelar Reserva" → "Confirmar") funciona e a remoção é observável no banco (a reserva semeada de hoje desapareceu da lista — restaurada depois para os testes do admin). Risco conhecido: `deleteBooking` faz **hard delete** (não define `CANCELED`), sem histórico/auditoria do cancelamento; a asserção do teste também é fraca (verifica apenas que há URL).

---

### Requisito: Páginas institucionais e busca pública

- **Descrição:** Visitantes acessam páginas estáticas, o telefone de contato, o estado vazio de busca e a página 404, sem autenticação.

#### Teste TC031 Ver as páginas institucionais

- **Código do Teste:** [TC031_View_the_institutional_pages.py](./TC031_View_the_institutional_pages.py)
- **Visualização e Resultado:** https://www.testsprite.com/dashboard/mcp/tests/1d908d08-75c7-5ac1-ba41-996ea6ee73eb/test/d9a43113-f757-4af4-9324-0723d5c12ddf
- **Status:** ✅ Aprovado
- **Severidade:** BAIXA
- **Análise / Constatações:** `/sobre`, `/contato` e `/termos` renderizam o conteúdo esperado para visitantes anônimos.

---

#### Teste TC033 Ler as páginas institucionais do site

- **Código do Teste:** [TC033_Read_the_institutional_pages_from_the_site.py](./TC033_Read_the_institutional_pages_from_the_site.py)
- **Visualização e Resultado:** https://www.testsprite.com/dashboard/mcp/tests/1d908d08-75c7-5ac1-ba41-996ea6ee73eb/test/b3375716-fb86-46bf-b3ff-18e296c21e4d
- **Status:** ✅ Aprovado
- **Severidade:** BAIXA
- **Análise / Constatações:** `/sobre`, `/carreiras`, `/parceiros`, `/privacidade`, `/termos` e `/cookies` acessíveis e legíveis.

---

#### Teste TC032 Abrir um contato telefônico da barbearia

- **Código do Teste:** [TC032_Abrir_um_contato_telefnico_da_barbearia.py](./TC032_Abrir_um_contato_telefnico_da_barbearia.py)
- **Visualização e Resultado:** https://www.testsprite.com/dashboard/mcp/tests/1d908d08-75c7-5ac1-ba41-996ea6ee73eb/test/067b14c0-635f-4704-8ec0-00129640b859
- **Status:** ✅ Aprovado
- **Severidade:** BAIXA
- **Análise / Constatações:** A opção de telefone (link `tel:`/WhatsApp) está disponível na página de detalhe da barbearia.

---

#### Teste TC034 Mostrar estado vazio quando nenhuma barbearia corresponde

- **Código do Teste:** [TC034_Show_an_empty_state_when_no_barbershops_match.py](./TC034_Show_an_empty_state_when_no_barbershops_match.py)
- **Visualização e Resultado:** https://www.testsprite.com/dashboard/mcp/tests/1d908d08-75c7-5ac1-ba41-996ea6ee73eb/test/b4e05315-b74c-4aed-a923-fb114183a41b
- **Status:** ✅ Aprovado
- **Severidade:** BAIXA
- **Análise / Constatações:** Busca sem correspondência exibe o estado vazio e nenhum cartão de barbearia.

---

#### Teste TC035 Exibir a página 404 para barbearia inexistente

- **Código do Teste:** [TC035_Exibir_a_pgina_404_para_barbearia_inexistente.py](./TC035_Exibir_a_pgina_404_para_barbearia_inexistente.py)
- **Visualização e Resultado:** https://www.testsprite.com/dashboard/mcp/tests/1d908d08-75c7-5ac1-ba41-996ea6ee73eb/test/172c3c6b-726e-448b-b048-7529cd787b4f
- **Status:** ✅ Aprovado
- **Severidade:** BAIXA
- **Análise / Constatações:** Rota de barbearia com identificador inválido exibe a página 404/not-found em vez de erro 500.

---

### Requisito: Dashboard administrativo

- **Descrição:** O admin autenticado acessa `/dashboard`, vê a saudação, as métricas do dia, navega entre dias e a agenda com ações de atendimento.

#### Teste TC036 Login do admin aterra no dashboard

- **Código do Teste:** [TC036_Admin_login_lands_on_the_dashboard.py](./TC036_Admin_login_lands_on_the_dashboard.py)
- **Visualização e Resultado:** https://www.testsprite.com/dashboard/mcp/tests/1d908d08-75c7-5ac1-ba41-996ea6ee73eb/test/9f7d0c12-fad7-40e0-9467-07a0c42fae3b
- **Status:** ✅ Aprovado
- **Severidade:** BAIXA
- **Análise / Constatações:** Login de `admin@teste.dev` redireciona para `/dashboard` com a saudação "Olá, Admin!", os 4 cartões de métricas ("Agendamentos", "Faturamento previsto", "Concluídos", "Faltas e cancelamentos") e a seção "Atendimentos do dia". O `requireBarbershopAdmin` concede acesso correto e o OnboardingTour não aparece (`onboardingDoneAt` definido no seed).

---

#### Teste TC037 Navegar entre dias no dashboard do admin

- **Código do Teste:** [TC037_Navigate_between_days_on_the_admin_dashboard.py](./TC037_Navigate_between_days_on_the_admin_dashboard.py)
- **Visualização e Resultado:** https://www.testsprite.com/dashboard/mcp/tests/1d908d08-75c7-5ac1-ba41-996ea6ee73eb/test/28358dc3-530d-42e3-96e6-9f2bcfb1d0d7
- **Status:** ✅ Aprovado
- **Severidade:** BAIXA
- **Análise / Constatações:** "Próximo dia" muda o título para o eyebrow "Visão do dia" e "Hoje" volta à saudação de hoje — o `DayNavigator` funciona nos dois sentidos.

---

#### Teste TC038 Ver o atendimento de hoje com ações de status

- **Código do Teste:** [TC038_See_todays_appointment_with_status_actions.py](./TC038_See_todays_appointment_with_status_actions.py)
- **Visualização e Resultado:** https://www.testsprite.com/dashboard/mcp/tests/1d908d08-75c7-5ac1-ba41-996ea6ee73eb/test/4d91ff44-3c6f-4e79-8c68-cf6bdb5fc0d9
- **Status:** ✅ Aprovado
- **Severidade:** BAIXA
- **Análise / Constatações:** A linha da reserva semeada ("Corte de Cabelo" 18:30, cliente "Cliente Teste") aparece em "Atendimentos do dia" com o badge "Confirmado" e os botões "Concluir", "Faltou" e "Cancelar" (apenas visibilidade, sem clique, para não alterar dados).

---

### Requisito: Agenda administrativa

- **Descrição:** A página `/schedule` mostra calendário, gerenciador de bloqueios e a linha do tempo do dia; o admin cria e remove bloqueios.

#### Teste TC039 Ver a linha do tempo da página de agenda

- **Código do Teste:** [TC039_View_the_schedule_page_timeline.py](./TC039_View_the_schedule_page_timeline.py)
- **Visualização e Resultado:** https://www.testsprite.com/dashboard/mcp/tests/1d908d08-75c7-5ac1-ba41-996ea6ee73eb/test/00a2efca-86bd-452b-bcbe-39e2f845a01a
- **Status:** ✅ Aprovado
- **Severidade:** BAIXA
- **Análise / Constatações:** Título "Gestão de horários", calendário mensal, cartão "Bloqueios do dia" com botão "Bloquear" e a linha do tempo com a reserva das 18:30 e nome do cliente.

---

#### Teste TC040 Criar e remover um bloqueio de agenda

- **Código do Teste:** [TC040_Create_and_remove_a_schedule_block.py](./TC040_Create_and_remove_a_schedule_block.py)
- **Visualização e Resultado:** https://www.testsprite.com/dashboard/mcp/tests/1d908d08-75c7-5ac1-ba41-996ea6ee73eb/test/fd03c2c2-0388-4f85-a054-2fcf8f69eb99
- **Status:** ✅ Aprovado
- **Severidade:** BAIXA
- **Análise / Constatações:** Fluxo completo passou: preset "Almoço" preenche 12:00–13:00, toast "Horário bloqueado.", cartão do bloqueio listado, remoção com toast "Bloqueio removido." e volta ao estado vazio "Nenhum bloqueio nesse dia.". Verificação pós-teste: 0 bloqueios no banco (nenhuma sobra).

---

### Requisito: Catálogo de serviços (admin)

- **Descrição:** O admin vê as métricas do catálogo, cria, edita, desativa/reativa e exclui serviços.

#### Teste TC041 Revisar a visão geral do catálogo de serviços

- **Código do Teste:** [TC041_Review_the_services_catalog_overview.py](./TC041_Review_the_services_catalog_overview.py)
- **Visualização e Resultado:** https://www.testsprite.com/dashboard/mcp/tests/1d908d08-75c7-5ac1-ba41-996ea6ee73eb/test/fb1385ac-d85e-44c5-862c-6ea572563f41
- **Status:** ✅ Aprovado
- **Severidade:** BAIXA
- **Análise / Constatações:** Título "Serviços" + eyebrow "Catálogo", cartões "Ativos"/"Preço médio"/"Duração média", cards de serviço com preço ("Corte de Cabelo", "Barba") e botões "Novo serviço"/contagem.

---

#### Teste TC042 Criar e depois excluir um serviço

- **Código do Teste:** [TC042_Create_and_then_delete_a_service.py](./TC042_Create_and_then_delete_a_service.py)
- **Visualização e Resultado:** https://www.testsprite.com/dashboard/mcp/tests/1d908d08-75c7-5ac1-ba41-996ea6ee73eb/test/39c1b089-28dc-4fb0-a66c-f48bc69dc470
- **Status:** ✅ Aprovado
- **Severidade:** BAIXA
- **Análise / Constatações:** CRUD completo passou: diálogo "Novo serviço" → toast "Serviço criado." → card "Corte Teste Sprite" listado → diálogo "Excluir Corte Teste Sprite?" → toast "Serviço excluído." → card removido. Verificação pós-teste: banco com 6 serviços, sem sobras.

---

#### Teste TC043 Desativar e reativar um serviço

- **Código do Teste:** [TC043_Deactivate_and_reactivate_a_service.py](./TC043_Deactivate_and_reactivate_a_service.py)
- **Visualização e Resultado:** https://www.testsprite.com/dashboard/mcp/tests/1d908d08-75c7-5ac1-ba41-996ea6ee73eb/test/bafed4fd-4bb6-498c-ba2e-d7156c9eb5d1
- **Status:** ✅ Aprovado
- **Severidade:** BAIXA
- **Análise / Constatações:** Switch do card "Sobrancelha": toasts "Serviço desativado." (card escurece) e "Serviço ativado." ao reativar. Verificação pós-teste: Sobrancelha `isActive: true` (estado restaurado).

---

### Requisito: Configurações da barbearia (admin)

- **Descrição:** O admin salva os dados da barbearia e os horários de funcionamento em `/settings`.

#### Teste TC044 Salvar o perfil da barbearia nas configurações

- **Código do Teste:** [TC044_Save_the_barbershop_profile_in_settings.py](./TC044_Save_the_barbershop_profile_in_settings.py)
- **Visualização e Resultado:** https://www.testsprite.com/dashboard/mcp/tests/1d908d08-75c7-5ac1-ba41-996ea6ee73eb/test/2f1d0f3b-acde-4f43-a5fc-380e556ae88c
- **Status:** ✅ Aprovado
- **Severidade:** BAIXA
- **Análise / Constatações:** Seção "Dados da barbearia" com nome pré-preenchido "Barbearia Vintage", campos de telefone e botão "Salvar dados"; toast "Dados da barbearia salvos." confirmou a persistência.

---

#### Teste TC045 Salvar os horários de funcionamento nas configurações

- **Código do Teste:** [TC045_Save_the_opening_hours_in_settings.py](./TC045_Save_the_opening_hours_in_settings.py)
- **Visualização e Resultado:** https://www.testsprite.com/dashboard/mcp/tests/1d908d08-75c7-5ac1-ba41-996ea6ee73eb/test/1b09026f-55c5-4fde-b489-faf6b2892b6c
- **Status:** ✅ Aprovado
- **Severidade:** BAIXA
- **Análise / Constatações:** Seção "Horário de funcionamento" com as 7 linhas de dias (Domingo..Sábado) e inputs de horário; toast "Horário de funcionamento salvo." ao salvar.

---

## 3️⃣ Métricas de Cobertura e Correspondência

- **Geral: 95,7%** — 22 aprovados de 23 testes únicos (24 execuções; 1 falha, 0 bloqueados após a reexecução)
- **Lote 1: 75,0%** (6 de 8)
- **Lote 2: 100,0%** (15 de 15)
- **Lote 3 (reexecução do TC018): 100,0%** (1 de 1)

| Requisito                                            | Total  | ✅ Aprovados | ❌ Falhas | ⛔ Bloqueados |
| ---------------------------------------------------- | ------ | ------------ | --------- | ------------- |
| Fluxo de reserva (TC001, TC013)                      | 2      | 1*           | 1         | 0             |
| Perfil do cliente (TC015, TC023)                     | 2      | 2            | 0         | 0             |
| Lista de agendamentos (TC018, TC019, TC021, TC022)   | 4      | 4            | 0         | 0             |
| Páginas institucionais e busca pública (TC031–TC035) | 5      | 5            | 0         | 0             |
| Dashboard administrativo (TC036–TC038)               | 3      | 3            | 0         | 0             |
| Agenda administrativa (TC039, TC040)                 | 2      | 2            | 0         | 0             |
| Catálogo de serviços admin (TC041–TC043)             | 3      | 3            | 0         | 0             |
| Configurações admin (TC044, TC045)                   | 2      | 2            | 0         | 0             |
| **Total**                                            | **23** | **22**       | **1**     | **0**         |

\* TC001 aprovado com ressalva: asserção fraca e nenhuma reserva criada (provável falso-positivo).

> O TC018 conta como aprovado: a primeira execução (24/09) ficou bloqueada por falta de conta sem reservas e a reexecução (25/09), após a correção, passou.

---

## 4️⃣ Principais Lacunas / Riscos

> 95,7% dos testes únicos aprovaram; a única falha (TC013) tem causa raiz identificada, e o bloqueio do TC018 foi **resolvido** com a conta isolada e reexecutado com sucesso. O lote administrativo (10 testes cobrindo `/dashboard`, `/schedule`, `/services`, `/settings`) passou 100% sem deixar dados residuais.

1. **Sessão client-side defasada pós-login (causa da falha do TC013 e do provável falso-positivo do TC001):** o `SessionProvider` do NextAuth não refetcha após o redirect soft do server action do `/login`; em headless `useSession()` fica `undefined` e `ServiceItem` abre o diálogo Google-only. Correção sugerida: navegação full-page (`window.location`) após o login de teste e tratar `status === "loading"` em `handleBookingClick` em vez de `data?.user`.
2. **Diálogo de login só oferece Google:** o `SignInDialog` não tem link para `/login` — beco sem saída para credenciais (irrelevante no fluxo real Google, mas deve ser revisto se credenciais virarem produto).
3. ~~**TC018 (estado vazio) requer conta isolada sem reservas**~~ — **RESOLVIDO em 25/09:** o seed cria `vazio@teste.dev` (cliente, zero reservas) sob a flag `TEST_LOGIN_ENABLED`; o TC018 foi reexecutado e aprovado. A dica da página `/login` agora lista as 3 contas de teste.
4. **Asserções fracas em TC001/TC022** (checagem de URL): aprovam sem validar o resultado real; TC001 passou sem criar reserva. Reforçar com asserções de toast/linha na lista. No código gerado do TC018, a asserção do heading usou seletor de classe (`.bg-primary\/10`) em vez do texto — compensada pelas asserções do CTA "Agendar Agora", que só existe no estado vazio.
5. **Efeitos colaterais em banco compartilhado:** o TC022 removeu por hard delete a reserva semeada de hoje 18:30 (restaurada manualmente para o lote administrativo); testes destrutivos do lote 2 (criar/excluir serviço, criar/remover bloqueio, desativar/ativar serviço) deixaram o banco limpo — verificado: 6 serviços, 0 bloqueios, Sobrancelha ativa. A reexecução do TC018 não altera dados (conta sem reservas).
6. **`deleteBooking` faz hard delete** (risco conhecido e reconfirmado): cancelamentos não deixam rastro `CANCELED` no histórico.
7. **Ordem de execução importa:** os testes não são isolados entre si (o TC018 bloqueou por causa do seed; o TC022 afetou a agenda do admin). Mitigação parcial: agora existe conta dedicada por cenário para estado vazio — considerar contas dedicadas também para cenários populados em execuções paralelas futuras.
8. **Cobertura restante não executada:** o plano tem 45 testes; 23 foram executados neste relatório. Os testes de cliente do plano regenerado (ex.: TC026 prevenir data passada, TC029 conflito de horário) e os antigos não executados da primeira rodada continuam disponíveis para lotes futuros (créditos: 125).
