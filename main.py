import logging

from src.pipeline.extraction import importa_csv
from src.pipeline.transformation import tratamento_base
from src.config.database import config
from src.config.logger import configure_logging
from src.pipeline.loading import insert_bd


logger = logging.getLogger(__name__)

def etl_tentativas():
    logger.info("Iniciando ETL de tentativas.")

    df = importa_csv()
    logger.info("Arquivo carregado com %s linhas e %s colunas.", *df.shape)

    df = tratamento_base(df)
    logger.info("Tratamento concluído com %s registros.", len(df))

    engine = config()
    insert_bd(engine, df)

    logger.info("ETL finalizado com sucesso.")

if __name__ == "__main__":
    configure_logging()

    try:
        etl_tentativas()
    except Exception:
        logger.exception("Falha na execução do ETL.")
        raise