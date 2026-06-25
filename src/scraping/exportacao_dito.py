from src.scraping.pages.portal_page import PortalPage
from src.scraping.browser.playwright_manager import BrowserManager
from src.scraping.utils.calculate_date import calcular_datas
from src.scraping.services.email.email_service import EmailService

def exporta_csv():
    browser = BrowserManager()

    try:

        context = browser.start()

        page = context.new_page()

        portal = PortalPage(page)

        portal.acessar()

        # Validar sessão ativa
        if portal.sessao_ativa():
            print("Status da sessão: \tativa")
        else:
            print("Status da sessão: \tinativa")
            print("A página exibiu a div login-box, indicando que a sessão foi deslogada.")
            email_service = EmailService()
            email_service.enviar_email_teste("gustavo.azevedo@bagaggio.com.br")
            print("Email de teste enviado para gustavo.azevedo@bagaggio.com.br")
            input("Pressione ENTER para encerrar")
            raise SystemExit(1)

        # Cálculo de Datas
        dt_inicio, dt_fim = calcular_datas()

        # Aplica o filtro de data
        portal.filtro_data(dt_inicio, dt_fim)

        # Exporta o relatório
        with page.expect_download() as download_info:
            portal.exportar()

        # Gerenciamento do download
        download = download_info.value
        print(f"Arquivo baixado: {download.suggested_filename}")
        print(f"Path: {download.path()}")

        browser.save_download(download, 'tentativas-dito.csv')

        print(f"Arquivo salvo em: C:\\Users\\BG - GUSTAVO AZEVEDO\\Documents\\IMPORTANTE\\Pythons\\etl-tentativas-score\\data\\{download.suggested_filename}")

    finally:

        browser.close()
        
if __name__ == "__main__":
    exporta_csv()