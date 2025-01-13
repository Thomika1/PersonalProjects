from functions import *
from gregas import *
import pandas as pd
import tkinter as tk
from tkinter import ttk
from pandastable import Table, TableModel
from tkinter import messagebox
import re
import os

class AbaBuySell:
    columns = ['Trade No.', 'Swap/Option','Underlying', 'Trade Date', 'Buy/Sell', 'Product Type', 'Ccy', 
               'Delivery Month','Expire Date', 'Strike', 'Notional', 'Long', 'Short', 'Sett. Price', 
               'Delta', 'Gamma', 'Vega','Theta', 'Rho', 'Premium (Eq USD)', 'MTM (Eq USD)']

    def __init__(self, notebook):
        # Cria o frame da aba
        self.frame = ttk.Frame(notebook)

        self.label = tk.Label(self.frame, text="Extrato")
        self.label.pack(side="top")
        # Frame para os botoe
        self.frame_botao_1 = tk.Frame(self.frame)
        self.frame_botao_1.pack(side="top")

        self.frame_botao_2 = tk.Frame(self.frame)
        self.frame_botao_2.pack(side="top")

        self.frame_botao_3 = tk.Frame(self.frame)
        self.frame_botao_3.pack(side="top")

        # Inicializa a janela adiconar contrato
        

        # Inicializa a tabela principal como DataFrame
        self.table = pd.DataFrame(columns=self.columns)
        self.table_junto = pd.DataFrame(columns=self.columns)
        self.table2 = pd.DataFrame(columns=self.columns)
    

        # Botão para abrir a janela de adição de contrato
        self.botao_adicionar_contrato = tk.Button(self.frame_botao_1, text="Adicionar Contrato", 
                                                  command=self.abrir_janela_adicionar, width=20)
        self.botao_adicionar_contrato.pack(side="left",padx=5,pady=5)
        
        #botão para abrir a janela de exibição das tabelas por mes
        self.botao_excluir_contrato = tk.Button(self.frame_botao_1, text='Excluir contrato',
                                                  command=self.abrir_janela_excluir_contrato, width=20)
        self.botao_excluir_contrato.pack(side = "left",padx=5, pady=5)

        
        # Frame para as entrys
        self.frame_entries = tk.Frame(self.frame_botao_2)
        self.frame_entries.pack(side="top")

        # Entrys para sett price
        self.frame_sett_price = tk.Frame(self.frame_entries)
        self.frame_sett_price.pack(side="left", padx=10)

        self.label_sett_price = tk.Label(self.frame_sett_price, text="Sett Price:")
        self.label_sett_price.pack(side="top", padx=5, pady=5)

        self.entry_sett_price = tk.Entry(self.frame_sett_price)
        self.entry_sett_price.pack(side="top", padx=5, pady=5)

        # Entrys para vol
        self.frame_vol = tk.Frame(self.frame_entries)
        self.frame_vol.pack(side="left", padx=10)

        self.label_vol = tk.Label(self.frame_vol, text="Vol:")
        self.label_vol.pack(side="top", padx=5, pady=5)

        self.entry_vol = tk.Entry(self.frame_vol)
        self.entry_vol.pack(side="top", padx=5, pady=5)
        
        # Frame e botao para atualizar as tabelas
        self.frame_botao_atualizar = tk.Frame(self.frame_botao_3)
        self.frame_botao_atualizar.pack()

        self.botao_atualizar = tk.Button(self.frame_botao_atualizar, text="Atualizar Tabela", command=self.botao_alterar_tabelas_price_vol)
        self.botao_atualizar.pack(padx=5, pady=5)
        

        # Frame para a tabela de swap
        frame_table_swap = tk.Frame(self.frame)
        frame_table_swap.pack(expand=True, fill='both', side="bottom")
        
        # Criação da tabela de swap com filtro
        self.table_swap = Table(frame_table_swap, dataframe=self.table[self.table["Swap/Option"] == "swap"],
                                showtoolbar=True, showstatusbar=True)
        
        # Frame para a tabela de options
        frame_table_option = tk.Frame(self.frame)
        frame_table_option.pack(expand=True, fill='both',side="bottom")
        
        # Criação da tabela de options com filtro
        self.table_option = Table(frame_table_option, dataframe=self.table[self.table["Swap/Option"] == "option"],
                                  showtoolbar=True, showstatusbar=True)
    

        # Carrega e exibe as tabelas
        self.carregar_tabelas()
        self.table_swap.show()
        self.table_option.show()
        
    def botao_alterar_tabelas_price_vol(self):  # Ação do botão para alterar os dados da tabela
        # Lógica para aplicar a volatilidade para a linha
        def logica_apply_mtm(linha):
            time_in_float = converte_data_float(linha["Expire Date"])
            premium = calcula_b_s(float(self.sett_price),float(linha["Strike"]),time_in_float,float(self.vol),dividend=0.0,rate=0.0)

            if linha["Swap/Option"].lower() == "option":  # Apenas para as linhas de "option" 
                if linha["Product Type"].lower() == "call":
                    
                    return round(premium[0]*linha["Notional"]*375, 2)  # Retorna o valor calculado
                else:
                    return round(premium[1]*linha["Notional"]*375, 2)

            elif linha["Swap/Option"].lower() == "swap":
                if linha["Buy/Sell"].lower() == "buy":
                    mtm = int(linha["Notional"])*(float(self.sett_price)-float(linha["Strike"]))*375
                    return round(mtm, 2)
                elif linha["Buy/Sell"].lower() == "sell":
                    mtm = int(linha["Notional"])*(float(linha["Strike"])-float(self.sett_price))*375
                    return round(mtm, 2)

        def logica_apply_delta(linha):
            time_in_float = converte_data_float(linha["Expire Date"])

            if linha["Swap/Option"].lower() == "option":  # Apenas para as linhas de "option"
                premium = calcula_b_s(float(self.sett_price),float(linha["Strike"]),time_in_float,float(self.vol),dividend=0.0,rate=0.0)
                delta = delta_calc(premium[2])

                if linha["Product Type"].lower() == "call":
                    if linha["Buy/Sell"].lower() == "buy":  
                        return round(delta[0]*linha["Notional"], 2)
                    elif linha["Buy/Sell"].lower() == "sell":
                        return round(-delta[0]*linha["Notional"], 2)
                    
                elif linha["Product Type"].lower() == "put":
                    if linha["Buy/Sell"].lower() == "buy":
                        return round(delta[1]*linha["Notional"], 2)
                    elif linha["Buy/Sell"].lower() == "sell":
                        return round(-delta[1]*linha["Notional"], 2)

            elif linha["Swap/Option"].lower() == "swap":
                if linha["Buy/Sell"].lower() == "buy":
                    return round(1*linha["Notional"], 2)
                elif linha["Buy/Sell"].lower() == "sell":
                    return round(-1*linha["Notional"], 2) # Mantém o valor original para swaps

        def logica_apply_gamma(linha):
            time_in_float = converte_data_float(linha["Expire Date"])

            if linha["Swap/Option"].lower() == "option":  # Apenas para as linhas de "option"
                premium = calcula_b_s(float(self.sett_price),float(linha["Strike"]),time_in_float,float(self.vol),dividend=0.0,rate=0.0)
                gamma = gamma_calc(premium[2],float(self.sett_price), float(self.vol), time_in_float)
                
                if linha["Buy/Sell"].lower() == "buy":
                    return round(gamma*linha["Notional"], 2)
                elif linha["Buy/Sell"].lower() == "sell":
                    return round(-gamma*linha["Notional"], 2)

            elif linha["Swap/Option"].lower() == "swap":
                return 0  # Mantém o valor original para swaps

        def logica_apply_vega(linha):
            time_in_float = converte_data_float(linha["Expire Date"])

            if linha["Swap/Option"].lower() == "option":  # Apenas para as linhas de "option"
                premium = calcula_b_s(float(self.sett_price),float(linha["Strike"]),time_in_float,float(self.vol),dividend=0.0,rate=0.0)
                vega = vega_calc(premium[2],float(self.sett_price), time_in_float)
                
                if linha["Buy/Sell"].lower() == "sell":
                    if linha["Product Type"].lower() == "put":
                        return round(-vega*linha["Notional"], 2)
                    else:
                        return round(vega*linha["Notional"], 2)
                else:
                    return round(vega*linha["Notional"], 2)

            elif linha["Swap/Option"].lower() == "swap":
                return 0  # Mantém o valor original para swaps
        
        def logica_apply_theta(linha):
            time_in_float = converte_data_float(linha["Expire Date"])

            if linha["Swap/Option"].lower() == "option":  # Apenas para as linhas de "option"
                premium = calcula_b_s(float(self.sett_price),float(linha["Strike"]),time_in_float,float(self.vol),dividend=0.0,rate=0.0)
                theta = theta_calc(premium[2],premium[3], float(self.sett_price), float(linha["Strike"]), time_in_float, 0.0, float(self.vol))
                
                if linha["Product Type"].lower() == "call":
                    if linha["Buy/Sell"].lower() == "buy":  
                        return round(theta[0]*linha["Notional"], 2)
                    elif linha["Buy/Sell"].lower() == "sell":
                        return round(-theta[0]*linha["Notional"], 2)
                    
                elif linha["Product Type"].lower() == "put":
                    if linha["Buy/Sell"].lower() == "buy":
                        return round(theta[1]*linha["Notional"], 2)
                    elif linha["Buy/Sell"].lower() == "sell":
                        return round(-theta[1]*linha["Notional"], 2)

            elif linha["Swap/Option"].lower() == "swap":
                return 0  # Mantém o valor original para swaps

        def logica_apply_rho(linha):
            time_in_float = converte_data_float(linha["Expire Date"])

            if linha["Swap/Option"].lower() == "option":  # Apenas para as linhas de "option"
                premium = calcula_b_s(float(self.sett_price),float(linha["Strike"]),time_in_float,float(self.vol),dividend=0.0,rate=0.0)
                rho = rho_calc(premium[3], float(linha["Strike"]), time_in_float, 0.0)
                
                if linha["Product Type"].lower() == "call":
                    if linha["Buy/Sell"].lower() == "buy":  
                        return round(rho[0]*linha["Notional"], 2)
                    elif linha["Buy/Sell"].lower() == "sell":
                        return round(rho[0]*linha["Notional"], 2)
                        
                elif linha["Product Type"].lower() == "put":
                    if linha["Buy/Sell"].lower() == "buy":
                        return round(rho[1]*linha["Notional"], 2)
                    elif linha["Buy/Sell"].lower() == "sell":
                        return round(rho[1]*linha["Notional"], 2)

            elif linha["Swap/Option"].lower() == "swap":
                return 0  # Mantém o valor original para swaps


        # Coleta os valores dos inputs de sett price e vol
        self.sett_price = self.entry_sett_price.get()
        self.vol = self.entry_vol.get()

        # Inicializa o DataFrame consolidado (se ainda não foi feito)
        self.table_completa = pd.DataFrame()

        # Atualiza os dados mês a mês
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))

        for mes in meses_nomes:
            caminho_arquivo = os.path.join(diretorio_atual, f"table_{mes}.csv")
            

            if os.path.exists(caminho_arquivo):
                # Carrega o arquivo para atualizar a coluna específica
                dados_mes = pd.read_csv(caminho_arquivo)

                dados_mes["Sett. Price"] = self.sett_price
                #chama as funcoes apply para alterar as colunas especificas
                dados_mes["MTM (Eq USD)"] = dados_mes.apply(logica_apply_mtm, axis=1)  
                dados_mes["Delta"] = dados_mes.astype(object).apply(logica_apply_delta, axis=1)
                dados_mes["Gamma"] = dados_mes.astype(object).apply(logica_apply_gamma, axis=1)
                dados_mes["Vega"] = dados_mes.astype(object).apply(logica_apply_vega, axis=1)
                dados_mes["Theta"] = dados_mes.astype(object).apply(logica_apply_theta, axis=1)
                dados_mes["Rho"] = dados_mes.astype(object).apply(logica_apply_rho, axis=1)
                
                # Salva o arquivo atualizado
                dados_mes.to_csv(caminho_arquivo, index=False)
            else:
                print(f"Arquivo não encontrado para o mês {mes}.")

        for mes in meses_nomes:
            caminho_arquivo = os.path.join(diretorio_atual, f"table_{mes}.csv")
            if os.path.exists(caminho_arquivo):
                dados_mes = pd.read_csv(caminho_arquivo)
                self.table_completa = pd.concat([self.table_completa, dados_mes], ignore_index=True)
            else:
                print(f"Arquivo não encontrado para o mês {mes}.")


        # Atualiza as tabelas da interface gráfica
        if not self.table_completa.empty:
            tabela_swap = self.table_completa[self.table_completa["Swap/Option"].str.lower() == "swap"]
            tabela_option = self.table_completa[self.table_completa["Swap/Option"].str.lower() == "option"]

            self.table_swap.updateModel(TableModel(tabela_swap))
            self.table_swap.redraw()

            self.table_option.updateModel(TableModel(tabela_option))
            self.table_option.redraw()
            
        print("Tabelas atualizadas com sucesso.")

    def abrir_janela_excluir_contrato(self):
        pass
        
        
    #função para abrir a janela com suas respectivas caracteristicas     
    def abrir_janela_adicionar(self):
        # Cria uma nova janela "top-level" que flutua sobre a principal
    
        # Verifica se já existe uma janela aberta com o título "Adicionar Contrato"
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Toplevel) and widget.title() == "Adicionar Contrato":
                widget.lift()  # Traz a janela existente para o topo
                return

        janela_adicionar = tk.Toplevel(self.frame)
        janela_adicionar.title("Adicionar Contrato")

        # Lista de entradas, com um campo de entrada para cada coluna da tabela
        entradas = {}
        
        # Loop para criar labels e entradas para cada coluna da tabela
        for coluna in self.columns:
            if coluna in except_colunas:
                continue  # Pula para a próxima iteração, ignorando as colunas especificadas
            else:
                # Cria um frame para organizar cada label e entrada
                frame_linha = tk.Frame(janela_adicionar)
                frame_linha.pack(fill="x", padx=5, pady=2)

                # Label para a coluna
                label = tk.Label(frame_linha, text=coluna, width=20, anchor="w")
                label.pack(side="left")

                # Campo de entrada para a coluna
                entrada = tk.Entry(frame_linha)
                entrada.pack(side="left", fill="x", expand=True)

                # Armazena a entrada no dicionário
                entradas[coluna] = entrada


        def remove_selection(event):
            # Remove a seleção de texto ao alterar o valor na combobox
           event.widget.selection_clear()

        # Combobox de expire dates
        frame_box_exp = tk.Frame(janela_adicionar)
        frame_box_exp.pack(fill='x', padx=5, pady=2)

        label_del_janela_add = tk.Label(frame_box_exp, text="Expire Date", width=20, anchor="w")
        label_del_janela_add.pack(side="left")

        self.box_del_janela_add = ttk.Combobox(frame_box_exp, values=entradas_del_date, state="readonly")
        self.box_del_janela_add.pack(side="left",fill="x", expand=True)

        # Combobox dos meses
        frame_del_mon = tk.Frame(janela_adicionar)
        frame_del_mon.pack(fill='x', padx=5, pady=2)

        label_del_mon = tk.Label(frame_del_mon, text="Delivery Month", width=20, anchor="w")
        label_del_mon.pack(side='left')

        self.box_del_mon = ttk.Combobox(frame_del_mon, values=meses_nomes, state="readonly")
        self.box_del_mon.pack(side="left",fill="x", expand=True)

        # combobox call e put
        call_put = ["Call", "Put"]
        frame_call_put = tk.Frame(janela_adicionar)
        frame_call_put.pack(fill='x', padx=5, pady=2)

        label_call_put = tk.Label(frame_call_put, text="Producut Type(call/put)", width=20, anchor="w")
        label_call_put.pack(side='left')

        self.box_call_put = ttk.Combobox(frame_call_put, values=call_put, state="readonly")
        self.box_call_put.pack(side="left",fill="x", expand=True)

        # combobox buy e sell
        buy_sell = ["Buy", "Sell"]
        frame_buy_sell = tk.Frame(janela_adicionar)
        frame_buy_sell.pack(fill='x', padx=5, pady=2)

        label_buy_sell = tk.Label(frame_buy_sell, text="Buy/Sell", width=20, anchor="w")
        label_buy_sell.pack(side='left')

        self.box_buy_sell = ttk.Combobox(frame_buy_sell, values=buy_sell, state="readonly")
        self.box_buy_sell.pack(side="left",fill="x", expand=True)

        #combobox swap option
        swap_option = ["Swap", "Option"]
        frame_swap_option = tk.Frame(janela_adicionar)
        frame_swap_option.pack(fill='x', padx=5, pady=2)

        label_swap_option = tk.Label(frame_swap_option, text="Swap/Option", width=20, anchor="w")
        label_swap_option.pack(side='left')

        self.box_swap_option = ttk.Combobox(frame_swap_option, values=swap_option, state="readonly")
        self.box_swap_option.pack(side="left",fill="x", expand=True)

        self.box_del_janela_add.bind("<<ComboboxSelected>>", remove_selection)
        self.box_del_mon.bind("<<ComboboxSelected>>", remove_selection)
        self.box_call_put.bind("<<ComboboxSelected>>", remove_selection)
        self.box_buy_sell.bind("<<ComboboxSelected>>", remove_selection)
        self.box_swap_option.bind("<<ComboboxSelected>>", remove_selection)

        # Função interna para capturar os dados e adicionar à tabela
        def adicionar_contrato():
            # Extrai os valores digitados em cada campo de entrada
            
            # trata as excecoes de fotmato de data
            if not re.fullmatch(r"^\d{2}-\d{2}-\d{4}$", entradas["Trade Date"].get()):
                messagebox.showerror("Erro de Validação", "Data deve estar no formato dd-mm-yy.")
                janela_adicionar.lift()
                return
            
            dados = {coluna: entradas[coluna].get() for coluna in self.columns if coluna not in except_colunas}
            
            # Adiciona os valores exepcionais
            dados["Buy/Sell"] = self.box_buy_sell.get()

            if dados["Buy/Sell"].lower() == "buy":
                dados["Long"] = dados["Notional"]
                dados["Short"] = 0
            elif dados["Buy/Sell"].lower() == "sell":
                dados["Long"] = 0
                dados["Short"] = dados["Notional"]

            dados["Ccy"] = "USD"

            dados["Underlying"] = "KC"
           
            dados["Product Type"] = self.box_call_put.get()

            dados['Delivery Month'] = self.box_del_mon.get()

            dados["Swap/Option"] = self.box_swap_option.get()

            # Independente do que for digitado em premium o valor eh ajustado para 0 no caso swap
            if dados["Swap/Option"].lower() == "swap":
                dados["Premium (Eq USD)"] = 0
            
            data_no_split = self.box_del_janela_add.get()
            data_split = data_no_split.split()
            data_true = data_split[1]
            dados["Expire Date"] = data_true

            # Converte os dados em DataFrame e concatena com self.table
            nova_linha = pd.DataFrame([dados])
            self.table = pd.concat([self.table, nova_linha], ignore_index=True)

            
            # Atualiza as visualizações específicas para swap e option
            self.table_junto = pd.concat([self.table, self.table2], ignore_index=True)
            
            if dados["Swap/Option"].lower() == "swap":
                self.table_swap.updateModel(TableModel(self.table_junto[self.table_junto["Swap/Option"].str.lower() == "swap"]))
                self.table_swap.redraw()
            elif dados["Swap/Option"].lower() == "option":
                self.table_option.updateModel(TableModel(self.table_junto[self.table_junto["Swap/Option"].str.lower() == "option"]))
                self.table_option.redraw()

            self.salvar_tabelas()
            # Fecha a janela após adicionar o contrato
            janela_adicionar.destroy()

        # Botão para adicionar contrato e fechar a janela
        botao_adicionar = tk.Button(janela_adicionar, text="Adicionar", command=adicionar_contrato)
        botao_adicionar.pack(pady=10)

    #função salva as tabelas
    def salvar_tabelas(self):
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    
        # Verifica se a coluna "Delivery Month" existe na tabela
        if "Delivery Month" not in self.table.columns:
            print("A coluna 'Delivery Month' não foi encontrada na tabela.")
            return

        # Agrupa a tabela por mês com base na coluna "Delivery Month"
        for mes, dados_mes in self.table.groupby("Delivery Month"):
            # Define o nome do arquivo com base no número do mês
            nome_arquivo = f"table_{mes}.csv"
            caminho_arquivo = os.path.join(diretorio_atual, nome_arquivo)
            
            # Verifica se o arquivo já existe
            if os.path.exists(caminho_arquivo):
                # Se o arquivo existe, carrega os dados existentes
                dados_existentes = pd.read_csv(caminho_arquivo)
                # Concatena os novos dados com os dados existentes
                dados_mes = pd.concat([dados_existentes, dados_mes])
            
            # Salva o DataFrame (novo ou concatenado) em um arquivo CSV
            dados_mes.to_csv(caminho_arquivo, index=False)
            print(f"Tabela para o mês {mes} salva como {nome_arquivo}.")

    #função para carregar o conteudo das tabelas
    def carregar_tabelas(self):
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))

        # Carrega os arquivos CSV por mês (1 a 12)
        for mes in meses_nomes:
            caminho_arquivo = os.path.join(diretorio_atual, f"table_{mes}.csv")
            
            if os.path.exists(caminho_arquivo):
                #print(f"Carregando dados de: {caminho_arquivo}")
                dados_mes = pd.read_csv(caminho_arquivo)
                self.table2 = pd.concat([self.table2, dados_mes], ignore_index=True)
            else:
                print(f"Arquivo não encontrado para o mês {mes}.")

        if not self.table2.empty:
            # Debug: Exibir os dados carregados
            #print("Dados carregados para 'self.table':")
            #print(self.table.head())

            # Atualiza o modelo para a tabela de swap
            self.table_swap.updateModel(TableModel(self.table2[self.table2["Swap/Option"].str.lower() == "swap"]))
            self.table_swap.redraw()

            # Atualiza o modelo para a tabela de option
            self.table_option.updateModel(TableModel(self.table2[self.table2["Swap/Option"].str.lower() == "option"]))
            self.table_option.redraw()
        else:
            print("Nenhum dado foi carregado; os arquivos CSV mensais podem não existir.")