import requests
import csv

url = "https://cpx.cbc.gov.tw/API/DataAPI/Get?FileName=BP01M01"
res = requests.get(url, timeout=10)
res.encoding = "utf-8"

data = res.json()
sets = []
try:
    sets = data['data']['dataSets']
except Exception as e:
    print("[錯誤] 解析API結構失敗:", e)
    exit(1)

rows_for_csv = []
for row in sets:
    if len(row) >= 3:
        period = str(row[0])
        # 僅存大於 2000M1
        if period > "2000M1":
            rows_for_csv.append([row[0], row[1], row[2]])

with open("usd_jpy_history.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['Period', 'NTD/USD', 'JPY/USD'])
    writer.writerows(rows_for_csv)

print("已將Period > 2000M1的 NTD/USD, JPY/USD三欄存入 usd_jpy_history.csv")
for row in rows_for_csv[:10]:
    print(f"Period: {row[0]}, NTD/USD: {row[1]}, JPY/USD: {row[2]}")