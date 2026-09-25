import asyncio
import re
from playwright import async_api
from playwright.async_api import expect

async def run_test():
    pw = None
    browser = None
    context = None

    try:
        # Start a Playwright session in asynchronous mode
        pw = await async_api.async_playwright().start()

        # Launch a Chromium browser in headless mode with custom arguments
        browser = await pw.chromium.launch(
            headless=True,
            args=[
                "--window-size=1280,720",
                "--disable-dev-shm-usage",
                "--ipc=host",
                "--single-process"
            ],
        )

        # Create a new browser context (like an incognito window)
        context = await browser.new_context()
        # Wider default timeout to match the agent's DOM-stability budget;
        # auto-waiting Playwright APIs (expect, locator.wait_for) inherit this.
        context.set_default_timeout(15000)

        # Open a new page in the browser context
        page = await context.new_page()

        # Interact with the page elements to simulate user flow
        # -> navigate
        await page.goto("http://localhost:3000")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Abrir a página 'Barbearias' (navegar para /barbershops) para procurar um link de barbearia inexistente ou tentar acessar uma URL inválida.
        await page.goto("http://localhost:3000/barbershops")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Navegar para a URL /barbershops/999999 e verificar se a página 'não encontrado' (404) é exibida.
        await page.goto("http://localhost:3000/barbershops/999999")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # --> Assertions to verify final state
        
        # --> Ao abrir /barbershops/999999, a aplicação exibe a página 'Erro 404 — Página não encontrada' com ações para 'Ver barbearias' e 'Voltar para o início'.
        await page.get_by_role("link", name="Ver barbearias").nth(0).scroll_into_view_if_needed()
        # Assert-outcome: passed
        # Assert: O botão 'Ver barbearias' está visível.
        await expect(page.get_by_role("link", name="Ver barbearias").nth(0)).to_be_visible(timeout=15000), "O bot\u00e3o 'Ver barbearias' est\u00e1 vis\u00edvel."
        await page.get_by_role("link", name="Voltar para o início").nth(0).scroll_into_view_if_needed()
        # Assert-outcome: passed
        # Assert: O botão 'Voltar para o início' está visível.
        await expect(page.get_by_role("link", name="Voltar para o início").nth(0)).to_be_visible(timeout=15000), "O bot\u00e3o 'Voltar para o in\u00edcio' est\u00e1 vis\u00edvel."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    