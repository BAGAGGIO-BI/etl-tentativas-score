import logging

from service.tratamento import tratamento_base
from utils.conexao import config
from utils.logging_config import configure_logging
from loader.carga import insert_bd


logger = logging.getLogger(__name__)

def etl_tentativas():
    logger.info("Iniciando ETL de tentativas.")

    df = tratamento_base()
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