import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import pandas as pd

from exchange import build_csv
from graph import plot_graph_usd, plot_graph_jpy, plot_graph_gbp


# =============================
# 📘 輔助函式
# =============================

def append_log(log_widget, text):
    log_widget.configure(state="normal")
    log_widget.insert("end", text + "\n")
    log_widget.see("end")
    log_widget.configure(state="disabled")


# =============================
# 📊 主邏輯
# =============================

def run_task(create_csv, money, log_widget):
    if create_csv:
        append_log(log_widget, "🟢 開始更新匯率資料 ...")
        build_csv(min_period="2000M1", create_csv=True)
    else:
        append_log(log_widget, "⚪ 使用現有 CSV 檔案，不重新下載。")

    csv_path = "usd_jpy_history.csv"
    if not os.path.exists(csv_path):
        raise FileNotFoundError("❌ 找不到匯率 CSV 檔案！")

    df_csv = pd.read_csv(csv_path, encoding="UTF-8")
    df_csv["Period"] = (
        df_csv["Period"].astype(str)
        .str.strip()
        .str.replace("M", "-", regex=False)
        .str.replace("\uFEFF", "")
    )
    df_csv["Period"] = pd.to_datetime(df_csv["Period"], format="%Y-%m", errors="coerce")

    money = money.strip().upper()
    if money == "USD":
        plot_graph_usd(df_csv, show=True)
    elif money == "JPY":
        plot_graph_jpy(df_csv, show=True)
    elif money == "GBP":
        plot_graph_gbp(df_csv, show=True)
    elif money == "ALL":
        plot_graph_usd(df_csv, show=False)
        plot_graph_jpy(df_csv, show=False)
        plot_graph_gbp(df_csv, show=True)
    else:
        raise ValueError("幣別必須是 USD / JPY / GBP / ALL")

    append_log(log_widget, "✅ 任務完成。")


# =============================
# 🖥️ GUI 主程式
# =============================

def main():
    root = tk.Tk()
    root.title("匯率小工具")
    root.geometry("800x600")
    root.option_add("*Font", ("Microsoft JhengHei", 12))

    # ==== 整個主畫面背景 ====
    root.configure(bg="#f5f8ff")

    # ==== 置中主框架 ====
    main_frame = ttk.Frame(root, padding=30)
    main_frame.place(relx=0.5, rely=0.5, anchor="center")  # ⬅️ 關鍵：完全置中

    # ==== 標題 ====
    lbl_title = ttk.Label(
        main_frame,
        text="匯率小工具",
        font=("Microsoft JhengHei", 26, "bold"),
        anchor="center"
    )
    lbl_title.grid(row=0, column=0, columnspan=2, pady=(0, 25))

    # ==== 勾選更新 ====
    var_create_csv = tk.BooleanVar(value=False)
    chk = ttk.Checkbutton(main_frame, text="更新並寫出 CSV", variable=var_create_csv)
    chk.grid(row=1, column=0, columnspan=2, pady=10, sticky="n")

    # ==== 選擇幣別 ====
    lbl_money = ttk.Label(main_frame, text="選擇幣別：", font=("Microsoft JhengHei", 13))
    lbl_money.grid(row=2, column=0, pady=(10, 5), sticky="e")

    var_money = tk.StringVar(value="USD")
    cb = ttk.Combobox(
        main_frame,
        textvariable=var_money,
        state="readonly",
        values=("USD", "JPY", "GBP", "ALL"),
        width=10,
        font=("Microsoft JhengHei", 13),
        justify="center"
    )
    cb.grid(row=2, column=1, pady=(10, 5), sticky="w")

    # ==== 執行按鈕 ====
    btn_run = ttk.Button(
        main_frame,
        text="▶ 執行",
        width=18,
        style="Accent.TButton"
    )
    btn_run.grid(row=3, column=0, columnspan=2, pady=25)

    # ==== 日誌輸出 ====
    log_box = ScrolledText(
        main_frame,
        width=70,
        height=10,
        wrap="word",
        state="disabled",
        font=("Consolas", 11)
    )
    log_box.grid(row=4, column=0, columnspan=2, pady=(10, 0))

    # ==== Button 動作 ====
    def on_run():
        btn_run.configure(state="disabled", text="處理中...")
        root.update_idletasks()
        try:
            run_task(create_csv=bool(var_create_csv.get()), money=var_money.get(), log_widget=log_box)
        except Exception as e:
            messagebox.showerror("錯誤", str(e))
            append_log(log_box, f"❌ 錯誤：{e}")
        finally:
            btn_run.configure(state="normal", text="▶ 執行")

    btn_run.configure(command=on_run)

    # ==== 美化風格 ====
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=("Microsoft JhengHei", 13))
    style.configure("Accent.TButton", font=("Microsoft JhengHei", 13, "bold"), padding=8)

    root.mainloop()


if __name__ == "__main__":
    main()
