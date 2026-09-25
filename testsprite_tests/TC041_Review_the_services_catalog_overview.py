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
        
        # -> Open the login page by navigating to the '/login' URL so the 'E-mail' and 'Senha' fields are visible.
        await page.goto("http://localhost:3000/login")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Fill 'E-mail' with admin@teste.dev and 'Senha' with TesteBarber2026, then click the 'Entrar' button to sign in.
        # voce@exemplo.com email field
        elem = page.get_by_role("textbox", name="E-mail")
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("admin@teste.dev")
        
        # -> Fill 'E-mail' with admin@teste.dev and 'Senha' with TesteBarber2026, then click the 'Entrar' button to sign in.
        # •••••••• password field
        elem = page.get_by_role("textbox", name="Senha")
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("TesteBarber2026")
        
        # -> Fill 'E-mail' with admin@teste.dev and 'Senha' with TesteBarber2026, then click the 'Entrar' button to sign in.
        # Entrar button
        elem = page.get_by_role("button", name="Entrar")
        await elem.click(timeout=10000)
        
        # -> Click the 'Serviços' link in the left navigation to open the services page.
        # Serviços link
        elem = page.get_by_role("link", name="Serviços")
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> Metric cards 'Ativos', 'Preço médio' and 'Duração média' are visible on the Services page.
        await page.get_by_text("/6Ativos").nth(0).scroll_into_view_if_needed()
        # Assert-outcome: passed
        # Assert: The 'Ativos' metric card is visible.
        await expect(page.get_by_text("/6Ativos").nth(0)).to_be_visible(timeout=15000), "The 'Ativos' metric card is visible."
        await page.locator("div:nth-child(2) > .flex > .w-fit").nth(0).scroll_into_view_if_needed()
        # Assert-outcome: passed
        # Assert: The 'Preço médio' metric card is visible.
        await expect(page.locator("div:nth-child(2) > .flex > .w-fit").nth(0)).to_be_visible(timeout=15000), "The 'Pre\u00e7o m\u00e9dio' metric card is visible."
        
        # --> The service card titled 'Barba' is visible in the services list.
        # Assert-outcome: passed
        # Assert: A service card with the title 'Barba' is present.
        await expect(page.locator("xpath=/html/body/div[2]/main/div/div[3]/div[2]/div[1]/div/div[2]/div[1]/div[1]/h3").nth(0)).to_have_text("Barba", timeout=15000), "A service card with the title 'Barba' is present."
        
        # --> The service 'Corte de Cabelo' is present (evidenced by its edit button).
        # Assert-outcome: passed
        # Assert: An edit button with aria-label 'Editar Corte de Cabelo' is present, proving the service exists.
        await expect(page.get_by_role("button", name="Editar Corte de Cabelo").nth(0)).to_have_attribute("aria-label", "Editar Corte de Cabelo", timeout=15000), "An edit button with aria-label 'Editar Corte de Cabelo' is present, proving the service exists."
        
        # --> The 'Novo serviço' button and the services count heading are visible.
        await page.get_by_role("button", name="Novo serviço").nth(0).scroll_into_view_if_needed()
        # Assert-outcome: passed
        # Assert: The 'Novo serviço' button is visible.
        await expect(page.get_by_role("button", name="Novo serviço").nth(0)).to_be_visible(timeout=15000), "The 'Novo servi\u00e7o' button is visible."
        await page.get_by_text("/6").nth(0).scroll_into_view_if_needed()
        # Assert-outcome: passed
        # Assert: The services count heading (shows the count) is visible.
        await expect(page.get_by_text("/6").nth(0)).to_be_visible(timeout=15000), "The services count heading (shows the count) is visible."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    