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
        
        # -> Click the 'Barbearias' link in the top navigation to open the barbershops listing.
        # Barbearias link
        elem = page.get_by_role("link", name="Barbearias")
        await elem.click(timeout=10000)
        
        # -> Click the 'Reservar' link for The Dapper Den to open the booking flow or navigate to its detail page.
        # Reservar link
        elem = page.locator("div").filter(has_text=re.compile(r"^The Dapper DenTravessa da Navalha, 101Reservar$")).get_by_role("link")
        await elem.click(timeout=10000)
        
        # -> Click the 'Reservar' button for the 'Corte de Cabelo' service to start the booking flow.
        # Reservar button
        elem = page.locator("div:nth-child(2) > .flex > .inline-flex").first
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> Booking flow opened: the sign-in dialog titled 'Faça login na plataforma' is visible.
        # Assert-outcome: passed
        # Assert: The sign-in dialog shows the title 'Faça login na plataforma'.
        await expect(page.locator("xpath=/html/body/div[5]").nth(0)).to_contain_text("Fa\u00e7a login na plataforma", timeout=15000), "The sign-in dialog shows the title 'Fa\u00e7a login na plataforma'."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    