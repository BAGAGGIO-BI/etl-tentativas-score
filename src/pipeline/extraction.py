import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------

# Etapa 1 - Importação do CSV
def importa_csv():
    csv_path = Path(__file__).resolve().parents[2] / "data" / "tentativas-dito.csv"

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

# -------------------------------------------------------------------------------------
