import requests
import csv

def _parse_float(x):
    try:
        return float(x)
    except Exception:
        return None

def build_csv(min_period = "2000M1", create_csv = False):
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
            if period > min_period:
                ntd_usd_raw = row[1]
                jpy_usd_raw = row[2]
                ntd_usd = _parse_float(ntd_usd_raw)
                jpy_usd = _parse_float(jpy_usd_raw)
                ntd_jpy = None
                if ntd_usd not in (None, 0.0) and jpy_usd is not None:
                    ntd_jpy = ntd_usd / jpy_usd
                rows_for_csv.append([
                    row[0],
                    ntd_usd_raw,
                    f"{ntd_jpy:.6f}" if ntd_jpy is not None else ""
                ])
    if create_csv:
        with open("usd_jpy_history.csv", "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(['Period', 'NTD/USD', 'NTD/JPY'])
            writer.writerows(rows_for_csv)

    print("已將Period > 2000M1的 NTD/USD, JPY/NTD三欄存入 usd_jpy_history.csv")
    for row in rows_for_csv[:10]:
        print(f"Period: {row[0]}, NTD/USD: {row[1]}, JPY/NTD: {row[2]}")

def main():
    build_csv(min_period="2000M1")

if __name__ == "__main__":
    main()