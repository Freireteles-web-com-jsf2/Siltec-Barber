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
        
        # -> Click the 'Barbearias' link in the top navigation to open the barbershops listing page.
        # Barbearias link
        elem = page.get_by_role("link", name="Barbearias")
        await elem.click(timeout=10000)
        
        # -> Click the 'Buscar' button to submit the search form with no term entered and trigger validation.
        # Buscar button
        elem = page.get_by_role("button", name="Buscar")
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> A mensagem de validação 'Digite algo para buscar' está visível após submeter a busca sem termo.
        # Assert-outcome: passed
        # Assert: Verifica que a mensagem de validação 'Digite algo para buscar' aparece na página.
        await expect(page.locator("body").nth(0)).to_contain_text("Digite algo para buscar", timeout=15000), "Verifica que a mensagem de valida\u00e7\u00e3o 'Digite algo para buscar' aparece na p\u00e1gina."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    