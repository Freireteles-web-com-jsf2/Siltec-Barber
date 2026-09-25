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
        
        # -> Open the login page by navigating to the 'Entrar' login route (http://localhost:3000/login).
        await page.goto("http://localhost:3000/login")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Fill the 'E-mail' field with cliente@teste.dev, fill the 'Senha' field with TesteBarber2026, and click the 'Entrar' button.
        # voce@exemplo.com email field
        elem = page.get_by_role("textbox", name="E-mail")
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("cliente@teste.dev")
        
        # -> Fill the 'E-mail' field with cliente@teste.dev, fill the 'Senha' field with TesteBarber2026, and click the 'Entrar' button.
        # •••••••• password field
        elem = page.get_by_role("textbox", name="Senha")
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("TesteBarber2026")
        
        # -> Fill the 'E-mail' field with cliente@teste.dev, fill the 'Senha' field with TesteBarber2026, and click the 'Entrar' button.
        # Entrar button
        elem = page.get_by_role("button", name="Entrar")
        await elem.click(timeout=10000)
        
        # -> Open the 'Perfil' page (the profile page that shows 'Meus dados') so the phone input and 'Salvar telefone' button can be verified.
        await page.goto("http://localhost:3000/perfil")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Fill the 'Telefone com WhatsApp' field with '(11) 98888-7777' and click the 'Salvar telefone' button.
        # (11) 99999-9999 tel field
        elem = page.get_by_role("textbox", name="Telefone com WhatsApp")
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("(11) 98888-7777")
        
        # -> Fill the 'Telefone com WhatsApp' field with '(11) 98888-7777' and click the 'Salvar telefone' button.
        # Salvar telefone button
        elem = page.get_by_role("button", name="Salvar telefone")
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> A confirmação de salvamento do telefone aparece com o texto 'Telefone salvo.'
        # Assert-outcome: passed
        # Assert: Verifica que o toast de confirmação mostra exatamente 'Telefone salvo.'
        await expect(page.locator("xpath=/html/body/section/ol/li").nth(0)).to_have_text("Telefone salvo.", timeout=15000), "Verifica que o toast de confirma\u00e7\u00e3o mostra exatamente 'Telefone salvo.'"
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    