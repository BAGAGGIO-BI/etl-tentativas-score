import logging

from src.config.logger import configure_logging
from src.main import etl_tentativas

logger = logging.getLogger(__name__)

def main():
    configure_logging()

    try:
        etl_tentativas()
    except Exception:
        logger.exception("Falha na execução do ETL.")
        raise

if __name__ == "__main__":
    main()