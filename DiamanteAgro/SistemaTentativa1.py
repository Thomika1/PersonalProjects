import pandas as pd
import tkinter as tk
from tkinter import ttk
from pandastable import Table, TableModel
import os

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
        self.aba1.salvar_tabelas()
        self.root.destroy()

class AbaBuySell:
    columns = ['Trade No.', 'Swap/Option','Underlying', 'Trade Date', 'Buy/Sell', 'Product Type', 'Ccy', 
               'Delivery Month', 'Expire Date', 'Strike', 'Notional', 'Long', 'Short', 'Sett. Price', 
               'Delta', 'Premium (Eq USD)', 'MTM (Eq USD)']

    def __init__(self, notebook):
        # Cria o frame da aba
        self.frame = ttk.Frame(notebook)

        # Inicializa a tabela principal como DataFrame
        self.table = pd.DataFrame(columns=self.columns)
        
        # Adiciona uma label como exemplo
        self.label = tk.Label(self.frame, text="Aba swap/options")
        self.label.pack()

        # Botão para abrir a janela de adição de contrato
        self.botao_adicionar_contrato = tk.Button(self.frame, text="Adicionar Contrato", 
                                                  command=self.abrir_janela_adicionar)
        self.botao_adicionar_contrato.pack(pady=10)
        
        #botão para abrir a janela de exibição das tabelas por mes
        self.botao_exibir_tabelas_mes = tk.Button(self.frame, text='Abrir exibição por mẽs',
                                                  command=self.abrir_janela_exibicao_mes)
        self.botao_exibir_tabelas_mes.pack(pady=15)
        
        
        # Frame para a tabela de swap
        frame_table_swap = tk.Frame(self.frame)
        frame_table_swap.pack(expand=True, fill='both')
        
        # Criação da tabela de swap com filtro
        self.table_swap = Table(frame_table_swap, dataframe=self.table[self.table["Swap/Option"] == "swap"],
                                showtoolbar=True, showstatusbar=True)
        
        
        # Frame para a tabela de options
        frame_table_option = tk.Frame(self.frame)
        frame_table_option.pack(expand=True, fill='both')
        
        # Criação da tabela de options com filtro
        self.table_option = Table(frame_table_option, dataframe=self.table[self.table["Swap/Option"] == "option"],
                                  showtoolbar=True, showstatusbar=True)

        # Carrega e exibe as tabelas
        self.carregar_tabelas()
        self.table_swap.show()
        self.table_option.show()
        
    
    def abrir_janela_exibicao_mes(self):
        # Lista de valores para os meses
        mes_list = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
        
        # Caminho dos arquivos
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        
        # Cria a janela para exibir as tabelas
        janela_exibicao_mes = tk.Toplevel(self.frame)
        janela_exibicao_mes.title("Tabelas por mês")
        janela_exibicao_mes.geometry("1920x1080")

        # Cria um canvas com scrollbar
        canvas = tk.Canvas(janela_exibicao_mes)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(janela_exibicao_mes, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame para conteúdo dentro do canvas
        frame_conteudo = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_conteudo, anchor="nw")

        # Atualiza a área de rolagem do canvas
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame_conteudo.bind("<Configure>", on_frame_configure)

        # Frames para cada mês
        frame_mes1 = tk.LabelFrame(frame_conteudo, text="Mês 1", padx=5, pady=5)
        frame_mes1.pack(expand=True, fill="both", pady=10)
        
        frame_mes2 = tk.LabelFrame(frame_conteudo, text="Mês 2", padx=5, pady=5)
        frame_mes2.pack(expand=True, fill="both", pady=10)

        # Frame para o botão e as comboboxes
        frame_botao = tk.Frame(frame_conteudo)
        frame_botao.pack(expand=True, fill='both', pady=10)

        # Comboboxes para seleção de mês
        box_mes1 = ttk.Combobox(frame_botao, values=mes_list)
        box_mes1.pack(pady=5)
        
        box_mes2 = ttk.Combobox(frame_botao, values=mes_list)
        box_mes2.pack(pady=5)

        # Função para exibir as tabelas
        def exibe_tabelas():
            # Mapeamento dos meses por nome para número
            meses = {
                "Janeiro": "1", "Fevereiro": "2", "Março": "3", "Abril": "4", 
                "Maio": "5", "Junho": "6", "Julho": "7", "Agosto": "8", 
                "Setembro": "9", "Outubro": "10", "Novembro": "11", "Dezembro": "12"
            }
            
            # Obter os meses selecionados
            mes1 = box_mes1.get()
            mes2 = box_mes2.get()
            
            # Converter o nome do mês para o número correspondente
            mes1_num = meses[mes1]
            mes2_num = meses[mes2]
            
            # Caminhos dos arquivos CSV
            caminho_arquivo_mes1 = os.path.join(diretorio_atual, f"table_{mes1_num}.csv")
            caminho_arquivo_mes2 = os.path.join(diretorio_atual, f"table_{mes2_num}.csv")
            
            # Carregar os arquivos CSV correspondentes
            df_mes1 = pd.read_csv(caminho_arquivo_mes1)
            df_mes2 = pd.read_csv(caminho_arquivo_mes2)
            
            # Filtrar e exibir as tabelas para cada tipo (Swap e Option) separadamente
            df_mes1_swap = df_mes1[df_mes1["Swap/Option"] == "swap"]
            df_mes1_option = df_mes1[df_mes1["Swap/Option"] == "option"]
            
            df_mes2_swap = df_mes2[df_mes2["Swap/Option"] == "swap"]
            df_mes2_option = df_mes2[df_mes2["Swap/Option"] == "option"]
            
            # Exibir as tabelas em frames diferentes
            table_mes1_swap = Table(frame_table_mes1_swap, dataframe=df_mes1_swap, showtoolbar=True, showstatusbar=True)
            table_mes1_option = Table(frame_table_mes1_option, dataframe=df_mes1_option, showtoolbar=True, showstatusbar=True)
            table_mes2_swap = Table(frame_table_mes2_swap, dataframe=df_mes2_swap, showtoolbar=True, showstatusbar=True)
            table_mes2_option = Table(frame_table_mes2_option, dataframe=df_mes2_option, showtoolbar=True, showstatusbar=True)
            
            # Atualizar as tabelas na interface
            table_mes1_swap.show()
            table_mes1_option.show()
            table_mes2_swap.show()
            table_mes2_option.show()
        
        # Botão para exibir as tabelas filtradas
        botao_exibe_tabelas_mes = tk.Button(frame_botao, text='Exibir Tabelas', command=exibe_tabelas)
        botao_exibe_tabelas_mes.pack(pady=5)

        # Frames para inserir as tabelas
        frame_table_mes1_swap = tk.Frame(frame_mes1)
        frame_table_mes1_swap.pack(expand=True, fill='both', padx=5, pady=5)
        
        frame_table_mes1_option = tk.Frame(frame_mes1)
        frame_table_mes1_option.pack(expand=True, fill='both', padx=5, pady=5)
        
        frame_table_mes2_swap = tk.Frame(frame_mes2)
        frame_table_mes2_swap.pack(expand=True, fill='both', padx=5, pady=5)
        
        frame_table_mes2_option = tk.Frame(frame_mes2)
        frame_table_mes2_option.pack(expand=True, fill='both', padx=5, pady=5)
        
        
    #função para abrir a janela com suas respectivas caracteristicas     
    def abrir_janela_adicionar(self):
        # Cria uma nova janela "top-level" que flutua sobre a principal
        janela_adicionar = tk.Toplevel(self.frame)
        janela_adicionar.title("Adicionar Contrato")
        
        # Lista de entradas, com um campo de entrada para cada coluna da tabela
        entradas = {}
        
        # Loop para criar labels e entradas para cada coluna da tabela
        for coluna in self.columns:
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

        # Função interna para capturar os dados e adicionar à tabela
        def adicionar_contrato():
            # Extrai os valores digitados em cada campo de entrada
            dados = {coluna: entradas[coluna].get() for coluna in self.columns}

            # Converte os dados em DataFrame e concatena com self.table
            nova_linha = pd.DataFrame([dados])
            self.table = pd.concat([self.table, nova_linha], ignore_index=True)

            # Atualiza as visualizações específicas para swap e option
            if dados["Swap/Option"].lower() == "swap":
                self.table_swap.updateModel(TableModel(self.table[self.table["Swap/Option"] == "swap"]))
                self.table_swap.redraw()
            elif dados["Swap/Option"].lower() == "option":
                self.table_option.updateModel(TableModel(self.table[self.table["Swap/Option"] == "option"]))
                self.table_option.redraw()

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
            
            # Salva o DataFrame correspondente ao mês em um arquivo CSV
            dados_mes.to_csv(caminho_arquivo, index=False)
            print(f"Tabela para o mês {mes} salva como {nome_arquivo}.")

    #função para carregar o conteudo das tabelas
    def carregar_tabelas(self):
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        self.table = pd.DataFrame(columns=self.columns)

        # Carrega os arquivos CSV por mês (1 a 12)
        for mes in range(1, 13):
            caminho_arquivo = os.path.join(diretorio_atual, f"table_{mes}.csv")
            
            if os.path.exists(caminho_arquivo):
                #print(f"Carregando dados de: {caminho_arquivo}")
                dados_mes = pd.read_csv(caminho_arquivo)
                self.table = pd.concat([self.table, dados_mes], ignore_index=True)
            else:
                print(f"Arquivo não encontrado para o mês {mes}.")

        if not self.table.empty:
            # Debug: Exibir os dados carregados
            #print("Dados carregados para 'self.table':")
            #print(self.table.head())

            # Atualiza o modelo para a tabela de swap
            self.table_swap.updateModel(TableModel(self.table[self.table["Swap/Option"].str.lower() == "swap"]))
            self.table_swap.redraw()

            # Atualiza o modelo para a tabela de option
            self.table_option.updateModel(TableModel(self.table[self.table["Swap/Option"].str.lower() == "option"]))
            self.table_option.redraw()
        else:
            print("Nenhum dado foi carregado; os arquivos CSV mensais podem não existir.")
            
            
class AbaPrecosMercado:
    def __init__(self, notebook):
        # Cria o frame da aba
        self.frame = ttk.Frame(notebook)
        # Configurações da aba Preços de Mercado
        self.label = tk.Label(self.frame, text="Aba Preços de Mercado")
        self.label.pack()
        # Adicione aqui os widgets e funcionalidades específicas desta aba

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
    sistema = SistemaGUI(root)
    root.mainloop()
