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


    def salvar_tabelas(self):
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        # Salva as tabelas em arquivos CSV no diretório atual
        self.table.to_csv(os.path.join(diretorio_atual, "table.csv"), index=False)
        

    def carregar_tabelas(self):
        # Carrega as tabelas do CSV se existirem
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_arquivo = os.path.join(diretorio_atual, "table.csv")
        
        if os.path.exists(caminho_arquivo):
            # Carrega os dados do CSV para o DataFrame principal
            self.table = pd.read_csv(caminho_arquivo)
            
            # Atualiza os modelos das tabelas swap e option com os novos dados
            self.table_swap.updateModel(TableModel(self.table[self.table["Swap/Option"] == "swap"]))
            self.table_option.updateModel(TableModel(self.table[self.table["Swap/Option"] == "option"]))
            
            # Redesenha as tabelas para refletir os dados carregados
            self.table_swap.redraw()
            self.table_option.redraw()

            
            

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
