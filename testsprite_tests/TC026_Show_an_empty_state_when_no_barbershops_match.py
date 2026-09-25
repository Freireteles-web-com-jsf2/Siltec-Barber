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
        
        # -> Fill the 'Buscar barbearia pelo nome...' field with a unique non-matching term and click the 'Buscar' button to run the search.
        # Buscar barbearia pelo nome... text field
        elem = page.get_by_role("textbox", name="Buscar barbearia pelo nome...")
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("termo-inexistente-xyz-99999")
        
        # -> Fill the 'Buscar barbearia pelo nome...' field with a unique non-matching term and click the 'Buscar' button to run the search.
        # Buscar button
        elem = page.get_by_role("button", name="Buscar")
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> The page displays the empty results state with the headline "Nenhuma barbearia encontrada".
        await page.locator("xpath=/html/body/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/svg").nth(0).scroll_into_view_if_needed()
        # Assert-outcome: passed
        # Assert: The empty-state illustration/icon is visible on the results area.
        await expect(page.locator("xpath=/html/body/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/svg").nth(0)).to_be_visible(timeout=15000), "The empty-state illustration/icon is visible on the results area."
        
        # --> Recovery actions are shown: 'Ver Todas as Barbearias', 'Voltar ao Início', 'Sugerir Barbearia', and 'Falar Conosco'.
        # Assert-outcome: passed
        # Assert: The 'Ver Todas as Barbearias' link is visible.
        await expect(page.locator("xpath=/html/body/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/a[1]").nth(0)).to_have_text("Ver Todas as Barbearias", timeout=15000), "The 'Ver Todas as Barbearias' link is visible."
        # Assert-outcome: passed
        # Assert: The 'Voltar ao Início' link is visible.
        await expect(page.locator("xpath=/html/body/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/a[2]").nth(0)).to_have_text("Voltar ao In\u00edcio", timeout=15000), "The 'Voltar ao In\u00edcio' link is visible."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    