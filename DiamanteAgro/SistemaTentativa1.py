import pandas as pd
import tkinter as tk
from tkinter import ttk
from pandastable import Table
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
    columns = ['Trade No.', 'Underlying', 'Trade Date', 'Buy/Sell', 'Product Type', 'Ccy', 
               'Delivery Month', 'Expire Date', 'Strike', 'Notional', 'Short', 'Sett. Price', 
               'Delta', 'Premium (Eq USD)', 'MTM (Eq USD)']

    def __init__(self, notebook):
        # Cria o frame da aba
        self.frame = ttk.Frame(notebook)

        # Inicializa as tabelas de buy e sell como atributos de instância
        self.buy_table = pd.DataFrame(columns=self.columns)
        self.sell_table = pd.DataFrame(columns=self.columns)

        # Adiciona uma label como exemplo
        self.label = tk.Label(self.frame, text="Aba Buy/Sell")
        self.label.pack()

        # Botão para abrir a janela de adição de contrato buy
        self.botao_adicionar_contrato_buy = tk.Button(self.frame, text="Adicionar Contrato buy", 
                                                       command=lambda: self.abrir_janela_adicionar("buy"))
        self.botao_adicionar_contrato_buy.pack(pady=10)

        # Botão para abrir a janela de adição de contrato sell
        self.botao_adicionar_contrato_sell = tk.Button(self.frame, text="Adicionar Contrato sell", 
                                                        command=lambda: self.abrir_janela_adicionar("sell"))
        self.botao_adicionar_contrato_sell.pack(pady=5)
        
        # Criação da tabela de buy
        self.table_buy = Table(self.frame, dataframe=self.buy_table, showtoolbar=True, showstatusbar=True)
        self.table_buy.pack(expand=True, fill='both')
        
        # Criação da tabela de sell
        self.table_sell = Table(self.frame, dataframe=self.sell_table, showtoolbar=True, showstatusbar=True)
        self.table_sell.pack(expand=True, fill='both')
    
        self.carregar_tabelas()        
         

    def abrir_janela_adicionar(self, tipo):
        # Cria uma nova janela "top-level" que flutua sobre a principal
        janela_adicionar = tk.Toplevel(self.frame)
        janela_adicionar.title("Adicionar Contrato")
        
        # Lista de entradas, com um campo de entrada para cada coluna da tabela
        entradas = {}
        
        # Loop para criar labels e entradas para cada coluna da tabela
        for i, coluna in enumerate(self.columns):
            label = tk.Label(janela_adicionar, text=coluna)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            
            entrada = tk.Entry(janela_adicionar)
            entrada.grid(row=i, column=1, padx=5, pady=5)
            
            # Armazena a entrada em um dicionário com o nome da coluna como chave
            entradas[coluna] = entrada

        # Função interna para capturar os dados e adicionar à tabela
        def adicionar_contrato():
            # Extrai os valores digitados em cada campo de entrada
            dados = {coluna: entradas[coluna].get() for coluna in self.columns}
            print("Acessando table_buy e table_sell...")
            print(f"table_buy: {hasattr(self, 'table_buy')}")
            print(f"table_sell: {hasattr(self, 'table_sell')}")

            # Adiciona uma nova linha na tabela de acordo com o tipo Buy/Sell
            if tipo == "buy":
                self.buy_table = pd.concat([self.buy_table, pd.DataFrame([dados])], ignore_index=True)
                self.table_buy.updateModel()  # Atualiza o modelo da tabela de buy
                self.table_buy.redraw()  # Redesenha a tabela de buy
            elif tipo == "sell":
                self.sell_table = pd.concat([self.sell_table, pd.DataFrame([dados])], ignore_index=True)
                self.table_sell.updateModel()  # Atualiza o modelo da tabela de sell
                self.table_sell.redraw()  # Redesenha a tabela de sell

            # Fecha a janela após adicionar o contrato
            janela_adicionar.destroy()
        
        # Botão para adicionar contrato e fechar a janela
        botao_adicionar = tk.Button(janela_adicionar, text="Adicionar", command=adicionar_contrato)
        botao_adicionar.grid(row=len(self.columns), column=0, columnspan=2, pady=10)

    def salvar_tabelas(self):
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        # Salva as tabelas em arquivos CSV no diretório atual
        self.buy_table.to_csv(os.path.join(diretorio_atual, "buy_table.csv"), index=False)
        self.sell_table.to_csv(os.path.join(diretorio_atual, "sell_table.csv"), index=False)

    def carregar_tabelas(self):
        # Carrega as tabelas do CSV se existirem
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        
        if os.path.exists(os.path.join(diretorio_atual, "buy_table.csv")):
            self.buy_table = pd.read_csv(os.path.join(diretorio_atual, "buy_table.csv"))
            self.table_buy.updateModel()  # Atualiza a tabela de buy com dados carregados
            self.table_buy.redraw()
        if os.path.exists(os.path.join(diretorio_atual, "sell_table.csv")):
            self.sell_table = pd.read_csv(os.path.join(diretorio_atual, "sell_table.csv"))
            self.table_sell.updateModel()  # Atualiza a tabela de sell com dados carregados
            self.table_sell.redraw()

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
