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
        
        # -> Open the login page and prepare to fill the 'E-mail' and 'Senha' fields to sign in as the admin.
        await page.goto("http://localhost:3000/login")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Fill the 'E-mail' field with admin@teste.dev, fill the 'Senha' field with TesteBarber2026, then click the 'Entrar' button.
        # voce@exemplo.com email field
        elem = page.get_by_role("textbox", name="E-mail")
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("admin@teste.dev")
        
        # -> Fill the 'E-mail' field with admin@teste.dev, fill the 'Senha' field with TesteBarber2026, then click the 'Entrar' button.
        # •••••••• password field
        elem = page.get_by_role("textbox", name="Senha")
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("TesteBarber2026")
        
        # -> Fill the 'E-mail' field with admin@teste.dev, fill the 'Senha' field with TesteBarber2026, then click the 'Entrar' button.
        # Entrar button
        elem = page.get_by_role("button", name="Entrar")
        await elem.click(timeout=10000)
        
        # -> Click the 'Agenda' link in the left sidebar to open the 'Gestão de horários' page.
        # Agenda link
        elem = page.get_by_role("link", name="Agenda")
        await elem.click(timeout=10000)
        
        # -> Click the 'Bloquear' button in the 'Bloqueios do dia' card to open the 'Bloquear horário' dialog.
        # Bloquear button
        elem = page.get_by_role("button", name="Bloquear")
        await elem.click(timeout=10000)
        
        # -> Click the 'Almoço' preset button, then click the 'Bloquear' confirm button to create the 12:00–13:00 block for today.
        # Almoço button
        elem = page.get_by_role("button", name="Almoço")
        await elem.click(timeout=10000)
        
        # -> Click the 'Almoço' preset button, then click the 'Bloquear' confirm button to create the 12:00–13:00 block for today.
        # Bloquear button
        elem = page.get_by_role("button", name="Bloquear")
        await elem.click(timeout=10000)
        
        # -> Click the 'Remover bloqueio' (trash) button on the block in the 'Bloqueios do dia' card to remove the block.
        # Remover bloqueio button
        elem = page.get_by_role("button", name="Remover bloqueio")
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> A notificação de sucesso 'Bloqueio removido.' é exibida após remover o bloqueio.
        # Assert-outcome: passed
        # Assert: Verifica que a notificação 'Bloqueio removido.' aparece.
        await expect(page.locator("xpath=/html/body/section/ol/li").nth(0)).to_have_text("Bloqueio removido.", timeout=15000), "Verifica que a notifica\u00e7\u00e3o 'Bloqueio removido.' aparece."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    