class PortalPage:

    def __init__(self, page):
        self.page = page

    def acessar(self):
        self.page.goto("https://app.dito.com.br/agenda/metas/results?brand=bagaggio&page=1&pageSize=10&sortColumn=goalProgress&sortOrder=asc&groupBy=seller", wait_until="domcontentloaded")
        self.aguardar_estado_inicial()

    def aguardar_estado_inicial(self, timeout_ms=15000):
        self.page.wait_for_selector("div.login-box, button.ant-btn-block", state="visible", timeout=timeout_ms)

    def sessao_ativa(self):
        return self.page.locator("div.login-box").count() == 0

    def filtro_data(self, dt_inicio, dt_fim):
        # Clica na classe com a class = "ant-picker-input-active"
        self.page.locator(".ant-picker-input-active").click()
        
        # Clica no td com o title contém a data de início
        self.page.locator(f"td[title='{dt_inicio}']").click()

        # Clica no td com o title contém a data de fim
        self.page.locator(f"td[title='{dt_fim}']").click()

    def exportar(self):
        # Clica no BUTTON com a classe = "ant-btn-default"
        self.page.locator("button.ant-btn-block").click()