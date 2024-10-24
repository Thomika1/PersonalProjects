import pandas as pd

def create_df():
    columns = ['Trade No.', 'Underlying', 'Trade Date', 'Buy/Sell', 'Product Type', 'Ccy', 
               'Delivery Month', 'Expire Date', 'Strike', 'Notional', 'Short', 'Sett. Price', 
               'Delta', 'Premium (Eq USD)', 'MTM (Eq USD)']
    return pd.DataFrame(columns=columns)

def refactor_types(contract): # corrige os tipos de dado do data frame
    contract['Trade No.'] = contract['Trade No.'].astype('string')
    contract['Underlying'] = contract['Underlying'].astype('string')
    contract['Trade Date'] = pd.to_datetime(contract['Trade Date'],format='%d-%m-%Y')
    contract['Buy/Sell'] = contract['Buy/Sell'].astype('string')
    contract['Product Type'] = contract['Product Type'].astype('string')
    contract['Ccy'] = contract['Ccy'].astype('string')
    contract['Delivery Month'] = pd.to_datetime(contract['Delivery Month'],format='%d-%m-%Y')
    contract['Expire Date'] = pd.to_datetime(contract['Expire Date'],format='%d-%m-%Y')
    contract['Strike'] = contract['Strike'].astype('float64')
    contract['Notional'] = contract['Notional'].astype('int64')
    contract['Short'] = contract['Short'].astype('int64')
    contract['Sett. Price'] = contract['Sett. Price'].astype('float64')
    contract['Delta'] = contract['Delta'].astype('float64')
    contract['Premium (Eq USD)'] = contract['Premium (Eq USD)'].astype('float64')
    contract['MTM (Eq USD)'] = contract['MTM (Eq USD)'].astype('float64')
    return contract

def get_date_input(prompt): # coleta os inputs de data no formato correto
    print("Digite a data no formato DD-MM-YYYY:")
    while True:
        date_str = input(prompt)
        try:
            date_value = pd.to_datetime(date_str, format="%d-%m-%Y").date()
            return date_value
        except ValueError:
            print("Formato de data inválido. Por favor, use o formato DD-MM-YYYY.")

def get_date_input_mon(prompt): # coleta os inputs de data no formato correto
    print("Digite a data no formato MM-YYYY")
    while True:
        date_str = input(prompt)
        try:
            date_value = pd.to_datetime(date_str, format="%m-%Y").date()
            return date_value
        except ValueError:
            print("Formato de data inválido. Por favor, use o formato MM-YYYY.")
              
def get_float_input(prompt):# coleta os inputs de floats no formato correto
    while True:
        float_str = input(prompt)
        try:
            float_value = float(float_str)
            return float_value
        except ValueError:
            print("formato de valor incorreto. Por favor, use números e '.' como separador decimal.")
    
def get_int_input(prompt):# coleta os inputs de inteiros no formato correto
    while True:
        int_str = input(prompt)
        try:
            int_value = int(int_str)
            return int_value
        except ValueError:
            print("Formato de valor incorreto. Por favor, use números inteiros!")
    
def inputs_contract(contract, n): # recebe os inputs do dados do csv
    
    while True:
        #trade_num = input("Digite o trade number: ")
        underl = input("Digite o Underlying: ")
        trade_date = get_date_input("Digite a data de trade: ")
        buy_sell = input("Digite se a operação foi buy ou sell: ")
        product_type = input("Digite o tipo do produto: ")
        ccy = input("Digite a moeda: ")
        deliv_mon = get_date_input_mon("Digite o mês e ano de entrega: ")
        expire_date = get_date_input("Digite a data de expiração: ")
        strike = get_float_input("Digite o strike: ")
        notional = get_int_input("Digite o Notional: ")
        short = get_int_input("Digite o Short: ")
        sett_price = get_float_input("Digite o preço estabelecido: ")
        delta = get_float_input("Digite o Delta: ")
        premium = get_float_input("Digite o Prêmio: ")
        mtm = get_float_input("Digite o MTM: ")

        n = n + 1

        new_row = {
            'Trade No.': n,
            'Underlying': underl,
            'Trade Date': trade_date,
            'Buy/Sell': buy_sell,
            'Product Type': product_type,
            'Ccy': ccy,
            'Delivery Month': deliv_mon,
            'Expire Date': expire_date,
            'Strike': strike,
            'Notional': notional,
            'Short': short,
            'Sett. Price': sett_price,
            'Delta': delta,
            'Premium (Eq USD)': premium,
            'MTM (Eq USD)': mtm
        }

        # Adicionar a nova linha ao DataFrame
        contract = pd.concat([contract, pd.DataFrame([new_row])], ignore_index=True)

        opcao = input("Deseja inserir outro contrato?\nDigite uma das opções numéricas:\n1 - sim\n2 - não\ninput: ")
        if opcao == '2':
            print("Saindo do menu de contratos.")
            break  # Sai do loop se o usuário digitar '2'

    return contract

def convert_to_csv(contract, nome): # converte o data frame para csv
    contract.to_csv(nome, index=True)

def menu(n): # menu de opções
    contract_buy = create_df()
    contract_sell = create_df()

    while True:
        print("\nMenu de Contratos:")
        print("1 - Inserir contrato de Buy")
        print("2 - Inserir contrato de Sell")
        print("3 - Exportar contratos para CSV")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '0':
            print("Saindo do menu.")
            break
        elif opcao == '1':
            contract_buy = inputs_contract(contract_buy,n)
        elif opcao == '2':
            contract_sell = inputs_contract(contract_sell,n)
        elif opcao == '3':
            nome_sell = input('Digite o nome do arquivo sell: ') + '.csv'
            nome_buy = input('Digite o nome do arquivo buy: ') + '.csv'
            convert_to_csv(contract_sell, nome_sell)
            convert_to_csv(contract_buy, nome_buy)
            print("Contratos exportados com sucesso!")
        else:
            print("Opção inválida. Tente novamente.")

def main():
    n = 0
    menu(n)

if __name__ == "__main__":
    main()