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
        
        # -> Click the 'Barbearias' link in the top navigation to open the barbershop listing page.
        # Barbearias link
        elem = page.get_by_role("link", name="Barbearias")
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> The Barbearias listing page is open and shows shop results.
        # Assert-outcome: passed
        # Assert: The browser is on the /barbershops page.
        await expect(page).to_have_url(re.compile("/barbershops"), timeout=15000), "The browser is on the /barbershops page."
        # Assert-outcome: passed
        # Assert: A shop card shows a 'Reservar' link, indicating listing results are visible.
        await expect(page.locator("xpath=/html/body/div[2]/div/div/div[2]/div/div[2]/div[2]/div[1]/div/div/div[2]/a").nth(0)).to_have_text("Reservar", timeout=15000), "A shop card shows a 'Reservar' link, indicating listing results are visible."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    