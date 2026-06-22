import pandas as pd
import logging
from pathlib import Path


logger = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------

def tratamento_base():
    logger.info("Iniciando tratamento do arquivo de origem.")

    df = importa_csv()
    logger.info("Arquivo carregado com %s linhas e %s colunas.", *df.shape)

    df = rename_id_vendedor(df)
    logger.debug("Coluna ID_VENDEDOR ajustada.")

    df = altera_progresso_meta(df)
    logger.debug("Coluna PROGRESSO_META convertida para decimal.")

    df = insere_col_situacao(df)
    logger.debug("Coluna SITUACAO criada.")

    df = reordena(df)
    logger.info("Tratamento finalizado com colunas reorganizadas.")

    return df

# -------------------------------------------------------------------------------------

# Etapa 1 - Importação do CSV
def importa_csv():
    csv_path = Path(__file__).resolve().parents[1] / "base-csv" / "tentativas-dito.csv"

    try:
        logger.info("Lendo CSV de origem em %s.", csv_path)

        df = pd.read_csv(
            csv_path,
            sep=",",
            dtype={
                "id_loja": str,
                "id_vendedor": str,
                "nome_loja": str,
                "nome_vendedor": str,
                "meta_atingida": int,
                "quantidade_total_contatos": int,
                "progresso_meta": float,
            },
        ).rename(
            {
                "id_loja": "ID_LOJA",
                "id_vendedor": "ID_VENDEDOR",
                "nome_loja": "NOME_LOJA",
                "nome_vendedor": "NOME_VENDEDOR",
                "meta_atingida": "META_ATINGIDA",
                "quantidade_total_contatos": "QUANTIDADE_TOTAL_CONTATOS",
                "progresso_meta": "PROGRESSO_META",
            },
            axis=1,
        )

        logger.info("CSV importado com sucesso.")
        return df

    except FileNotFoundError:
        logger.exception("Arquivo CSV não encontrado: %s", csv_path)
        raise
    except Exception:
        logger.exception("Falha ao importar o CSV de origem.")
        raise

# Etapa 2 - Tratamento dos Dados

# Etapa 2.1 - Renomear a Coluna 'id_vendedor' para remover os 9 primeiros caracteres
def rename_id_vendedor(df):
    df['ID_VENDEDOR'] = df['ID_VENDEDOR'].str[9:]

    return df

# Etapa 2.2 - Alterar a Coluna 'progresso_meta' para o formato decimal
def altera_progresso_meta(df):
    df['PROGRESSO_META'] = df['PROGRESSO_META'].div(100).round(6)

    return df
    
# Etapa 2.3 - Inserir a Coluna 'situacao' para identificar vendedores 'Volante'    
def insere_col_situacao(df):
    df['SITUACAO'] = df['ID_VENDEDOR'].duplicated(keep=False).map({True: 'Volante', False: ' '})
    return df

# Etapa 2.4 - Reordenar as Colunas para o formato final
def reordena(df):
    df = df[['ID_LOJA', 'ID_VENDEDOR', 
             'NOME_LOJA', 'NOME_VENDEDOR', 
             'META_ATINGIDA', 'QUANTIDADE_TOTAL_CONTATOS', 
             'SITUACAO', 'PROGRESSO_META'
            ]]
    
    return df

# -------------------------------------------------------------------------------------
