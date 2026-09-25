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
        
        # -> Open the login page, fill the 'E-mail' field with admin@teste.dev and 'Senha' with TesteBarber2026, then click the 'Entrar' button to sign in.
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
        
        # -> Click the 'Serviços' link in the sidebar to open the Services page.
        # Serviços link
        elem = page.get_by_role("link", name="Serviços")
        await elem.click(timeout=10000)
        
        # -> Click the 'Desativar serviço' switch on the 'Sobrancelha' card to deactivate the service.
        # Desativar serviço button
        elem = page.locator("div").filter(has_text=re.compile(r"^Sobrancelha$")).get_by_label("Desativar serviço")
        await elem.click(timeout=10000)
        
        # -> Click the 'Ativar serviço' switch on the 'Sobrancelha' service card to reactivate it and observe the activation toast.
        # Ativar serviço button
        elem = page.get_by_role("switch", name="Ativar serviço", exact=True)
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> The 'Sobrancelha' service was reactivated: the 'Serviço ativado.' toast appeared and the service switch is active.
        # Assert-outcome: passed
        # Assert: Toast 'Serviço ativado.' is visible in the notifications list.
        await expect(page.locator("xpath=/html/body/section/ol/li").nth(0)).to_have_text("Servi\u00e7o ativado.", timeout=15000), "Toast 'Servi\u00e7o ativado.' is visible in the notifications list."
        # Assert-outcome: passed
        # Assert: The Sobrancelha service switch shows the active state via its aria-label.
        await expect(page.locator("div").filter(has_text=re.compile(r"^Sobrancelha$")).get_by_label("Desativar serviço").nth(0)).to_have_attribute("aria-label", "Desativar servi\u00e7o", timeout=15000), "The Sobrancelha service switch shows the active state via its aria-label."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    