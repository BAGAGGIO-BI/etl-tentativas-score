# ETL Tentativas Score

Projeto de ETL em Python para tratar o arquivo CSV de tentativas e carregar os dados em uma tabela do SQL Server.

O arquivo deve ser exportado do App Dito na Aba de 'Resultado das Metas', aplicando o filto de data para o período e o agrupamento por vendedores. Além disso, o arquivo deve ser salvo com o nome `tentativas-dito.csv`.

## Visão geral

O fluxo principal do projeto é:

1. Ler o arquivo CSV de origem em `base-csv/`.
2. Aplicar tratamentos e padronizações nas colunas.
3. Montar a conexão com o banco de dados usando variáveis de ambiente.
4. Limpar a tabela de destino.
5. Inserir os dados tratados no banco.

## Estrutura do projeto

```text
main.py                 # Ponto de entrada da aplicação
service/tratamento.py   # Regras de tratamento do CSV
utils/conexao.py        # Configuração da conexão com o banco
loader/carga.py         # Rotinas de carga no banco
base-csv/               # Arquivos de origem
```

## Requisitos

- Python 3.x
- Acesso a um banco SQL Server
- Driver ODBC compatível com SQL Server

## Instalação

1. Crie e ative um ambiente virtual.
```bash
python -m venv .venv
```
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env` na raiz do projeto com base no `.env.example` e preencha as variáveis abaixo:

```env
DB_USER=
DB_PASSWORD=
DB_SERVER=
DB_DATABASE=
DB_DRIVER=
TABLE_TENTATIVAS=
```

## Execução

Para executar o ETL:

1. Iniciar o venv
```bash
.venv\Scripts\activate
```

2. Rodar o script main
```bash
python main.py
```

3. Desativar o venv ao fim da execução
```bash
deactivate
```

## O que o tratamento faz

- Renomeia e padroniza o nome das colunas do CSV, transformando todas em maiúsculas.
- Remove os 9 primeiros caracteres do identificador do vendedor, mantendo apenas os 6 dígitos do código de vendedor.
- Converte o progresso da meta para formato decimal (porcentagem).
- Cria a coluna `SITUACAO` para identificar vendedores duplicados (volantes).
- Reordena as colunas antes da carga para ficar no padrão utilizado na planilha do Score.

## Layout do CSV de entrada

O arquivo `.csv` bruto que foi exportado da Dito deverá contar com a seguinte estrutura : 

| Coluna | Tipo | Exemplo | Descrição |
|--------|------|---------|-----------|
| id_loja | string | 01234567 | Identificador da loja (padrão Dito) |
| id_vendedor | string | 012345 | ID com 14 caracteres (será truncado para 6) |
| nome_loja | string | Bagaggio Rua Freguesia | Nome amigável da loja |
| nome_vendedor | string | JOAO DA SILVA | Nome do vendedor |
| meta_atingida | inteiro | 617 | Quantidade de contatos realizados no período |
| quantidade_total_contatos | inteiro | 540 | Meta de contatos |
| progresso_meta | float | 114.259259 | Porcentagem da meta atingida (será convertido para 1.142593) |

Atenção aos seguintes pontos : 

- 
- A porcentagem da meta atingida poderá ser maior do que 100% (como sinalizado na Tabela acima), porém o valor normal geralmente é menor do que 100%.

## Estrutura da tabela de destino

A tabela definida em `TABLE_TENTATIVAS` deverá ter a seguinte estrutura:

```sql
CREATE TABLE [dbo].[TABLE_TENTATIVAS] (
    [ID_LOJA]   					CHAR(8)			NOT NULL,
    [ID_VENDEDOR]   				CHAR(6)			NOT NULL,
    [NOME_LOJA] 					VARCHAR(255)	NOT NULL,
    [NOME_VENDEDOR] 				VARCHAR(255)	NOT NULL,
    [META_ATINGIDA] 				INT				NOT NULL,
    [QUANTIDADE_TOTAL_CONTATOS] 	INT				NOT NULL,
    [SITUACAO]  					VARCHAR(7)		NOT NULL,
    [PROGRESSO_META]    			DECIMAL(6,5)    NOT NULL
);
```

| Coluna | Tipo | Descrição |
|--------|------| -----------|
| ID_LOJA | CHAR(8) | Identificador único da loja (padrão Dito) |
| ID_VENDEDOR | CHAR(6) | Código do vendedor (6 dígitos após tratamento) |
| NOME_LOJA | VARCHAR(255) | Nome amigável da loja |
| NOME_VENDEDOR | VARCHAR(255) | Nome do vendedor |
| META_ATINGIDA | INT | Total de contatos realizados no período |
| QUANTIDADE_TOTAL_CONTATOS | INT | Meta de contatos mensal |
| SITUACAO | VARCHAR(7) | 'Volante' se duplicado, ' ' se único |
| PROGRESSO_META | DECIMAL(6,5) | Progresso em formato decimal (0.000000 a 3.000000) |

## Saída esperada

Ao final da execução, os dados tratados devem estar carregados na tabela definida em `TABLE_TENTATIVAS` no arquivo `.env`.

## Observações

- O arquivo de entrada esperado é `base-csv/tentativas-dito.csv`.
- O projeto usa `pandas` para leitura e manipulação dos dados.
- A carga é feita com `SQLAlchemy` e `pyodbc`.

## Logging e observabilidade

O projeto usa uma configuração central de logs em `utils/logging_config.py`.

Por padrão, a execução gera saída no console e também grava um arquivo em `logs/etl_tentativas_score.log`.

As variáveis abaixo podem ser usadas para ajustar o comportamento:

```env
LOG_LEVEL=INFO
LOG_DIR=logs
```

Cada módulo emite seus próprios eventos, o que ajuda a localizar falhas por etapa:

- `service/tratamento.py`: leitura e transformação do CSV.
- `utils/conexao.py`: criação da conexão e teste do banco.
- `loader/carga.py`: limpeza da tabela e inserção dos dados.
- `main.py`: início, fim e captura de exceções do fluxo completo.

## Próximos passos sugeridos

- Adicionar exemplos do layout do CSV de entrada.
- Documentar a tabela de destino no banco.
- Incluir logs de execução e tratamento de erros mais detalhados.
