import logging

from src.config.app_settings import load_app_settings
from src.scraping.pages.portal_page import PortalPage
from src.scraping.browser.playwright_manager import BrowserManager
from src.scraping.utils.calculate_date import calcular_datas
from src.scraping.services.email.email_service import EmailService


logger = logging.getLogger(__name__)
SETTINGS = load_app_settings()

def exporta_csv():
    logger.info("Iniciando etapa de scraping do App Dito.")

    browser = BrowserManager()

    try:
        context = browser.start()

        page = context.new_page()

        portal = PortalPage(page)

        portal.acessar()

        # Validar sessão ativa
        if portal.sessao_ativa():
            logger.info("Status da sessão: ativa.")
        else:
            logger.warning("Status da sessão: inativa.")
            logger.warning("A página exibiu a div login-box, indicando que a sessão foi deslogada.")
            email_service = EmailService()
            email_service.enviar_email_teste(SETTINGS["alert_email"])
            logger.info("Email de teste enviado para %s.", SETTINGS["alert_email"])
            input("Pressione ENTER para encerrar")
            raise SystemExit(1)

        # Cálculo de Datas
        dt_inicio, dt_fim = calcular_datas()

        # Clica no campo de data e seleciona a data de início e fim
        portal.filtro_data(dt_inicio, dt_fim)

        # Aplica o filtro
        portal.aplicar_filtro()

        # Exporta o relatório
        with page.expect_download() as download_info:
            portal.exportar()

        # Gerenciamento do download
        download = download_info.value
        logger.info("Arquivo baixado: %s.", download.suggested_filename)
        logger.debug("Path temporário do download: %s.", download.path())

        saved_path = browser.save_download(download, SETTINGS["download_filename"])

        logger.info("Arquivo salvo em: %s.", saved_path)

        logger.info("Etapa de scraping concluída com sucesso.")

    except Exception:
        logger.exception("Falha na etapa de scraping/exportação.")
        raise

    finally:

        browser.close()
        logger.info("Navegador finalizado.")
        
if __name__ == "__main__":
    exporta_csv()