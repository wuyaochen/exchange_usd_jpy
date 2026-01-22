import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import pandas as pd

from exchange import build_csv
from graph import plot_graph_usd, plot_graph_jpy, plot_graph_gbp

def append_log(log_text, text):
    log_text.configure(state="normal")
    log_text.insert("end", text + "\n")
    log_text.see("end")
    log_text.configure(state="disabled")


def run_task(should_update, currency, log_text):
    if should_update:
        append_log(log_text, "開始更新匯率資料")
        build_csv(min_period="2000M1", create_csv=True)
    else:
        append_log(log_text, "使用現有 CSV 檔案")

    csv_file = "usd_jpy_history.csv"
    if not os.path.exists(csv_file):
        raise FileNotFoundError("找不到匯率 CSV 檔案！")

    df_csv = pd.read_csv(csv_file, encoding="UTF-8")
    df_csv["Period"] = (
        df_csv["Period"].astype(str)
        .str.strip()
        .str.replace("M", "-", regex=False)
        .str.replace("\uFEFF", "")
    )
    df_csv["Period"] = pd.to_datetime(df_csv["Period"], format="%Y-%m", errors="coerce")

    currency = currency.strip().upper()
    if currency == "USD":
        plot_graph_usd(df_csv, show=True)
    elif currency == "JPY":
        plot_graph_jpy(df_csv, show=True)
    elif currency == "GBP":
        plot_graph_gbp(df_csv, show=True)
    elif currency == "ALL":
        plot_graph_usd(df_csv, show=False)
        plot_graph_jpy(df_csv, show=False)
        plot_graph_gbp(df_csv, show=True)
    else:
        raise ValueError("幣別必須是 USD / JPY / GBP / ALL")

    append_log(log_text, "任務完成")


def main():
    root_window = tk.Tk()
    root_window.title("匯率小工具")
    root_window.geometry("800x600")
    root_window.option_add("*Font", ("Microsoft JhengHei", 12))

    root_window.configure(bg="#f5f8ff")

    content = ttk.Frame(root_window, padding=30)
    content.place(relx=0.5, rely=0.5, anchor="center")

    title_label = ttk.Label(
        content,
        text="匯率小工具",
        font=("Microsoft JhengHei", 26, "bold"),
        anchor="center"
    )
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 25))

    update_csv_var = tk.BooleanVar(value=False)
    update_check = ttk.Checkbutton(content, text="更新並寫出 CSV", variable=update_csv_var)
    update_check.grid(row=1, column=0, columnspan=2, pady=10, sticky="n")

    currency_label = ttk.Label(content, text="選擇幣別：", font=("Microsoft JhengHei", 13))
    currency_label.grid(row=2, column=0, pady=(10, 5), sticky="e")

    currency_var = tk.StringVar(value="USD")
    currency_box = ttk.Combobox(
        content,
        textvariable=currency_var,
        state="readonly",
        values=("USD", "JPY", "GBP", "ALL"),
        width=10,
        font=("Microsoft JhengHei", 13),
        justify="center"
    )
    currency_box.grid(row=2, column=1, pady=(10, 5), sticky="w")

    run_button = ttk.Button(
        content,
        text="執行",
        width=18,
        style="Accent.TButton"
    )
    run_button.grid(row=3, column=0, columnspan=2, pady=25)

    log_text = ScrolledText(
        content,
        width=70,
        height=10,
        wrap="word",
        state="disabled",
        font=("Consolas", 11)
    )
    log_text.grid(row=4, column=0, columnspan=2, pady=(10, 0))

    def on_run():
        run_button.configure(state="disabled", text="處理中")
        root_window.update_idletasks()
        try:
            run_task(
                should_update=bool(update_csv_var.get()),
                currency=currency_var.get(),
                log_text=log_text
            )
        except Exception as e:
            messagebox.showerror("錯誤", str(e))
            append_log(log_text, f"錯誤：{e}")
        finally:
            run_button.configure(state="normal", text="執行")

    run_button.configure(command=on_run)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=("Microsoft JhengHei", 13))
    style.configure("Accent.TButton", font=("Microsoft JhengHei", 13, "bold"), padding=8)

    root_window.mainloop()


if __name__ == "__main__":
    main()
