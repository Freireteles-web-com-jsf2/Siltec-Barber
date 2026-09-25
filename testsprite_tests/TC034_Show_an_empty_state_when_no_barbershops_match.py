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
        
        # -> Navigate to the Barbershops page at /barbershops.
        await page.goto("http://localhost:3000/barbershops")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Type 'zzxyq_notfound_999' into the 'Buscar barbearia pelo nome...' search field and click the 'Buscar' button to trigger the search.
        # Buscar barbearia pelo nome... text field
        elem = page.get_by_role("textbox", name="Buscar barbearia pelo nome...")
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("zzxyq_notfound_999")
        
        # -> Type 'zzxyq_notfound_999' into the 'Buscar barbearia pelo nome...' search field and click the 'Buscar' button to trigger the search.
        # Buscar button
        elem = page.get_by_role("button", name="Buscar")
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> The page shows the empty-state message 'Nenhuma barbearia encontrada' for the unmatched search.
        # Assert-outcome: passed
        # Assert: Empty-state message 'Nenhuma barbearia encontrada' is visible on the results area.
        await expect(page.locator("body").nth(0)).to_contain_text("Nenhuma barbearia encontrada", timeout=15000), "Empty-state message 'Nenhuma barbearia encontrada' is visible on the results area."
        
        # --> The search reports zero results: the page shows '0 barbearias encontradas'.
        # Assert-outcome: passed
        # Assert: Results count indicates zero barbershops were found.
        await expect(page.locator("body").nth(0)).to_contain_text("0 barbearias encontradas", timeout=15000), "Results count indicates zero barbershops were found."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    