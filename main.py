import pandas as pd
from service.tratamento import tratamento_base
from utils.conexao import config
from loader.carga import insert_bd

def etl_tentativas():
    df = tratamento_base()

    engine = config()
    insert_bd(engine, df)

if __name__ == "__main__":
    etl_tentativas()