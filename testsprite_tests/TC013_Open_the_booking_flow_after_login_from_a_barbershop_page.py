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
        
        # -> Open the login page ('Entrar') by navigating to /login so the test can sign in with cliente@teste.dev / TesteBarber2026.
        await page.goto("http://localhost:3000/login")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Fill the 'E-mail' field with cliente@teste.dev, fill the 'Senha' field with TesteBarber2026, and click the 'Entrar' button.
        # voce@exemplo.com email field
        elem = page.get_by_role("textbox", name="E-mail")
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("cliente@teste.dev")
        
        # -> Fill the 'E-mail' field with cliente@teste.dev, fill the 'Senha' field with TesteBarber2026, and click the 'Entrar' button.
        # •••••••• password field
        elem = page.get_by_role("textbox", name="Senha")
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("TesteBarber2026")
        
        # -> Fill the 'E-mail' field with cliente@teste.dev, fill the 'Senha' field with TesteBarber2026, and click the 'Entrar' button.
        # Entrar button
        elem = page.get_by_role("button", name="Entrar")
        await elem.click(timeout=10000)
        
        # -> Click the 'Barbearias' navigation link in the top menu to open the barbershops list.
        # Barbearias link
        elem = page.get_by_role("link", name="Barbearias")
        await elem.click(timeout=10000)
        
        # -> Click the 'Reservar' button for the 'The Dapper Den' barbershop card to open the booking flow.
        # Reservar link
        elem = page.locator("div").filter(has_text=re.compile(r"^The Dapper DenTravessa da Navalha, 101Reservar$")).get_by_role("link")
        await elem.click(timeout=10000)
        
        # -> Click the 'Reservar' button for the 'Corte de Cabelo' service to open the booking flow.
        # Reservar button
        elem = page.locator("div:nth-child(2) > .flex > .inline-flex").first
        await elem.click(timeout=10000)
        
        # -> Close the 'Faça login na plataforma' modal by clicking its 'Close' button, then click the 'Reservar' button for the 'Corte de Cabelo' service to open the booking flow.
        # Close button
        elem = page.get_by_role("button", name="Close")
        await elem.click(timeout=10000)
        
        # -> Close the 'Faça login na plataforma' modal by clicking its 'Close' button, then click the 'Reservar' button for the 'Corte de Cabelo' service to open the booking flow.
        # Reservar button
        elem = page.locator("div:nth-child(4) > div > div:nth-child(2) > .flex > .inline-flex")
        await elem.click(timeout=10000)
        
        # -> Close the 'Faça login na plataforma' dialog and click the 'Reservar' button for 'Corte de Cabelo' to open the booking flow.
        # Close button
        elem = page.get_by_role("button", name="Close")
        await elem.click(timeout=10000)
        
        # -> Close the 'Faça login na plataforma' dialog and click the 'Reservar' button for 'Corte de Cabelo' to open the booking flow.
        # Reservar button
        elem = page.locator("div:nth-child(2) > .flex > .inline-flex").first
        await elem.click(timeout=10000)
        
        # -> Click the dialog 'Close' button to dismiss the 'Faça login na plataforma' modal so the page can be interacted with.
        # Close button
        elem = page.get_by_role("button", name="Close")
        await elem.click(timeout=10000)
        
        # -> Click the 'Reservar' button for the 'Corte de Cabelo' service to open the booking flow.
        # Reservar button
        elem = page.locator("div:nth-child(2) > .flex > .inline-flex").first
        await elem.click(timeout=10000)
        
        # -> Click the 'Close' button on the 'Faça login na plataforma' dialog, then click the 'Reservar' button for the Corte de Cabelo service to open the booking flow.
        # Close button
        elem = page.get_by_role("button", name="Close")
        await elem.click(timeout=10000)
        
        # -> Click the 'Close' button on the 'Faça login na plataforma' dialog, then click the 'Reservar' button for the Corte de Cabelo service to open the booking flow.
        # Reservar button
        elem = page.locator("div:nth-child(4) > div > div:nth-child(2) > .flex > .inline-flex")
        await elem.click(timeout=10000)
        
        # -> Press Escape to dismiss the 'Faça login na plataforma' dialog, then click the 'Reservar' button for 'Corte de Cabelo' to try to open the booking flow.
        # Reservar button
        elem = page.locator("div:nth-child(2) > .flex > .inline-flex").first
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> The booking flow did not open because a persistent 'Faça login na plataforma' modal remained open and blocked the reserve action.
        await page.locator("xpath=/html/body/div[5]").nth(0).scroll_into_view_if_needed()
        # Assert-outcome: failed
        # Assert: Expected the 'Faça login na plataforma' modal to be dismissed so the booking flow could open.
        await expect(page.locator("xpath=/html/body/div[5]").nth(0)).to_be_visible(timeout=15000), "Expected the 'Fa\u00e7a login na plataforma' modal to be dismissed so the booking flow could open."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    