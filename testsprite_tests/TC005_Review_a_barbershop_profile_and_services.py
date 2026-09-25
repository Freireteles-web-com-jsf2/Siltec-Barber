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
        
        # -> Click the 'The Dapper Den' barbershop card to open its detail page.
        # 5,0
        elem = page.locator(".inline-flex > .text-xs").first
        await elem.click(timeout=10000)
        
        # -> Click the 'Reservar' button on the 'The Dapper Den' card to open its detail page
        # Reservar link
        elem = page.locator("div").filter(has_text=re.compile(r"^The Dapper DenTravessa da Navalha, 101Reservar$")).get_by_role("link")
        await elem.click(timeout=10000)
        
        # -> Scroll to the 'Nossos Serviços' section to bring the services list into view.
        await page.mouse.wheel(0, 300)
        
        # --> Assertions to verify final state
        
        # --> The about section is visible with the barber's description.
        await page.locator(".flex > .rounded-xl").first.nth(0).scroll_into_view_if_needed()
        # Assert-outcome: passed
        # Assert: The about section container is visible on the page.
        await expect(page.locator(".flex > .rounded-xl").first.nth(0)).to_be_visible(timeout=15000), "The about section container is visible on the page."
        
        # --> The services list and opening hours are displayed on the page.
        await page.locator("div:nth-child(2) > .flex > .inline-flex").first.nth(0).scroll_into_view_if_needed()
        # Assert-outcome: passed
        # Assert: A service entry 'Reservar' button is visible, indicating services are listed.
        await expect(page.locator("div:nth-child(2) > .flex > .inline-flex").first.nth(0)).to_be_visible(timeout=15000), "A service entry 'Reservar' button is visible, indicating services are listed."
        await page.get_by_text("Fechado").nth(0).scroll_into_view_if_needed()
        # Assert-outcome: passed
        # Assert: The opening hours panel shows a 'Fechado' entry, indicating hours are displayed.
        await expect(page.get_by_text("Fechado").nth(0)).to_be_visible(timeout=15000), "The opening hours panel shows a 'Fechado' entry, indicating hours are displayed."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    