import os

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

# 1. Inserção no Banco de Dados -------------------------------------------------------

# 1.1 - Estabelece a conexão e insere os Dados tratados no banco
def insert_bd(engine, df):

    # Identifica a Tabela do Banco
    TABLE = os.getenv("TABLE_TENTATIVAS")

    try:
        # Operação de verificação e truncate dentro de transação
        with engine.begin() as conn:

            # 1 - Checar se tabela existe
            exists = table_exists(engine, TABLE)

            # 2 - Checar quantidade de registros 
            if exists:
                qtd = conn.execute(text(f"SELECT COUNT(1) FROM {TABLE}")).scalar()

                if qtd and qtd > 0:
                    try:
                        truncate_table(conn, TABLE)
                    except Exception as e_trunc:
                        
                        print(f"\t- Falha ao truncar a tabela {TABLE}:", e_trunc)
                        print("\t- Tentando fallback com DELETE...")

                        try:
                            delete_table(conn, TABLE)
                        except Exception as e_delete:
                            print(f"\t- Falha ao deletar os registros da tabela {TABLE}:", e_delete)
                            raise
            else:
                print(f"\t- Tabela {TABLE} não existe.")

        print("\t- Iniciando carga.")

        # 3 - Inserir com pandas.to_sql (append)
        insert_table(df, TABLE, engine)

        print("\t- Carga concluída.")

    # Tratamento de Exceção - Biblioteca SQL Alchemy
    except SQLAlchemyError as sae:
        print("\t- Erro SQLAlchemy:", sae)
        raise

    # Tratamento de Exceção - Outro Erro
    except Exception as e:
        print("\t- Erro geral:", e)
        raise

    print("\n\t---------------------------\n")


# -------------------------------------------------------------------------------------

# Funções Auxiliares para Verificação, Truncate e Insert

# Verifica se a tabela existe no banco DADOS_EXCEL
def table_exists(engine, table_name):
    exists = engine.dialect.has_table(engine.connect(), table_name)
    return exists

# Trunca a tabela (caso exista e tenha registros) para evitar duplicidade
def truncate_table(conn, table_name):
    print("Executando TRUNCATE TABLE...")
    conn.execute(text(f"TRUNCATE TABLE {table_name}"))
    print("TRUNCATE concluído.")

# Fallback: Deleta todos os registros da tabela (caso exista) para evitar duplicidade
def delete_table(conn, table_name):
    print("Fallback: Executando DELETE FROM...")
    conn.execute(text(f"DELETE FROM {table_name}"))
    print("DELETE concluído.")

# Insere os dados tratados no banco utilizando pandas.to_sql (método append)
def insert_table(df, table_name, engine): 
    print("Inserindo os dados tratados no banco...")
    df.to_sql(
        name=table_name,
        con=engine,
        schema="dbo",
        if_exists="append",
        index=False,
        chunksize=200
    )

# -------------------------------------------------------------------------------------
