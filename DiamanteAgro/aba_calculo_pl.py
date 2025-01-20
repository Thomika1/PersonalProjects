import tkinter as tk
from tkinter import ttk
from functions import *


class AbaCalculoPL:
    def __init__(self, notebook):
        # Cria o frame da aba
        self.frame = ttk.Frame(notebook)
        # Configurações da aba Cálculo de P&L
        self.label = tk.Label(self.frame, text="Aba Cálculo de P&L")
        self.label.pack()

        # Cria frame papa soa mtm
        self.frame_soma_mtm = tk.Frame(self.frame)
        self.frame_soma_mtm.pack(expand=True)

        # Cria Entry em read mode para exibir a soma do mtm
        self.entry_soma_mtm = tk.Entry(self.frame_soma_mtm)
        self.entry_soma_mtm.pack()
        self.entry_soma_mtm.config(state="readonly")

        self.botao_atualizar_soma = tk.Button(self.frame_soma_mtm,text="Atualizar Soma MTM", command=self.atualiza_mtm)
        self.botao_atualizar_soma.pack(side="bottom", padx=20, pady=30)

        # Chama funcao para atualizar a entry
        self.atualiza_mtm()

    def atualiza_mtm(self):
        df_completo = le_arquivos()

        soma = df_completo["MTM (Eq USD)"].sum()


        self.entry_soma_mtm.config(state="normal")      # Habilita edição temporariamente
        self.entry_soma_mtm.delete(0, tk.END)           # Remove o conteúdo existente
        self.entry_soma_mtm.insert(0, "MTM Sum: "+str(soma))             # Insere o novo texto
        self.entry_soma_mtm.config(state="readonly")    # Volta o estado para readonly

        # Adicione aqui os widgets e funcionalidades específicas desta aba