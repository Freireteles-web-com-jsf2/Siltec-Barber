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
        
        # -> Abrir a página 'Barbearias' navegando para /barbershops
        await page.goto("http://localhost:3000/barbershops")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Click the 'Barbearia Vintage' card to open its details page.
        # 5,0
        elem = page.locator("div:nth-child(7) > .bg-card > .p-0 > .relative > .inline-flex > .text-xs")
        await elem.click(timeout=10000)
        
        # -> Click the 'Reservar' button on the 'Barbearia Vintage' card to open its details page.
        # Reservar link
        elem = page.locator("div").filter(has_text=re.compile(r"^Barbearia VintageRua da Barbearia, 123Reservar$")).get_by_role("link")
        await elem.click(timeout=10000)
        
        # -> Click the 'Ligar' button in the Contato section to exercise the phone contact option.
        # Ligar button
        elem = page.get_by_role("button", name="Ligar")
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> The barbershop details page shows a phone contact with 'Copiar' and 'Ligar' buttons.
        await page.get_by_role("button", name="Ligar").nth(0).scroll_into_view_if_needed()
        # Assert-outcome: passed
        # Assert: The 'Ligar' button is visible.
        await expect(page.get_by_role("button", name="Ligar").nth(0)).to_be_visible(timeout=15000), "The 'Ligar' button is visible."
        await page.get_by_role("button", name="Copiar").nth(0).scroll_into_view_if_needed()
        # Assert-outcome: passed
        # Assert: The 'Copiar' button is visible.
        await expect(page.get_by_role("button", name="Copiar").nth(0)).to_be_visible(timeout=15000), "The 'Copiar' button is visible."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    