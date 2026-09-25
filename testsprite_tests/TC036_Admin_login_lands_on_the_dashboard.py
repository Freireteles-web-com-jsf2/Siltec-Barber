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
        
        # -> Open the login page by navigating to /login (the page with the 'Entrar' login form).
        await page.goto("http://localhost:3000/login")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Fill the 'E-mail' field with admin@teste.dev, fill the 'Senha' field with TesteBarber2026, then click the 'Entrar' button to submit the login form.
        # voce@exemplo.com email field
        elem = page.get_by_role("textbox", name="E-mail")
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("admin@teste.dev")
        
        # -> Fill the 'E-mail' field with admin@teste.dev, fill the 'Senha' field with TesteBarber2026, then click the 'Entrar' button to submit the login form.
        # •••••••• password field
        elem = page.get_by_role("textbox", name="Senha")
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("TesteBarber2026")
        
        # -> Fill the 'E-mail' field with admin@teste.dev, fill the 'Senha' field with TesteBarber2026, then click the 'Entrar' button to submit the login form.
        # Entrar button
        elem = page.get_by_role("button", name="Entrar")
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> After login the browser is on the dashboard page (URL contains /dashboard).
        # Assert-outcome: passed
        # Assert: The URL contains '/dashboard'.
        await expect(page).to_have_url(re.compile("/dashboard"), timeout=15000), "The URL contains '/dashboard'."
        
        # --> The four top metric cards (Agendamentos, Faturamento previsto, Concluídos, Faltas e cancelamentos) are visible on the dashboard.
        await page.locator(".w-fit").first.nth(0).scroll_into_view_if_needed()
        # Assert-outcome: passed
        # Assert: The first metric card (Agendamentos) is visible.
        await expect(page.locator(".w-fit").first.nth(0)).to_be_visible(timeout=15000), "The first metric card (Agendamentos) is visible."
        await page.locator("div:nth-child(2) > .flex > .w-fit").first.nth(0).scroll_into_view_if_needed()
        # Assert-outcome: passed
        # Assert: The second metric card (Faturamento previsto) is visible.
        await expect(page.locator("div:nth-child(2) > .flex > .w-fit").first.nth(0)).to_be_visible(timeout=15000), "The second metric card (Faturamento previsto) is visible."
        
        # --> The 'Atendimentos do dia' area is present — a seeded appointment with action buttons is visible.
        await page.get_by_role("button", name="Concluir").nth(0).scroll_into_view_if_needed()
        # Assert-outcome: passed
        # Assert: An appointment action button (Concluir) is visible, indicating the 'Atendimentos do dia' section is present.
        await expect(page.get_by_role("button", name="Concluir").nth(0)).to_be_visible(timeout=15000), "An appointment action button (Concluir) is visible, indicating the 'Atendimentos do dia' section is present."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    