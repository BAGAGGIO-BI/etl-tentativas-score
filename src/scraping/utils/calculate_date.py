from datetime import datetime, timedelta

def calcular_datas():
    # Data Inicio (Dia 26 do mês passado) no formato 'YYYY-MM-DD'
    
    dt_inicio = (datetime.now()).replace(day=26).replace(month=datetime.now().month - 1).strftime('%Y-%m-%d')

    # Data Fim (Ontem) no formato 'YYYY-MM-DD'

    # Caso seja exportado até o dia 26, será pego o dia anterior
    if datetime.now().day <= 26:
        dt_fim = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    # Caso seja exportado após o dia 26, será pego o dia 26 do mês atual    
    else:
        dt_fim = (datetime.now()).replace(day=26).strftime('%Y-%m-%d')

    print(f"Data de Início: \t{dt_inicio}")
    print(f"Data de Fim: \t\t{dt_fim}")

    return dt_inicio, dt_fim