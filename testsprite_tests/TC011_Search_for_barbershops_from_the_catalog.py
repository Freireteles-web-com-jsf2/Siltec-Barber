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
        
        # -> Click the 'Barbearias' link in the header to open the barbershops listing page.
        # Barbearias link
        elem = page.get_by_role("link", name="Barbearias")
        await elem.click(timeout=10000)
        
        # -> Fill the 'Buscar barbearia pelo nome...' field with 'Dapper' and click the 'Buscar' button to run the search.
        # Buscar barbearia pelo nome... text field
        elem = page.get_by_role("textbox", name="Buscar barbearia pelo nome...")
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("Dapper")
        
        # -> Fill the 'Buscar barbearia pelo nome...' field with 'Dapper' and click the 'Buscar' button to run the search.
        # Buscar button
        elem = page.get_by_role("button", name="Buscar")
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> Search input contains the typed term 'Dapper'.
        # Assert-outcome: passed
        # Assert: Search input value equals 'Dapper'.
        await expect(page.get_by_role("textbox", name="Buscar barbearia pelo nome...").nth(0)).to_have_value("Dapper", timeout=15000), "Search input value equals 'Dapper'."
        
        # --> The browser URL includes the search query parameter for 'Dapper'.
        # Assert-outcome: passed
        # Assert: URL contains the search parameter 'title=Dapper'.
        await expect(page).to_have_url(re.compile("title=Dapper"), timeout=15000), "URL contains the search parameter 'title=Dapper'."
        
        # --> A search result is visible with a 'Reservar' link.
        await page.get_by_role("link", name="Reservar").nth(0).scroll_into_view_if_needed()
        # Assert-outcome: passed
        # Assert: A 'Reservar' link for a listed barbershop is visible.
        await expect(page.get_by_role("link", name="Reservar").nth(0)).to_be_visible(timeout=15000), "A 'Reservar' link for a listed barbershop is visible."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    