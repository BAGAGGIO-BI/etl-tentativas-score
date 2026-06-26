import pandas as pd
import logging
from pathlib import Path
from src.pipeline.extraction import importa_csv

logger = logging.getLogger(__name__)

# Função Principal de Tratamento de Base ----------------------------------------------


def tratamento_base(df):
    logger.info("Iniciando tratamento do arquivo de origem.")

    df = rename_id_vendedor(df)
    logger.debug("Coluna ID_VENDEDOR ajustada.")

    df = altera_progresso_meta(df)
    logger.debug("Coluna PROGRESSO_META convertida para decimal.")

    df = insere_col_situacao(df)
    logger.debug("Coluna SITUACAO criada.")

    df = reordena(df)
    logger.info("Tratamento finalizado com colunas reorganizadas.")

    return df


# Funções de Tratamento ---------------------------------------------------------------

# Etapa 2 - Tratamento dos Dados


# Etapa 2.1 - Renomear a Coluna 'id_vendedor' para remover os 9 primeiros caracteres
def rename_id_vendedor(df):
    df["ID_VENDEDOR"] = df["ID_VENDEDOR"].str[9:]

    return df


# Etapa 2.2 - Alterar a Coluna 'progresso_meta' para o formato decimal
def altera_progresso_meta(df):
    df["PROGRESSO_META"] = df["PROGRESSO_META"].div(100).round(6)

    return df


# Etapa 2.3 - Inserir a Coluna 'situacao' para identificar vendedores 'Volante'
def insere_col_situacao(df):
    df["SITUACAO"] = (
        df["ID_VENDEDOR"].duplicated(keep=False).map({True: "Volante", False: " "})
    )
    return df


# Etapa 2.4 - Reordenar as Colunas para o formato final
def reordena(df):
    df = df[
        [
            "ID_LOJA",
            "ID_VENDEDOR",
            "NOME_LOJA",
            "NOME_VENDEDOR",
            "META_ATINGIDA",
            "QUANTIDADE_TOTAL_CONTATOS",
            "SITUACAO",
            "PROGRESSO_META",
        ]
    ]

    return df


# -------------------------------------------------------------------------------------
