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
        self.entry_soma_mtm = tk.Entry(self.frame_soma_mtm, width=25)
        self.entry_soma_mtm.pack(pady=20)
        self.entry_soma_mtm.config(state="readonly")

        self.entry_soma_mtm_swap = tk.Entry(self.frame_soma_mtm, width=25)
        self.entry_soma_mtm_swap.pack(pady=20)
        self.entry_soma_mtm_swap.insert(0, "MTM Sum Swap: ")
        self.entry_soma_mtm_swap.config(state="readonly")

        self.entry_soma_mtm_option = tk.Entry(self.frame_soma_mtm, width=25)
        self.entry_soma_mtm_option.pack(pady=20)
        self.entry_soma_mtm_option.insert(0, "MTM Sum Option: ")
        self.entry_soma_mtm_option.config(state="readonly")
        



        self.botao_atualizar_soma = tk.Button(self.frame_soma_mtm,text="Atualizar Soma MTM", command=self.atualiza_mtm)
        self.botao_atualizar_soma.pack(side="bottom", padx=20, pady=30)

        # Chama funcao para atualizar a entry
        self.atualiza_mtm()

    # Atualiza o valor da soma mtm
    def atualiza_mtm(self):
        df_completo = le_arquivos()

        soma = df_completo["MTM (Eq USD)"].sum()

        # Filtrar e somar os valores para Swaps
        soma_mtm_swap = df_completo[df_completo["Swap/Option"].str.lower() == "swap"]["MTM (Eq USD)"].sum()

        # Filtrar e somar os valores para Opções
        soma_mtm_option = df_completo[df_completo["Swap/Option"].str.lower() == "option"]["MTM (Eq USD)"].sum()

        print(soma_mtm_option)
        print(soma_mtm_swap)


        self.entry_soma_mtm.config(state="normal")                      # Habilita edição temporariamente
        self.entry_soma_mtm.delete(0, tk.END)                           # Remove o conteúdo existente
        self.entry_soma_mtm.insert(0, "MTM Sum: $"+str(soma))            # Insere o novo texto
        self.entry_soma_mtm.config(state="readonly")                    # Volta o estado para readonly

        self.entry_soma_mtm_swap.config(state="normal")                      # Habilita edição temporariamente
        self.entry_soma_mtm_swap.delete(0, tk.END)                           # Remove o conteúdo existente
        self.entry_soma_mtm_swap.insert(0, "MTM Sum Swap: $"+str(soma_mtm_swap))            # Insere o novo texto
        self.entry_soma_mtm_swap.config(state="readonly")                    # Volta o estado para readonly

        self.entry_soma_mtm_option.config(state="normal")                      # Habilita edição temporariamente
        self.entry_soma_mtm_option.delete(0, tk.END)                           # Remove o conteúdo existente
        self.entry_soma_mtm_option.insert(0, "MTM Sum Option: $"+str(soma_mtm_option))            # Insere o novo texto
        self.entry_soma_mtm_option.config(state="readonly")                    # Volta o estado para readonly

        # Adicione aqui os widgets e funcionalidades específicas desta aba