from gregas import *
import tkinter as tk
from tkinter import ttk
from functions import *

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
        rho = rho_calc(d2=premium[3], strike_price=strike_price, time=time_in_float, rate=0)

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