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
        
        # -> Navigate to the 'Barbearias' page (open the barbershops listing).
        await page.goto("http://localhost:3000/barbershops")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Click the 'Reservar' button on the first barbershop card to open its detail / booking flow.
        # Reservar link
        elem = page.locator("div").filter(has_text=re.compile(r"^The Dapper DenTravessa da Navalha, 101Reservar$")).get_by_role("link")
        await elem.click(timeout=10000)
        
        # -> Click the 'Reservar' button for the 'Corte de Cabelo' service to open the booking / sign-in dialog.
        # Reservar button
        elem = page.locator("div:nth-child(2) > .flex > .inline-flex").first
        await elem.click(timeout=10000)
        
        # -> Click the 'Close' button on the 'Faça login na plataforma' sign-in dialog to dismiss it.
        # Close button
        elem = page.get_by_role("button", name="Close")
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> The barbershop detail page is visible: the URL is a /barbershops/ page and service 'Reservar' buttons are shown.
        # Assert-outcome: passed
        # Assert: The current URL contains '/barbershops/', indicating a barbershop detail page.
        await expect(page).to_have_url(re.compile("/barbershops/"), timeout=15000), "The current URL contains '/barbershops/', indicating a barbershop detail page."
        # Assert-outcome: passed
        # Assert: A service 'Reservar' button is visible on the barbershop detail page.
        await expect(page.locator("#servicos").nth(0)).to_contain_text("Reservar", timeout=15000), "A service 'Reservar' button is visible on the barbershop detail page."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    