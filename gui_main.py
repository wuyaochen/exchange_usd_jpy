import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import os

import pandas as pd

from exchange import build_csv
from graph import plot_graph_usd, plot_graph_jpy

def run_task(create_csv, money, log_widget):
    if create_csv:
        append_log(log_widget, "開始更新匯率")
        build_csv(min_period="2000M1", create_csv=True)
    else:
        append_log(log_widget, "不更新CSV，使用現有檔案")

    csv_path = "usd_jpy_history.csv"
    if not os.path.exists(csv_path):
        raise FileNotFoundError("csv不存在")
    
    df_csv = pd.read_csv(csv_path, encoding="UTF-8")

    if "Period" in df_csv.columns:
        df_csv["Period"] = pd.to_datetime(df_csv["Period"].astype(str).str.replace("M", "-"), format="%Y-%m")

        money = money.strip().upper()
        if money == "USD":
            selected = df_csv[["Period", "NTD/USD"]]
            append_log(log_widget, "最近幾筆(USD): \n" + selected.tail().to_string(index=False))
            plot_graph_usd(df_csv, show = True)
        
        elif money == "JPY":
            selected = df_csv[["Period", "NTD/JPY"]]
            append_log(log_widget, "最近幾筆(JPY): \n" + selected.tail().to_string(index=False))
            plot_graph_jpy(df_csv, show = True)
        
        elif money == "ALL":
            append_log(log_widget, "最近幾筆(ALL): \n" + df_csv.tail().to_string(index=False))
            plot_graph_usd(df_csv, show = False)
            plot_graph_jpy(df_csv, show = True)
        else:
            raise ValueError("幣別必須是 USD / JPY / ALL")
        append_log(log_widget, "完成")

def append_log(log_widget, text):
    log_widget.configure(state="normal")
    log_widget.insert("end", text + "\n")
    log_widget.see("end")
    log_widget.configure(state="disabled")

def main():
    root = tk.Tk()
    root.title("外匯GUI (USD/JPY)")

    frm = ttk.Frame(root, padding=20)
    frm.grid(row=0, column=0, sticky="nsew")

    var_create_csv = tk.BooleanVar(value=False)
    var_money = tk.StringVar(value="USD")

    ttk.Checkbutton(frm, text="更新並寫出CSV", variable=var_create_csv).grid(row=0, column=0, sticky='w')
    ttk.Label(frm, text="幣別:").grid(row=0, column=1, sticky="e", padx=(12, 4))
    cb = ttk.Combobox(frm, textvariable=var_money, state="readonly", values=("USD", "JPY", "ALL"), width=6)
    cb.grid(row=0, column=2, sticky="w")

    btn_run = ttk.Button(frm, text="執行")
    btn_run.grid(row=0, column=3, sticky="e", padx=(12, 0))

    log_box = ScrolledText(root, height=12, wrap="word", state="disabled")
    log_box.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0,8))

    root.grid_rowconfigure(0, weight=0)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    def on_run():
        btn_run.configure(state="disabled")
        
        try:
            run_task(create_csv=bool(var_create_csv.get()), money=var_money.get(), log_widget=log_box)
        
        finally:
            btn_run.configure(state="normal")
    btn_run.configure(command=on_run)
    root.minsize(700, 500)
    root.mainloop()

if __name__ == "__main__":
    main()