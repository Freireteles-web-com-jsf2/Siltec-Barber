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
        
        # -> Open the login page and sign in using the 'E-mail' field (admin@teste.dev) and 'Senha' (TesteBarber2026) by clicking the 'Entrar' button.
        await page.goto("http://localhost:3000/login")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Fill the 'E-mail' field with admin@teste.dev, the 'Senha' field with TesteBarber2026, and click the 'Entrar' button to sign in as admin.
        # voce@exemplo.com email field
        elem = page.get_by_role("textbox", name="E-mail")
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("admin@teste.dev")
        
        # -> Fill the 'E-mail' field with admin@teste.dev, the 'Senha' field with TesteBarber2026, and click the 'Entrar' button to sign in as admin.
        # •••••••• password field
        elem = page.get_by_role("textbox", name="Senha")
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("TesteBarber2026")
        
        # -> Fill the 'E-mail' field with admin@teste.dev, the 'Senha' field with TesteBarber2026, and click the 'Entrar' button to sign in as admin.
        # Entrar button
        elem = page.get_by_role("button", name="Entrar")
        await elem.click(timeout=10000)
        
        # -> Open the 'Serviços' page by clicking the 'Serviços' link in the left sidebar.
        # Serviços link
        elem = page.get_by_role("link", name="Serviços")
        await elem.click(timeout=10000)
        
        # -> Click the 'Novo serviço' button to open the new service dialog.
        # Novo serviço button
        elem = page.get_by_role("button", name="Novo serviço")
        await elem.click(timeout=10000)
        
        # -> Fill the 'Nome' field with 'Corte Teste Sprite', the 'Descrição' with 'Serviço criado pelo teste automatizado.', set 'Preço (R$)' to 50, then open the 'Duração' dropdown.
        # Corte de cabelo text field
        elem = page.get_by_role("textbox", name="Nome")
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("Corte Teste Sprite")
        
        # -> Fill the 'Nome' field with 'Corte Teste Sprite', the 'Descrição' with 'Serviço criado pelo teste automatizado.', set 'Preço (R$)' to 50, then open the 'Duração' dropdown.
        # Estilo personalizado com técnicas modernas. text area
        elem = page.get_by_role("textbox", name="Descrição")
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("Servi\u00e7o criado pelo teste automatizado.")
        
        # -> Fill the 'Nome' field with 'Corte Teste Sprite', the 'Descrição' with 'Serviço criado pelo teste automatizado.', set 'Preço (R$)' to 50, then open the 'Duração' dropdown.
        # 60,00 number field
        elem = page.get_by_role("spinbutton", name="Preço (R$)")
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("50")
        
        # -> Fill the 'Nome' field with 'Corte Teste Sprite', the 'Descrição' with 'Serviço criado pelo teste automatizado.', set 'Preço (R$)' to 50, then open the 'Duração' dropdown.
        # 15 min 20 min 30 min 45 min 60 min 75 min 90 min... dropdown
        elem = page.get_by_label("Duração")
        await elem.click(timeout=10000)
        
        # -> Select '30 min' from the 'Duração' dropdown in the 'Novo serviço' dialog.
        # 15 min 20 min 30 min 45 min 60 min 75 min 90 min... dropdown
        elem = page.locator("xpath=/html/body/div[4]/form/div[3]/div[2]/div/select").nth(0)
        await elem.wait_for(state="visible", timeout=10000)
        await elem.select_option("")
        
        # -> Fill the 'URL da imagem' field with 'https://utfs.io/f/c97a2dc9-cf62-468b-a851-bfd2bdde775f-16p.png' and click the 'Criar serviço' button.
        # https://... text field
        elem = page.get_by_role("textbox", name="URL da imagem")
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("https://utfs.io/f/c97a2dc9-cf62-468b-a851-bfd2bdde775f-16p.png")
        
        # -> Fill the 'URL da imagem' field with 'https://utfs.io/f/c97a2dc9-cf62-468b-a851-bfd2bdde775f-16p.png' and click the 'Criar serviço' button.
        # Criar serviço button
        elem = page.get_by_role("button", name="Criar serviço")
        await elem.click(timeout=10000)
        
        # -> Click the delete button labeled 'Excluir Corte Teste Sprite' to open the confirmation dialog.
        # Excluir Corte Teste Sprite button
        elem = page.get_by_role("button", name="Excluir Corte Teste Sprite")
        await elem.click(timeout=10000)
        
        # -> Click the 'Excluir' button in the confirmation dialog to confirm deletion of 'Corte Teste Sprite'.
        # Excluir button
        elem = page.get_by_role("button", name="Excluir")
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> A notificação de sucesso 'Serviço excluído.' é exibida após a exclusão.
        # Assert-outcome: passed
        # Assert: Verifica que a notificação 'Serviço excluído.' aparece.
        await expect(page.locator("xpath=/html/body/section/ol/li").nth(0)).to_have_text("Servi\u00e7o exclu\u00eddo.", timeout=15000), "Verifica que a notifica\u00e7\u00e3o 'Servi\u00e7o exclu\u00eddo.' aparece."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    