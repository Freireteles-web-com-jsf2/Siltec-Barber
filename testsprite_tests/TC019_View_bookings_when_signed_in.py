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
        
        # -> Navigate to the login page ('Entrar') at /login.
        await page.goto("http://localhost:3000/login")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Fill the 'E-mail' field with cliente@teste.dev, fill the 'Senha' field with TesteBarber2026, then click the 'Entrar' button to submit the login form.
        # voce@exemplo.com email field
        elem = page.get_by_role("textbox", name="E-mail")
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("cliente@teste.dev")
        
        # -> Fill the 'E-mail' field with cliente@teste.dev, fill the 'Senha' field with TesteBarber2026, then click the 'Entrar' button to submit the login form.
        # •••••••• password field
        elem = page.get_by_role("textbox", name="Senha")
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("TesteBarber2026")
        
        # -> Fill the 'E-mail' field with cliente@teste.dev, fill the 'Senha' field with TesteBarber2026, then click the 'Entrar' button to submit the login form.
        # Entrar button
        elem = page.get_by_role("button", name="Entrar")
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> The browser is on the bookings page (redirected to /bookings).
        # Assert-outcome: passed
        # Assert: URL contains /bookings.
        await expect(page).to_have_url(re.compile("/bookings"), timeout=15000), "URL contains /bookings."
        
        # --> An upcoming confirmed booking is visible (Corte de Cabelo on setembro 24).
        await page.get_by_role("button", name="Confirmado Corte de Cabelo").nth(0).scroll_into_view_if_needed()
        # Assert-outcome: passed
        # Assert: The upcoming confirmed booking 'Corte de Cabelo' is visible.
        await expect(page.get_by_role("button", name="Confirmado Corte de Cabelo").nth(0)).to_be_visible(timeout=15000), "The upcoming confirmed booking 'Corte de Cabelo' is visible."
        
        # --> A past (finished) booking is visible in the history (Pézinho on setembro 17).
        await page.get_by_role("button", name="Finalizado Pézinho Barbearia").nth(0).scroll_into_view_if_needed()
        # Assert-outcome: passed
        # Assert: The finished booking 'Pézinho' is visible in the history.
        await expect(page.get_by_role("button", name="Finalizado Pézinho Barbearia").nth(0)).to_be_visible(timeout=15000), "The finished booking 'P\u00e9zinho' is visible in the history."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    