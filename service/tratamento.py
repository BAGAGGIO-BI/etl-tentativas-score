import pandas as pd

# -------------------------------------------------------------------------------------

def tratamento_base():
    df = importa_csv()
    df = rename_id_vendedor(df)
    df = altera_progresso_meta(df)
    df = insere_col_situacao(df)
    df = reordena(df)

    return df

# -------------------------------------------------------------------------------------

# Etapa 1 - Importação do CSV
def importa_csv():
    df = pd.read_csv('./base-csv/tentativas-dito.csv',
                    sep=',',                                    
                    dtype={'id_loja':                    str,
                            'id_vendedor':               str,
                            'nome_loja':                 str,
                            'nome_vendedor':             str,
                            'meta_atingida':             int,
                            'quantidade_total_contatos': int,
                            'progresso_meta':            float
                        }
                    ).rename(
                        {'id_loja': 'ID_LOJA',
                         'id_vendedor': 'ID_VENDEDOR',
                         'nome_loja': 'NOME_LOJA',
                         'nome_vendedor': 'NOME_VENDEDOR',
                         'meta_atingida': 'META_ATINGIDA',
                         'quantidade_total_contatos': 'QUANTIDADE_TOTAL_CONTATOS',
                         'progresso_meta': 'PROGRESSO_META'
                        }, axis=1
                    )
    
    return df

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
