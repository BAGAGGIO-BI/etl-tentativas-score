import os
import logging

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

# 1. Inserção no Banco de Dados -------------------------------------------------------


# 1.1 - Estabelece a conexão e insere os Dados tratados no banco
def insert_bd(engine, df):

    # Identifica a Tabela do Banco
    TABLE = os.getenv("TABLE_TENTATIVAS")

    if not TABLE:
        raise EnvironmentError("Variável TABLE_TENTATIVAS não definida.")

    logger.info("Iniciando carga na tabela %s com %s registros.", TABLE, len(df))

    try:
        # Operação de verificação e truncate dentro de transação
        with engine.begin() as conn:

            # 1 - Checar se tabela existe
            exists = table_exists(engine, TABLE)

            # 2 - Checar quantidade de registros
            if exists:
                qtd = conn.execute(text(f"SELECT COUNT(1) FROM {TABLE}")).scalar()

                logger.info("Tabela %s encontrada com %s registros.", TABLE, qtd or 0)

                if qtd and qtd > 0:
                    try:
                        truncate_table(conn, TABLE)
                    except Exception as e_trunc:

                        logger.warning(
                            "Falha ao truncar a tabela %s. Tentando fallback com DELETE.",
                            TABLE,
                        )

                        try:
                            delete_table(conn, TABLE)
                        except Exception as e_delete:
                            logger.exception(
                                "Falha ao deletar os registros da tabela %s.", TABLE
                            )
                            raise
            else:
                logger.warning("Tabela %s não existe.", TABLE)

        logger.info("Iniciando carga na tabela %s.", TABLE)

        # 3 - Inserir com pandas.to_sql (append)
        insert_table(df, TABLE, engine)

        logger.info("Carga concluída com sucesso na tabela %s.", TABLE)

    # Tratamento de Exceção - Biblioteca SQL Alchemy
    except SQLAlchemyError as sae:
        logger.exception("Erro SQLAlchemy durante a carga na tabela %s.", TABLE)
        raise

    # Tratamento de Exceção - Outro Erro
    except Exception as e:
        logger.exception("Erro geral durante a carga na tabela %s.", TABLE)
        raise

    logger.info("---------------------------")


# -------------------------------------------------------------------------------------

# Funções Auxiliares para Validação, Truncate e Insert


# Verifica se a tabela existe no banco DADOS_EXCEL
def table_exists(engine, table_name):
    with engine.connect() as conn:
        return engine.dialect.has_table(conn, table_name)


# Trunca a tabela (caso exista e tenha registros) para evitar duplicidade
def truncate_table(conn, table_name):
    logger.info("Executando TRUNCATE TABLE em %s.", table_name)
    conn.execute(text(f"TRUNCATE TABLE {table_name}"))
    logger.info("TRUNCATE concluído em %s.", table_name)


# Fallback: Deleta todos os registros da tabela (caso exista) para evitar duplicidade
def delete_table(conn, table_name):
    logger.info("Executando DELETE FROM em %s.", table_name)
    conn.execute(text(f"DELETE FROM {table_name}"))
    logger.info("DELETE concluído em %s.", table_name)


# Insere os dados tratados no banco utilizando pandas.to_sql (método append)
def insert_table(df, table_name, engine):
    logger.info("Inserindo os dados tratados no banco na tabela %s.", table_name)
    df.to_sql(
        name=table_name,
        con=engine,
        schema="dbo",
        if_exists="append",
        index=False,
        chunksize=200,
    )


# -------------------------------------------------------------------------------------
