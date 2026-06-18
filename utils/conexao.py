import os
import urllib
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# 1. Configuração do Ambiente ---------------------------------------------------------

def config():

    server, database, user, password, driver = config_dotenv()

    # Monta a string ODBC de forma segura
    odbc_str = (
        f"driver={{{driver}}};"
        f"server={server};"
        f"database={database};"
        f"UID={user};"
        f"PWD={password};"
        "TrustServerCertificate=yes;"
    )

    # Codificação de Texto com Caracteres Especiais
    params = urllib.parse.quote_plus(odbc_str)

    # Cria engine (fast_executemany melhora performance em inserts via pyodbc)
    engine = create_engine(
        f"mssql+pyodbc:///?odbc_connect={params}", fast_executemany=True
    )

    testeConexao(engine)

    return engine

# 2. Funções Auxiliares de Conexão e Inserção -----------------------------------------

# 2.1. Teste de Conexão com o Banco (antes de INSERT ou TRUNCATE) ---------------------
def testeConexao(engine):
    try:
        # Testar Conexão (Query teste)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1")).fetchone()
        print("\n- Conexão teste OK.")
    except Exception as e:
        print("- Falha ao conectar no banco:", e, "\n")
        raise

# 2.2. Configuração do Ambiente a partir do .env --------------------------------------
def config_dotenv():

    # Carrega os Dados da .env em variáveis
    load_dotenv(".env")

    # Associa as variáveis de ambiente com as variáveis locais
    server      = os.getenv("DB_SERVER")
    database    = os.getenv("DB_DATABASE")
    user        = os.getenv("DB_USER")
    password    = os.getenv("DB_PASSWORD")
    driver      = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")

    # Tratamento de Erro para a Conexão com o Banco
    if not all([server, database, user, password]):
        raise EnvironmentError(
            "- Sem Variáveis de Conexão. Verifique .env ou variáveis de ambiente.\n"
        )

    return server, database, user, password, driver
