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

```bash
python main.py
```

## O que o tratamento faz

- Renomeia e padroniza o nome das colunas do CSV, transformando todas em maiúsculas.
- Remove os 9 primeiros caracteres do identificador do vendedor, mantendo apenas os 6 dígitos do código de vendedor.
- Converte o progresso da meta para formato decimal (porcentagem).
- Cria a coluna `SITUACAO` para identificar vendedores duplicados (volantes).
- Reordena as colunas antes da carga para ficar no padrão utilizado na planilha do Score.

## Saída esperada

Ao final da execução, os dados tratados devem estar carregados na tabela definida em `TABLE_TENTATIVAS` no arquivo `.env`.

## Observações

- O arquivo de entrada esperado é `base-csv/tentativas-dito.csv`.
- O projeto usa `pandas` para leitura e manipulação dos dados.
- A carga é feita com `SQLAlchemy` e `pyodbc`.

## Próximos passos sugeridos

- Adicionar exemplos do layout do CSV de entrada.
- Documentar a tabela de destino no banco.
- Incluir logs de execução e tratamento de erros mais detalhados.
