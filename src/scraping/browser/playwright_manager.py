import logging

from playwright.sync_api import sync_playwright

from src.config.app_settings import load_app_settings


logger = logging.getLogger(__name__)

class BrowserManager:

    def __init__(self):
        self.settings = load_app_settings()
        self.playwright = None
        self.context = None
        self.download_dir = self.settings["data_dir"]

    def start(self):

        logger.info(
            "Iniciando navegador Playwright com perfil em %s e modo headless=%s.",
            self.settings["chrome_user_data_dir"],
            self.settings["chrome_headless"],
        )

        self.download_dir.mkdir(parents=True, exist_ok=True)

        self.playwright = sync_playwright().start()

        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.settings["chrome_user_data_dir"]),
            headless=self.settings["chrome_headless"],
            channel=self.settings["chrome_channel"],
            accept_downloads=True,
        )

        return self.context

    def close(self):

        logger.info("Encerrando navegador Playwright.")

        if self.context:
            self.context.close()

        if self.playwright:
            self.playwright.stop()

    def save_download(self, download, filename):
        target_path = self.download_dir / filename
        logger.info("Salvando download em %s.", target_path)
        download.save_as(str(target_path))
        return target_path