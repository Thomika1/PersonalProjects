import pandas as pd
import tkinter as tk
from tkinter import ttk
from pandastable import Table, TableModel
import os
from math import log, e
from scipy import stats
from datetime import date
import numpy as np
from datetime import date, datetime

pd.set_option('future.no_silent_downcasting', True)

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

class SistemaGUI:
    def __init__(self, root):
        # Configurações gerais da interface principal
        self.root = root
        self.root.title("Sistema de Gestão Financeira")
        
        largura = self.root.winfo_screenwidth()
        altura = self.root.winfo_screenheight()
        self.root.geometry(f"{largura}x{altura}+0+0")

        # Criação do notebook para organizar as abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        # Instancia as abas e adiciona ao notebook
        self.aba1 = AbaBuySell(self.notebook)
        self.aba2 = AbaPrecosMercado(self.notebook)
        self.aba3 = AbaCalculoPL(self.notebook)
        
        # Adiciona as abas ao notebook
        self.notebook.add(self.aba1.frame, text="Buy/Sell")
        self.notebook.add(self.aba2.frame, text="Preços de Mercado")
        self.notebook.add(self.aba3.frame, text="Cálculo de P&L")
        
        # Configura o evento de fechamento da janela
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_programa)

    def fechar_programa(self):
        # Salva as tabelas antes de fechar
        #self.aba1.salvar_tabelas()
        self.root.destroy()

def converte_data_float(raw_date):

    delivery_month_date = datetime.strptime(raw_date, "%d-%m-%Y").date()
        
    ##subtrai o delivery month pela dia de hoje
    data = delivery_month_date - date.today()
    time_in_float = data.days / 365.0
    return time_in_float

class AbaBuySell:
    columns = ['Trade No.', 'Swap/Option','Underlying', 'Trade Date', 'Buy/Sell', 'Product Type', 'Ccy', 
               'Delivery Month', 'Expire Date', 'Strike', 'Notional', 'Long', 'Short', 'Sett. Price', 
               'Delta', 'Gamma', 'Vega','Theta', 'Rho', 'Premium (Eq USD)', 'MTM (Eq USD)']

    def __init__(self, notebook):
        self.table_completa = pd.DataFrame()
        # Cria o frame da aba
        self.frame = ttk.Frame(notebook)

        self.label = tk.Label(self.frame, text="Aba swap/options")
        self.label.pack(side="top")
        # Frame para os botoe
        self.frame_botao_1 = tk.Frame(self.frame)
        self.frame_botao_1.pack(side="top")

        self.frame_botao_2 = tk.Frame(self.frame)
        self.frame_botao_2.pack(side="top")

        self.frame_botao_3 = tk.Frame(self.frame)
        self.frame_botao_3.pack(side="top")

        # Inicializa a tabela principal como DataFrame
        self.table = pd.DataFrame(columns=self.columns)
        self.table_junto = pd.DataFrame(columns=self.columns)
        self.table2 = pd.DataFrame(columns=self.columns)
    

        # Botão para abrir a janela de adição de contrato
        self.botao_adicionar_contrato = tk.Button(self.frame_botao_1, text="Adicionar Contrato", 
                                                  command=self.abrir_janela_adicionar, width=20)
        self.botao_adicionar_contrato.pack(side="left",padx=5,pady=5)
        
        #botão para abrir a janela de exibição das tabelas por mes
        self.botao_exibir_tabelas_mes = tk.Button(self.frame_botao_1, text='Abrir exibição por mẽs',
                                                  command=self.abrir_janela_exibicao_mes, width=20)
        self.botao_exibir_tabelas_mes.pack(side = "left",padx=5, pady=5)

        
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
        def logica_apply(linha):
            time_in_float = converte_data_float(linha["Expire Date"])
            
            if linha["Swap/Option"].lower() == "option":  # Apenas para as linhas de "option"
                premium = calcula_b_s(
                    float(self.sett_price),
                    float(linha["Strike"]),
                    time_in_float,
                    float(self.vol),
                    dividend=0.0,
                    rate=0.0
                )
                return premium[1]  # Retorna o valor calculado
            elif linha["Swap/Option"].lower() == "swap":
                return linha["MTM (Eq USD)"]  # Mantém o valor original para swaps

        # Coleta os valores dos inputs de sett price e vol
        self.sett_price = self.entry_sett_price.get()
        self.vol = self.entry_vol.get()

        # Inicializa o DataFrame consolidado (se ainda não foi feito)
        if not hasattr(self, "table_completa"):
            self.table_completa = pd.DataFrame()

        # Atualiza os dados mês a mês
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        for mes in range(1, 13):
            caminho_arquivo = os.path.join(diretorio_atual, f"table_{mes}.csv")
            
            if os.path.exists(caminho_arquivo):
                # Carrega o arquivo para atualizar a coluna específica
                dados_mes = pd.read_csv(caminho_arquivo)
                dados_mes["MTM (Eq USD)"] = dados_mes.apply(logica_apply, axis=1)  # Atualiza a coluna
                # Salva o arquivo atualizado
                dados_mes.to_csv(caminho_arquivo, index=False)

                # Atualiza o DataFrame completo sem duplicar
                if self.table_completa.empty:
                    self.table_completa = dados_mes
                else:
                    # Atualiza somente as linhas que pertencem ao mês atual
                    self.table_completa.update(dados_mes)
            else:
                print(f"Arquivo não encontrado para o mês {mes}.")

        # Atualiza as tabelas da interface gráfica
        tabela_swap = self.table_completa[self.table_completa["Swap/Option"].str.lower() == "swap"]
        tabela_option = self.table_completa[self.table_completa["Swap/Option"].str.lower() == "option"]

        self.table_swap.updateModel(TableModel(tabela_swap))
        self.table_swap.redraw()

        self.table_option.updateModel(TableModel(tabela_option))
        self.table_option.redraw()

        print("Tabelas atualizadas com sucesso.")

    def abrir_janela_exibicao_mes(self):
        #lista de valores
        mes_list = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
        
        #caminho dos arquivos
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        
        #cria a janela para exibir as tabelas
        janela_exibicao_mes = tk.Toplevel(self.frame)
        janela_exibicao_mes.title("Tabelas por mês")

        
        #definindo o tamanho da janela
        janela_exibicao_mes.geometry("1920x1080")
        
        #frame para o botao e as combobox
        frame_botao = tk.Frame(janela_exibicao_mes)
        frame_botao.pack(expand=True, fill='both')
        

        frame_mes1 = tk.LabelFrame(janela_exibicao_mes, text="Mês 1")
        frame_mes1.pack(side="left", expand=True, fill="both")  # Ajustar para 'side="left"'

        frame_mes2 = tk.LabelFrame(janela_exibicao_mes, text="Mês 2")
        frame_mes2.pack(side="right", expand=True, fill="both")  # Ajustar para 'side="right"'
            
        
        #combobox com o valores e posição 
        box_mes1 = ttk.Combobox(frame_botao, values=mes_list)
        box_mes1.pack(pady=5)
        
        box_mes2 = ttk.Combobox(frame_botao, values=mes_list)
        box_mes2.pack(pady=5)
        
        def exibe_tabelas(): #filtrar os valores e salvar
            # Mapeamento dos meses por nome para número
            meses = {
                "Janeiro": "1",
                "Fevereiro": "2",
                "Março": "3",
                "Abril": "4",
                "Maio": "5",
                "Junho": "6",
                "Julho": "7",
                "Agosto": "8",
                "Setembro": "9",
                "Outubro": "10",
                "Novembro": "11",
                "Dezembro": "12"
            } # dicionario para mapear os meses
            
            # Obter os meses selecionados
            mes1 = box_mes1.get()
            mes2 = box_mes2.get()
            
            # Converter o nome do mês para o número correspondente
            mes1_num = meses[mes1]
            mes2_num = meses[mes2]
            
            caminho_arquivo_mes1 = os.path.join(diretorio_atual, f"table_{mes1_num}.csv")
            caminho_arquivo_mes2 = os.path.join(diretorio_atual, f"table_{mes2_num}.csv")
    
            
            # Carregar os arquivos CSV correspondentes
            df_mes1 = pd.read_csv(caminho_arquivo_mes1)
            df_mes2 = pd.read_csv(caminho_arquivo_mes2)
            
                
            #POSSO USAR SELF_TABLE_JUNTO PARA QUE ATUALIZE SEMPRE 
            
            table_p_concat_mes1 = self.table[self.table["Delivery Month"] == mes1]
            df_mes1_concat = pd.concat([table_p_concat_mes1, df_mes1], ignore_index=True)
            
            table_p_concat_mes2 = self.table[self.table["Delivery Month"] == mes2]
            df_mes2_concat = pd.concat([table_p_concat_mes2, df_mes2], ignore_index=True)
            
            
            # Filtrar e exibir as tabelas para cada tipo (Swap e Option) separadamente
            # Para o mês 1
            df_mes1_swap = df_mes1_concat[df_mes1["Swap/Option"] == "swap"]
            df_mes1_option = df_mes1_concat[df_mes1["Swap/Option"] == "option"]
            
            # Para o mês 2
            df_mes2_swap = df_mes2_concat[df_mes2["Swap/Option"] == "swap"]
            df_mes2_option = df_mes2_concat[df_mes2["Swap/Option"] == "option"]
            
            
            # Exibir as tabelas em frames diferentes para cada categoria e mês
            table_mes1_swap = Table(frame_table_mes1_swap, dataframe=df_mes1_swap, showtoolbar=True, showstatusbar=True)
            table_mes1_option = Table(frame_table_mes1_option, dataframe=df_mes1_option, showtoolbar=True, showstatusbar=True)
            table_mes2_swap = Table(frame_table_mes2_swap, dataframe=df_mes2_swap, showtoolbar=True, showstatusbar=True)
            table_mes2_option = Table(frame_table_mes2_option, dataframe=df_mes2_option, showtoolbar=True, showstatusbar=True)
            
            # Atualizar as tabelas na interface
            table_mes1_swap.show()
            table_mes1_option.show()
            table_mes2_swap.show()
            table_mes2_option.show()
        
        
        #cria botao para gerar as tabelas filtradas
        botao_exibe_tabelas_mes = tk.Button(frame_botao, text = 'Exibir Tabelas',command=exibe_tabelas)
        botao_exibe_tabelas_mes.pack(pady=5)
        
        #cria o frame para inserir a Table
        frame_table_mes1_swap = tk.LabelFrame(frame_mes1,text='Swap')
        frame_table_mes1_swap.pack(expand=True, fill='both')
        
        frame_table_mes1_option = tk.LabelFrame(frame_mes1,text='Option')
        frame_table_mes1_option.pack(expand=True, fill='both')
        
        frame_table_mes2_swap = tk.LabelFrame(frame_mes2,text='Swap')
        frame_table_mes2_swap.pack(expand=True, fill='both')
        
        frame_table_mes2_option = tk.LabelFrame(frame_mes2,text='Option')
        frame_table_mes2_option.pack(expand=True, fill='both')
        
    #função para abrir a janela com suas respectivas caracteristicas     
    def abrir_janela_adicionar(self):
        # Cria uma nova janela "top-level" que flutua sobre a principal
        janela_adicionar = tk.Toplevel(self.frame)
        janela_adicionar.title("Adicionar Contrato")
        
        # Lista de entradas, com um campo de entrada para cada coluna da tabela
        entradas = {}
        
        # Loop para criar labels e entradas para cada coluna da tabela
        for coluna in self.columns:
            if coluna in ["Sett. Price", "Delta", "MTM (Eq USD)", 'Gamma', 'Vega','Theta', 'Rho', "Expire Date"]:
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

        frame_box = tk.Frame(janela_adicionar)
        frame_box.pack(fill='x', padx=5, pady=2)

        label_del_janela_add = tk.Label(frame_box, text="Expire Date", width=20, anchor="w")
        label_del_janela_add.pack(side="left")

        self.box_del_janela_add = ttk.Combobox(frame_box, values=entradas_del_date)
        self.box_del_janela_add.pack(side="left",fill="x", expand=True)


        # Função interna para capturar os dados e adicionar à tabela
        def adicionar_contrato():
            # Extrai os valores digitados em cada campo de entrada
            dados = {coluna: entradas[coluna].get() for coluna in self.columns if coluna not in ["Sett. Price", "Delta", "MTM (Eq USD)",'Gamma', 'Vega','Theta', 'Rho', 'Expire Date']}
            
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
                self.table_swap.updateModel(TableModel(self.table_junto[self.table_junto["Swap/Option"] == "swap"]))
                self.table_swap.redraw()
            elif dados["Swap/Option"].lower() == "option":
                self.table_option.updateModel(TableModel(self.table_junto[self.table_junto["Swap/Option"] == "option"]))
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
        for mes in range(1, 13):
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
                         
class AbaPrecosMercado:
    def __init__(self, notebook):
        # Cria o frame da aba
        self.frame = ttk.Frame(notebook)

        entradas = ["call","put"] #entradas para a call e a put
        entradas_buy_sell = ["buy","sell"] # entradas para o campo 
        
        
        # Configurações da aba Preços de Mercado
        self.label = tk.Label(self.frame, text="Calculadora de Opções")
        self.label.pack()
        
        frame_calculadora = tk.Frame(self.frame)
        frame_calculadora.pack(expand=True, fill='both')
        
        # Lista das labels para os botões
        labels = [
            "Strike", "Sett. Price", "Volatility",
            "Expire Date", "Notional"
        ]

        # Dicionário para armazenar as entradas
        self.entries = {}

        subframe = tk.Frame(frame_calculadora)
        subframe.pack(expand=True, pady=20)  # Centraliza o conteúdo do subframe dentro do frame_calculadora

        # Adiciona os campos de entrada com labels acima
        for i, label_text in enumerate(labels):
            # Cria um sub-frame para cada campo (organizado verticalmente)
            field_frame = tk.Frame(subframe)
            field_frame.grid(row=i // 3, column=i % 3, padx=20, pady=20, sticky="n")  # Divide em linhas/colunas
            
            # Cria uma label e coloca acima do campo
            label = tk.Label(field_frame, text=label_text)
            label.pack()  # Centraliza a label acima
            
            # Cria o campo de entrada e coloca abaixo
            entry = tk.Entry(field_frame, width=20)
            entry.pack()  # Centraliza o campo abaixo da label
            
            # Armazena a entrada no dicionário
            self.entries[label_text] = entry

        new_row = (len(labels) + 2) // 3

        # Adiciona o campo "Call ou Put"
        field_frame_call_put = tk.Frame(subframe)
        field_frame_call_put.grid(row=new_row-1, column=2, padx=20, pady=20, sticky="n")

        label_call_put = tk.Label(field_frame_call_put, text="Call ou Put")
        label_call_put.pack()

        self.box_call_put = ttk.Combobox(field_frame_call_put, values=entradas, width=19)
        self.box_call_put.pack()

        # Adiciona o campo "Buy ou Sell"
        field_frame_buy_sell = tk.Frame(subframe)
        field_frame_buy_sell.grid(row=new_row, column=0, padx=20, pady=20, sticky="n")

        label_buy_sell = tk.Label(field_frame_buy_sell, text="Buy ou Sell")
        label_buy_sell.pack()

        self.box_buy_sell = ttk.Combobox(field_frame_buy_sell, values=entradas_buy_sell, width=19)
        self.box_buy_sell.pack()

        # Adicona o ccampo del date como combobox
        field_frame_del_date = tk.Frame(subframe)
        field_frame_del_date.grid (row=new_row, column=1, padx=20, pady=20, sticky="n")
        
        label_del_date = tk.Label(field_frame_del_date, text="Delivery Date")
        label_del_date.pack()

        self.box_del_date = ttk.Combobox(field_frame_del_date, values=entradas_del_date, width=19)
        self.box_del_date.pack()

        style = ttk.Style()
        style.configure("TCombobox", arrowsize=25)

        def atualizar_entry(event):
            selecionado = self.box_del_date.get().split()
            entry = self.entries["Expire Date"]

            entry.delete(0, tk.END)
            entry.insert(0, selecionado[1])

        self.box_del_date.bind("<<ComboboxSelected>>", atualizar_entry)

        # Botão para armazenar os dados das entradas
        self.save_button = tk.Button(self.frame, text="Armazenar Entradas", command=self.store_entries_data)
        self.save_button.pack(side=tk.BOTTOM, pady = 20)

        # Variável para armazenar os dados das entradas
        self.stored_data = None
        
    def store_entries_data(self):
        # Coleta os dados das entradas e armazena em uma variável
        # armazena os dados em um dictionary
        self.stored_data = {label: entry.get() for label, entry in self.entries.items()}
        # print("Dados armazenados:", self.stored_data)  # Exibe os dados no console para verificação
        
        self.stored_data["Call/Put"] = self.box_call_put.get() #adiciona a coluna call ou put no dictionary e pega o resultado4
        self.stored_data["Buy/Sell"] = self.box_buy_sell.get()
        self.stored_data["Delivery Date"] = self.box_del_date.get()

        # ajusta o input com split e forma uma tupla com o valor 0 sendo o codigo e valor 1 sendo a data
        del_date_split = self.stored_data["Delivery Date"].split()
         
        # exibe o delivery date no campo de entrada do expire date
        exp_date_config = self.entries["Expire Date"]
        exp_date_config.delete(0, tk.END)
        exp_date_config.insert(0, del_date_split[1])

        #sobrescreve o expire date com o delivery date por codigo
        self.stored_data["Expire Date"] = del_date_split[1]

        time_in_float = converte_data_float(self.stored_data["Expire Date"])
        
        #converte para float todos os tipos
        stock_price = float(self.stored_data["Sett. Price"])
        strike_price = float(self.stored_data["Strike"])
        vol = float(self.stored_data["Volatility"])
        
        #de fato calcula e exibe o B&S
        premium = calcula_b_s(stock_price=stock_price, strike_price=strike_price, rate=0, time=time_in_float, vol=vol, dividend=0)
        delta = delta_calc(premium[2])
        gamma = gamma_calc(d1=premium[2], stock_price=stock_price, vol=vol, time=time_in_float)
        vega = vega_calc(d1=premium[2], stock_price=stock_price, time=time_in_float)
        theta = theta_calc(d1 = premium[2], d2 = premium[3], stock_price=stock_price, strike_price=strike_price, time=time_in_float, rate=0, vol=vol) 
        rho = roh_calc(d2=premium[3], strike_price=strike_price, time=time_in_float, rate=0)

        #verifica se o frame ja tem uma string
        if not hasattr(self, 'result_label'):
            self.result_label = tk.Label(self.frame, text="", font=("Helvetica", 16, "bold italic"))
            self.result_label.pack(pady=10)

        # Atualiza o texto da label existente e diferencia call e put buy ou sell
        if self.stored_data["Call/Put"] == "call":
            if self.stored_data["Buy/Sell"] == "buy":
                self.result_label.config(text=f"Premium: {premium[0]:.4f}\n" +
                                        f"Delta: {delta[0]:.4f}\n" +
                                        f"Gamma: {gamma:.4f}\n" +
                                        f"Vega: {vega:.4f}\n" +
                                        f"Theta: {theta[0]:.4f}\n" +
                                        f"Rho: {rho[0]:.4f}")
            else:
                self.result_label.config(text=f"Premium: {premium[0]:.4f}\n" +
                                        f"Delta: {-delta[0]:.4f}\n" +
                                        f"Gamma: {-gamma:.4f}\n" +
                                        f"Vega: {vega:.4f}\n" +
                                        f"Theta: {-theta[0]:.4f}\n" +
                                        f"Rho: {rho[0]:.4f}")
        else:
            if self.stored_data["Buy/Sell"] == "buy":
                self.result_label.config(text=f"Premium: {premium[1]:.4f}\n" +
                                        f"Delta: {delta[1]:.4f}\n" +
                                        f"Gamma: {gamma:.4f}\n" +
                                        f"Vega: {vega:.4f}\n" +
                                        f"Theta: {theta[1]:.4f}\n" +
                                        f"Rho: {rho[1]:.4f}")       
            else:
                self.result_label.config(text=f"Premium: {premium[1]:.4f}\n" +
                                        f"Delta: {-delta[1]:.4f}\n" +
                                        f"Gamma: {-gamma:.4f}\n" +
                                        f"Vega: {-vega:.4f}\n" +
                                        f"Theta: {-theta[1]:.4f}\n" +
                                        f"Rho: {rho[1]:.4f}") 

    #product type é call put ou swap
        # S: Preço atual do ativo (ação/subjacente) stock_price
        # 𝐾
        # K: Preço de exercício (strike price) strike_price
        # 𝑇
        # T: Tempo até o vencimento, geralmente em anos (em fração de ano: dias/365) Tempo
        # 𝜎
        # σ: Volatilidade implícita anual do ativo vol
        # 𝑟
        # r: Taxa de juros livre de risco rate
    
# funcoes globais das gregas

def calcula_b_s(stock_price, strike_price, time, vol, dividend = 0.0, rate=0.0):

        d1 = (log(stock_price/strike_price)+(rate-dividend+vol**2/2)*time)/(vol*time**.5)
        d2 = d1 - vol*time**.5
        
        call = stats.norm.cdf(d1) * stock_price*e**(-dividend*time)-stats.norm.cdf(d2)*strike_price*e**(-rate*time)
        put = stats.norm.cdf(-d2)*strike_price*e**(-rate*time)-stats.norm.cdf(-d1)*stock_price*e**(-dividend*time)
        
        return [call, put, d1, d2]
    
def delta_calc(d1): # calcula delta para call e para put
        "Calcula delta"
        
        delta_call = stats.norm.cdf(d1,0,1)
        
        delta_put = -stats.norm.cdf(-d1,0,1)
         
        return [delta_call, delta_put]
    
def gamma_calc(d1, stock_price, vol, time): # calcula gamma 
        "Calcula gamma"
        
        gamma = stats.norm.pdf(d1,0,1)/(stock_price*vol*np.sqrt(time))
        
        return gamma
        
def vega_calc( d1, stock_price, time):
        "calcula vega"
        
        vega = stock_price*stats.norm.pdf(d1,0,1)*np.sqrt(time)
        
        return vega*0.01
        
def theta_calc( d1, d2, stock_price, strike_price, time, rate, vol):
        "calcula theta"
        
        theta_call = -stock_price*stats.norm.pdf(d1,0,1)*vol/(2*np.sqrt(time)) - rate*stock_price*np.exp(-rate*time)*stats.norm.cdf(d2,0,1)
        
        theta_put = -stock_price*stats.norm.pdf(d1,0,1)*vol/(2*np.sqrt(time)) + rate*stock_price*np.exp(-rate*time)*stats.norm.cdf(-d2,0,1)
        
        return [theta_call/365 , theta_put/365 ]
    
def roh_calc( d2, strike_price, time, rate):
        "calcula roh"
        
        rho_call = strike_price*time*np.exp(-rate*time)*stats.norm.cdf(d2,0,1)
        
        rho_put = -strike_price*time*np.exp(-rate*time)*stats.norm.cdf(-d2,0,1)
        
        return [rho_call*0.01, rho_put*0.01]

class AbaCalculoPL:
    def __init__(self, notebook):
        # Cria o frame da aba
        self.frame = ttk.Frame(notebook)
        # Configurações da aba Cálculo de P&L
        self.label = tk.Label(self.frame, text="Aba Cálculo de P&L")
        self.label.pack()
        # Adicione aqui os widgets e funcionalidades específicas desta aba

# Inicialização do sistema
if __name__ == "__main__":
    root = tk.Tk()
    
    # cria uma instancia do sistema
    sistema = SistemaGUI(root)
    root.mainloop()
