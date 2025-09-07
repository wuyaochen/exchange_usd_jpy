import pandas as pd
from graph import plot_graph_usd, plot_graph_jpy
from excahnge import build_csv

def run():
    exchange_update = input("是否更新匯率資料(目前最新為2025年8月資料):(Y/N)")
    if exchange_update.upper() == "Y":
        update_data = True
    else:
        update_data = False
    build_csv(min_period = "2000M1", create_csv=update_data)

    df_csv = pd.read_csv("usd_jpy_history.csv", encoding="utf-8-sig")
    df_csv["Period"] = pd.to_datetime(df_csv['Period'].str.replace('M', '-'),
                         format='%Y-%m')

    money = input("選擇你想查的幣值 (USD 或 JPY 或 ALL): ").strip().upper()

    if money == 'USD':
        selected = df_csv[['Period', 'NTD/USD']]
        print(selected.tail().to_string(index=False))
        plot_graph_usd(df_csv, show=True)
    elif money == 'JPY':
        selected = df_csv[['Period', 'NTD/JPY']]
        print(selected.tail().to_string(index=False))
        plot_graph_jpy(df_csv, show=True)
    elif money == 'ALL':
        print(df_csv.tail().to_string(index=False))
        plot_graph_usd(df_csv, show=False)
        plot_graph_jpy(df_csv, show=True)

    else:
        print("輸入無效，請輸入 USD 或 JPY 或 ALL")

if __name__ == "__main__":
    run()
