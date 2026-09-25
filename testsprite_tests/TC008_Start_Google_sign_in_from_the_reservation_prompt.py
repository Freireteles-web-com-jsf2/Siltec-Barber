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
        
        # -> Navigate to the 'Barbearias' listing page (http://localhost:3000/barbershops).
        await page.goto("http://localhost:3000/barbershops")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Click the 'Reservar' button for the first barbershop (The Dapper Den) to start the reservation flow
        # Reservar link
        elem = page.locator("div").filter(has_text=re.compile(r"^The Dapper DenTravessa da Navalha, 101Reservar$")).get_by_role("link")
        await elem.click(timeout=10000)
        
        # -> Click the 'Reservar' button for the 'Corte de Cabelo' service to start the booking and trigger the sign-in dialog.
        # Reservar button
        elem = page.locator("div:nth-child(2) > .flex > .inline-flex").first
        await elem.click(timeout=10000)
        
        # -> Click the 'Google' button in the 'Faça login na plataforma' dialog to start the Google authentication flow.
        # Google button
        elem = page.get_by_role("button", name="Fazer login com o Google")
        await elem.click(timeout=10000)
        
        # -> Click the 'Barbearias' link to open the barbearias listing page.
        # Barbearias link
        elem = page.get_by_role("link", name="Barbearias")
        await elem.click(timeout=10000)
        
        # -> Open the 'The Dapper Den' detail page by clicking the 'Reservar' button labeled 'Reservar' for The Dapper Den.
        # Reservar link
        elem = page.locator("div").filter(has_text=re.compile(r"^The Dapper DenTravessa da Navalha, 101Reservar$")).get_by_role("link")
        await elem.click(timeout=10000)
        
        # -> Click the 'Reservar' button for the 'Corte de Cabelo' service to trigger the booking sign-in dialog.
        # Reservar button
        elem = page.locator("div:nth-child(2) > .flex > .inline-flex").first
        await elem.click(timeout=10000)
        
        # -> Click the 'Google' button in the 'Faça login na plataforma' dialog to attempt to start the Google OAuth authentication flow and observe whether a redirect to an OAuth endpoint or an internal auth route occurs.
        # Google button
        elem = page.get_by_role("button", name="Fazer login com o Google")
        await elem.click(timeout=10000)
        
        # -> Click the 'Barbearias' link to open the barbearias listing page so the booking flow can be retried.
        # Barbearias link
        elem = page.get_by_role("link", name="Barbearias")
        await elem.click(timeout=10000)
        
        # -> Open The Dapper Den detail page by clicking the 'Reservar' button for The Dapper Den.
        # Reservar link
        elem = page.locator("div").filter(has_text=re.compile(r"^The Dapper DenTravessa da Navalha, 101Reservar$")).get_by_role("link")
        await elem.click(timeout=10000)
        
        # -> Click the 'Reservar' button for the 'Corte de Cabelo' service to open the 'Faça login na plataforma' sign-in dialog.
        # Reservar button
        elem = page.locator("div:nth-child(2) > .flex > .inline-flex").first
        await elem.click(timeout=10000)
        
        # -> Click the 'Google' button in the 'Faça login na plataforma' dialog and verify the application attempted to start the Google authentication flow (look for callbackUrl, /api/auth, accounts.google.com, or a redirect).
        # Google button
        elem = page.get_by_role("button", name="Fazer login com o Google")
        await elem.click(timeout=10000)
        
        # -> Click the 'Barbearias' link to open the barbearias listing page.
        # Barbearias link
        elem = page.get_by_role("link", name="Barbearias")
        await elem.click(timeout=10000)
        
        # -> Open 'The Dapper Den' detail page by clicking the 'Reservar' link next to the 'The Dapper Den' listing.
        # Reservar link
        elem = page.locator("div").filter(has_text=re.compile(r"^The Dapper DenTravessa da Navalha, 101Reservar$")).get_by_role("link")
        await elem.click(timeout=10000)
        
        # -> Click the 'Reservar' button for the 'Corte de Cabelo' service to open the 'Faça login na plataforma' sign-in dialog.
        # Reservar button
        elem = page.locator("div:nth-child(2) > .flex > .inline-flex").first
        await elem.click(timeout=10000)
        
        # -> Click the 'Google' button in the 'Faça login na plataforma' dialog to attempt to start the Google authentication flow.
        # Google button
        elem = page.get_by_role("button", name="Fazer login com o Google")
        await elem.click(timeout=10000)
        
        # -> Click the 'Barbearias' navigation link to open the barbearias listing page so the booking flow can be retried.
        # Barbearias link
        elem = page.get_by_role("link", name="Barbearias")
        await elem.click(timeout=10000)
        
        # -> Open The Dapper Den detail page by clicking the 'Reservar' link next to The Dapper Den in the listing.
        # Reservar link
        elem = page.locator("div").filter(has_text=re.compile(r"^The Dapper DenTravessa da Navalha, 101Reservar$")).get_by_role("link")
        await elem.click(timeout=10000)
        
        # -> Click the 'Reservar' button next to 'Corte de Cabelo' to open the 'Faça login na plataforma' sign-in dialog.
        # Reservar button
        elem = page.locator("div:nth-child(2) > .flex > .inline-flex").first
        await elem.click(timeout=10000)
        
        # -> Click the 'Google' button in the 'Faça login na plataforma' dialog and observe whether the app attempts to start the Google authentication flow (redirect, callbackUrl, or /api/auth markers).
        # Google button
        elem = page.get_by_role("button", name="Fazer login com o Google")
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> The booking sign-in dialog's Google button initiated the OAuth attempt — the browser URL contains a callbackUrl parameter.
        # Assert-outcome: passed
        # Assert: Checks the browser URL includes 'callbackUrl' indicating an OAuth callback/redirect was initiated.
        await expect(page).to_have_url(re.compile("callbackUrl="), timeout=15000), "Checks the browser URL includes 'callbackUrl' indicating an OAuth callback/redirect was initiated."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    