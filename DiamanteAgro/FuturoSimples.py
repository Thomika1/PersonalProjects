import pandas as pd
import requests
import yfinance as yf
import datetime
from requests.exceptions import ConnectionError

def create_df():  # Cria um DataFrame vazio 
    columns = ['type_', 'start', 'exp_date', 'exercise_price', 'swap_value', 'strike_swap', 'reward', 'position', 'market']
    return pd.DataFrame(columns=columns)

def refactor_types(contract): # corrige os tipos de dado do data frame
    contract['type_'] = contract['type_'].astype('string')
    contract['start'] = pd.to_datetime(contract['start'],format='%d-%m-%Y')
    contract['exp_date'] = pd.to_datetime(contract['exp_date'],format='%d-%m-%Y')
    contract['exercise_price'] = contract['exercise_price'].astype('float64')
    contract['swap_value'] = contract['swap_value'].astype('float64')
    contract['strike_swap'] = contract['strike_swap'].astype('float64')
    contract['reward'] = contract['reward'].astype('float64')
    contract['position'] = contract['position'].astype('string')
    contract['market'] = contract['market'].astype('string')

def get_date_input(prompt): # coleta os inputs de data no formato correto
    while True:
        date_str = input(prompt)
        try:
            date_value = pd.to_datetime(date_str, format="%d-%m-%Y")
            
            return date_value
        except ValueError:
            print("Formato de data inválido. Por favor, use o formato DD-MM-YYYY.")
            
    
def inputs(contract):
    
    while True:  # Loop para preencher um input
        # Solicitar dados ao usuário
        opcao = input("Deseja inserir um contrato?\nDigite uma das opções numéricas:\n1 - sim\n2 - não\ninput: ")
        if opcao == '2':
            print("Saindo do menu.")
            break  # Sai do loop se o usuário digitar '2'
        
        type_ = input("Digite o Tipo: ")
        print("Digite a data no formato DD-MM-YYYY:1\n")
        start = get_date_input("Digite o Início: ")
        exp_date = get_date_input("Digite a Data de Expiração: ")
        exercise_price = input("Digite o Preço de Exercício: ")
        swap_value = input("Digite o Valor de Swap: ")
        strike_swap = input("Digite o Strike Swap: ")
        reward = input("Digite a Recompensa: ")
        position = input("Digite a Posição: ")
        market = input("Digite o Mercado: ")

        # Criar um dicionário com os dados
        new_row = {
            'type_': type_,
            'start': start,
            'exp_date': exp_date,
            'exercise_price': exercise_price,
            'swap_value': swap_value,
            'strike_swap': strike_swap,
            'reward': reward,
            'position': position,
            'market': market
        }

        # Adicionar a nova linha ao DataFrame usando pd.concat
        contract = pd.concat([contract, pd.DataFrame([new_row])], ignore_index=True)
   
    # Exibir o DataFrame após sair do loop
    print(contract.to_markdown())

###############################   


def main():
    contract = create_df()
    contract = refactor_types(contract)
    inputs(contract)

if __name__ == "__main__":
    main()
