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
        
        # -> Click the 'Barbearias' link in the top navigation to open the list of barbershops.
        # Barbearias link
        elem = page.get_by_role("link", name="Barbearias")
        await elem.click(timeout=10000)
        
        # -> Click the 'The Dapper Den' barbershop card to open its detail page.
        # 5,0
        elem = page.locator(".inline-flex > .text-xs").first
        await elem.click(timeout=10000)
        
        # -> Click the 'The Dapper Den' barbershop card to open its detail page.
        # 5,0
        elem = page.locator(".inline-flex > .text-xs").first
        await elem.click(timeout=10000)
        
        # -> Click the 'Reservar' button on The Dapper Den card to open the barbershop detail/booking view and then check for a contact phone option.
        # Reservar link
        elem = page.locator("div").filter(has_text=re.compile(r"^The Dapper DenTravessa da Navalha, 101Reservar$")).get_by_role("link")
        await elem.click(timeout=10000)
        
        # -> Click the 'Ligar' button in the contact section to invoke the phone action.
        # Ligar button
        elem = page.get_by_role("button", name="Ligar")
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> The phone action 'Ligar' is available on the barbershop detail page.
        # Assert-outcome: passed
        # Assert: The 'Ligar' button is present with the label 'Ligar'.
        await expect(page.locator("xpath=/html/body/div[2]/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/div/button[2]").nth(0)).to_have_text("Ligar", timeout=15000), "The 'Ligar' button is present with the label 'Ligar'."
        
        # --> The contact section remained visible after interacting with the phone action and shows the contact controls.
        # Assert-outcome: passed
        # Assert: The contact controls remain visible (the 'Copiar' button is present), indicating the contact section is still shown.
        await expect(page.locator("xpath=/html/body/div[2]/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/div/button[1]").nth(0)).to_have_text("Copiar", timeout=15000), "The contact controls remain visible (the 'Copiar' button is present), indicating the contact section is still shown."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    