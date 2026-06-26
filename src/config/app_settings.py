from pathlib import Path
from functools import lru_cache
import os

from dotenv import load_dotenv


@lru_cache(maxsize=1)
def load_app_settings():
    project_root = Path(__file__).resolve().parents[2]
    load_dotenv(project_root / ".env")

    return {
        "project_root": project_root,
        "data_dir": Path(os.getenv("DATA_DIR", project_root / "data")),
        "log_dir": Path(os.getenv("LOG_DIR", project_root / "logs")),
        "scraping_url": os.getenv(
            "SCRAPING_URL",
            "https://app.dito.com.br/agenda/metas/results?brand=bagaggio&page=1&pageSize=10&sortColumn=goalProgress&sortOrder=asc&groupBy=seller",
        ),
        "chrome_user_data_dir": Path(
            os.getenv(
                "CHROME_USER_DATA_DIR",
                r"C:\Users\BG - GUSTAVO AZEVEDO\Documents\IMPORTANTE\Profiles\Profile",
            )
        ),
        "chrome_channel": os.getenv("CHROME_CHANNEL", "chrome"),
        "chrome_headless": os.getenv("CHROME_HEADLESS", "false").lower() == "true",
        "download_filename": os.getenv("SCRAPING_DOWNLOAD_FILENAME", "tentativas-dito.csv"),
        "alert_email": os.getenv("SCRAPING_ALERT_EMAIL", "gustavo.azevedo@bagaggio.com.br"),
    }
