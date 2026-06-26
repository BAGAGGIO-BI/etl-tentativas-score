import logging

from src.config.app_settings import load_app_settings


logger = logging.getLogger(__name__)
SETTINGS = load_app_settings()

class PortalPage:

    def __init__(self, page):
        self.page = page

    def acessar(self):
        logger.info("Acessando o portal Dito em %s.", SETTINGS["scraping_url"])
        self.page.goto(SETTINGS["scraping_url"], wait_until="domcontentloaded")
        self.aguardar_estado_inicial()

    def aguardar_estado_inicial(self, timeout_ms=15000):
        logger.debug("Aguardando estado inicial do portal.")
        self.page.wait_for_selector("div.login-box, button.ant-btn-block", state="visible", timeout=timeout_ms)

    def sessao_ativa(self):
        return self.page.locator("div.login-box").count() == 0

    def filtro_data(self, dt_inicio, dt_fim):
        logger.info("Aplicando filtro de datas de %s até %s.", dt_inicio, dt_fim)

        # Clica na classe com a class = "ant-picker-input-active"
        self.page.locator(".ant-picker-input-active").click()
        
        # Clica no td com o title contém a data de início
        self.page.locator(f"td[title='{dt_inicio}']").click()

        # Clica no td com o title contém a data de fim
        self.page.locator(f"td[title='{dt_fim}']").click()

    def aplicar_filtro(self):
        logger.info("Aplicando filtro no portal.")

        # Espera o botão de aplicar filtro estar habilitado
        # o botão precisa conter o texto "Aplicar Filtro"
        self.page.locator("button.ant-btn-default:has-text('Aplicar')").click()

    def exportar(self):
        logger.info("Acionando exportação do relatório.")

        # Clica no BUTTON com a classe = "ant-btn-block"
        self.page.locator("button.ant-btn-block").click()