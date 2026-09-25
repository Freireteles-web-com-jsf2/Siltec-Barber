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
        
        # -> Click the 'Barbearias' link in the top navigation to open the barbearias listing page.
        # Barbearias link
        elem = page.get_by_role("link", name="Barbearias")
        await elem.click(timeout=10000)
        
        # -> Click the 'Reservar' button for 'The Dapper Den' in the search results to open its detail/booking page.
        # Reservar link
        elem = page.locator("div").filter(has_text=re.compile(r"^The Dapper DenTravessa da Navalha, 101Reservar$")).get_by_role("link")
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> Barbershop detail page for The Dapper Den is open.
        # Assert-outcome: passed
        # Assert: The URL contains /barbershops/ indicating a barbershop detail page.
        await expect(page).to_have_url(re.compile("/barbershops/"), timeout=15000), "The URL contains /barbershops/ indicating a barbershop detail page."
        await page.get_by_role("paragraph").filter(has_text="4.9").nth(0).scroll_into_view_if_needed()
        # Assert-outcome: passed
        # Assert: The detail page header/rating element is visible on the page.
        await expect(page.get_by_role("paragraph").filter(has_text="4.9").nth(0)).to_be_visible(timeout=15000), "The detail page header/rating element is visible on the page."
        
        # --> The 'Nossos Serviços' section with service entries is visible (services have 'Reservar' buttons).
        await page.locator("div:nth-child(2) > .flex > .inline-flex").first.nth(0).scroll_into_view_if_needed()
        # Assert-outcome: passed
        # Assert: A service's 'Reservar' button is visible, proving the services list is shown.
        await expect(page.locator("div:nth-child(2) > .flex > .inline-flex").first.nth(0)).to_be_visible(timeout=15000), "A service's 'Reservar' button is visible, proving the services list is shown."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    