# 使用說明（程式執行順序）

本專案的執行順序為：先由 [main.py](main.py) 啟動，於 [def run()](main.py:5) 依互動指示呼叫 [excahnge2.py](excahnge2.py) 的 [def build_csv()](excahnge2.py:10) 產生/更新 [usd_jpy_history.csv](usd_jpy_history.csv)，接著依輸入選擇繪圖，分別使用 [graph.py](graph.py) 的 [def plot_graph_usd()](graph.py:5) 或 [def plot_graph_jpy()](graph.py:34)。

## 環境需求
- Python 3.9+（建議 3.10+）
- 已安裝套件：requests、pandas、matplotlib

安裝指令（如尚未安裝）：
```bash
pip install -U requests pandas matplotlib
```

## 執行步驟
1. 在專案根目錄執行：
   ```bash
   python main.py
   ```
2. 依提示輸入是否更新匯率資料（Y/N）
   - 輸入 Y：由 [excahnge2.py](excahnge2.py) 的 [def build_csv()](excahnge2.py:10) 下載/更新資料並覆寫 [usd_jpy_history.csv](usd_jpy_history.csv)
   - 輸入 N：使用現有的 [usd_jpy_history.csv](usd_jpy_history.csv)
3. 依提示輸入幣別（USD / JPY / ALL）
   - USD：顯示最近期美元資料並繪製匯率圖（呼叫 [graph.py](graph.py) 的 [def plot_graph_usd()](graph.py:5)）
   - JPY：顯示最近期日圓資料並繪製匯率圖（呼叫 [graph.py](graph.py) 的 [def plot_graph_jpy()](graph.py:34)）
   - ALL：同時顯示最新資料並依序繪製兩張圖（先 [def plot_graph_usd()](graph.py:5)，再 [def plot_graph_jpy()](graph.py:34)）
4. 關閉圖表視窗後，程式結束。如需再次查詢，重複步驟 1。

## 主要檔案與職責
- [main.py](main.py)：互動式啟動點，流程由 [def run()](main.py:5) 控制（更新資料 -> 讀取 [usd_jpy_history.csv](usd_jpy_history.csv) -> 選擇繪圖）
- [excahnge2.py](excahnge2.py)：資料抓取與 CSV 產生（[def build_csv()](excahnge2.py:10)）
- [graph.py](graph.py)：繪圖函式（[def plot_graph_usd()](graph.py:5)、[def plot_graph_jpy()](graph.py:34)）
- [exchange.py](exchange.py)：舊版抓取腳本（目前非主流程）
- [usd_jpy_history.csv](usd_jpy_history.csv)：資料輸出檔（更新資料後產生/覆寫）

## 注意事項
- 首次使用建議選擇更新（Y）以產生 [usd_jpy_history.csv](usd_jpy_history.csv)；之後可視需求再更新。
