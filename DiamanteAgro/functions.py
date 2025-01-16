from datetime import date
from datetime import date, datetime
import os
import pandas as pd

diretorio_atual = os.path.dirname(os.path.abspath(__file__))

except_colunas = ["Sett. Price", "Delta", "MTM (Eq USD)",'Gamma', 'Vega','Theta', 'Rho', 'Expire Date', 'Delivery Month', "Long", "Short", "Product Type", "Buy/Sell", "Swap/Option", "Ccy", "Underlying", "Trade No."]

meses_nomes = ["Janeiro", "Fevereiro", "Marco", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outrubro", "Novembro", "Dezembro"]

columns = ['Trade No.', 'Swap/Option','Underlying', 'Trade Date', 'Buy/Sell', 'Product Type', 'Ccy', 
               'Delivery Month','Expire Date', 'Strike', 'Notional', 'Long', 'Short', 'Sett. Price', 
               'Delta', 'Gamma', 'Vega','Theta', 'Rho', 'Premium (Eq USD)', 'MTM (Eq USD)']


entradas_del_date = [
                            ("KCH5", "12-02-2025"),
                            ("KCK5", "11-04-2025"),
                            ("KCN5", "12-06-2025"),
                            ("KCU5", "08-08-2025"),
                            ("KCZ5", "12-11-2025"),
                            ("KCH6", "11-02-2026"),
                            ("KCK6", "10-04-2026"),
                            ("KCN6", "12-06-2026"),
                            ("KCU6", "14-08-2026"),
                            ("KCZ6", "12-11-2026"),
                            ("KCH7", "10-02-2027"),
                            ("KCK7", "09-04-2027"),
                            ("KCN7", "11-06-2027"),
                            ("KCU7", "13-08-2027")
                            ]# entradas de codigo de datas

def conta_linhas():
    tamanho = 0
    for mes in meses_nomes: 
        caminho_arquivo = os.path.join(diretorio_atual, f"table_{mes}.csv")
        if os.path.exists(caminho_arquivo):
            dados_mes = pd.read_csv(caminho_arquivo)
            if not dados_mes.empty:        
                tamanho = tamanho + len(dados_mes)
                print(tamanho)
        else:
            pass
    return tamanho

def converte_data_float(raw_date):

    delivery_month_date = datetime.strptime(raw_date, "%d-%m-%Y").date()
        
    ##subtrai o delivery month pela dia de hoje
    data = delivery_month_date - date.today()
    time_in_float = data.days / 365.0
    return time_in_float