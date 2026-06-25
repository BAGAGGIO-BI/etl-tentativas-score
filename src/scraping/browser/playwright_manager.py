from playwright.sync_api import sync_playwright

class BrowserManager:

    def __init__(self):
        self.playwright = None
        self.context = None

    def start(self):

        self.playwright = sync_playwright().start()

        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir="C:\\Users\\BG - GUSTAVO AZEVEDO\\Documents\\IMPORTANTE\\Profiles\\Profile",
            headless=False,
            channel="chrome"
        )

        return self.context

    def close(self):

        if self.context:
            self.context.close()

        if self.playwright:
            self.playwright.stop()

    def save_download(self, download, filename):
        download.save_as(f'C:\\Users\\BG - GUSTAVO AZEVEDO\\Documents\\IMPORTANTE\\Pythons\\etl-tentativas-score\\data\\{filename}')