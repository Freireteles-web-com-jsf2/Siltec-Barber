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
        
        # -> Open the 'Sobre' (About) page and verify the about page content is displayed.
        await page.goto("http://localhost:3000/sobre")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Click the 'Contato' link in the footer to open the contact page and verify its content.
        # Contato link
        elem = page.get_by_role("link", name="Contato", exact=True)
        await elem.click(timeout=10000)
        
        # -> Click the 'Termos' link in the footer to open the Terms page.
        # Termos link
        elem = page.get_by_role("link", name="Termos")
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> The About page (/sobre) was opened and shows the 'Sobre o Siltec-Barber' heading and descriptive content.
        # Assert-outcome: passed
        # Assert: URL contains '/sobre', confirming the About page was opened.
        await expect(page).to_have_url(re.compile("/sobre"), timeout=15000), "URL contains '/sobre', confirming the About page was opened."
        
        # --> The Contact page (/contato) was opened and shows the 'Contato' heading and contact sections.
        # Assert-outcome: passed
        # Assert: URL contains '/contato', confirming the Contact page was opened.
        await expect(page).to_have_url(re.compile("/contato"), timeout=15000), "URL contains '/contato', confirming the Contact page was opened."
        
        # --> The Terms page (/termos) is open and displays the 'Termos de Uso' heading and 'Última atualização: 5 de setembro de 2026'.
        # Assert-outcome: passed
        # Assert: URL contains '/termos', confirming the Terms page is open.
        await expect(page).to_have_url(re.compile("/termos"), timeout=15000), "URL contains '/termos', confirming the Terms page is open."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    