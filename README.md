# 使用說明（程式執行順序）

本專案提供 CLI 與 GUI 兩種操作介面，執行順序為：啟動程式後依互動指示呼叫 [exchange.py](exchange.py) 的 `def build_csv()` 產生/更新 [usd_jpy_history.csv](usd_jpy_history.csv)，接著依輸入選擇繪圖，使用 [graph.py](graph.py) 的繪圖函式繪製匯率圖表。

## 環境需求
- Python 3.9+（建議 3.10+）
- 已安裝套件：requests、pandas、matplotlib

安裝指令（如尚未安裝）：
```bash
pip install -U requests pandas matplotlib
```

## 執行步驟

### 方法一：GUI 介面（建議）
1. 在專案根目錄執行：
   ```bash
   python gui_main.py
   ```
2. 勾選「更新並寫出 CSV」選項（首次使用建議勾選）
3. 選擇幣別（USD / JPY / GBP / ALL）
4. 點擊「▶ 執行」按鈕
5. 查看日誌輸出與繪製的圖表

### 方法二：命令列介面
1. 在專案根目錄執行：
   ```bash
   python main.py
   ```
2. 依提示輸入是否更新匯率資料（Y/N）
   - 輸入 Y：由 [exchange.py](exchange.py) 的 `def build_csv()` 下載/更新資料並覆寫 [usd_jpy_history.csv](usd_jpy_history.csv)
   - 輸入 N：使用現有的 [usd_jpy_history.csv](usd_jpy_history.csv)
3. 依提示輸入幣別（USD / JPY / GBP / ALL）
   - USD：顯示最近期美元資料並繪製匯率圖
   - JPY：顯示最近期日圓資料並繪製匯率圖
   - GBP：顯示最近期英鎊資料並繪製匯率圖
   - ALL：同時顯示最新資料並依序繪製三張圖
4. 關閉圖表視窗後，程式結束。如需再次查詢，重複步驟 1。

## 主要檔案與職責
- [gui_main.py](gui_main.py)：**建議使用的 GUI 介面**（tkinter 實作，包含日誌視窗與完整功能）
- [main.py](main.py)：CLI 命令列介面，提供互動式操作
- [exchange.py](exchange.py)：資料抓取與 CSV 產生（`def build_csv()`）
- [graph.py](graph.py)：繪圖函式（`plot_graph_usd()`、`plot_graph_jpy()`、`plot_graph_gbp()`）
- [usd_jpy_history.csv](usd_jpy_history.csv)：資料輸出檔（更新資料後產生/覆寫）

## 注意事項
- 首次使用建議選擇更新（Y）以產生 [usd_jpy_history.csv](usd_jpy_history.csv)；之後可視需求再更新。

