import pandas as pd
import tkinter as tk
from tkinter import ttk
import warnings
from aba_extrato import AbaBuySell
from aba_precos_mercado import AbaPrecosMercado
from aba_calculo_pl import AbaCalculoPL

pd.set_option('future.no_silent_downcasting', True)
warnings.filterwarnings("ignore", category=FutureWarning)
pd.set_option('display.float_format', '{:.2f}'.format)
pd.set_option("display.max_rows", None)

# inicializa as abas
class SistemaGUI:
    def __init__(self, root):
        # Configurações gerais da interface principal
        self.root = root
        self.root.title("Sistema de Gestão de Contratos")
        
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
        self.notebook.add(self.aba1.frame, text="Extrato")
        self.notebook.add(self.aba2.frame, text="Calculadora de opções")
        self.notebook.add(self.aba3.frame, text="Cálculo de P&L")
        
        # Configura o evento de fechamento da janela
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_programa)

    def fechar_programa(self):
        # Salva as tabelas antes de fechar
        #self.aba1.salvar_tabelas()
        self.root.destroy()

# Inicialização do sistema
if __name__ == "__main__":
    root = tk.Tk()
    
    # cria uma instancia do sistema
    sistema = SistemaGUI(root)
    root.mainloop()