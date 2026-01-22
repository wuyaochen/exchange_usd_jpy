# AI Coding Agent Instructions

## 專案概述
這是一個匯率查詢與視覺化工具，從台灣央行 API 抓取歷史匯率資料（NTD/USD、NTD/JPY、NTD/GBP），並提供 CLI 與 GUI 兩種操作介面。

## 核心架構

### 資料流
1. **資料抓取**：`exchange.py` 的 `build_csv()` 從 `https://cpx.cbc.gov.tw/API/DataAPI/Get?FileName=BP01M01` 獲取 JSON 資料
2. **資料處理**：解析 JSON 並計算匯率（NTD/JPY = NTD/USD ÷ JPY/USD）
3. **CSV 輸出**：寫入 `usd_jpy_history.csv`（編碼：`utf-8-sig`，欄位：Period, NTD/USD, NTD/JPY, NTD/GBP）
4. **視覺化**：`graph.py` 使用 matplotlib 繪製時間序列圖表

### 主要元件
- **`exchange.py`**：資料抓取核心
  - `build_csv(min_period="2000M1", create_csv=False)` - 主要函式
  - `_parse_float(x)` - 安全轉換浮點數
  
- **`graph.py`**：繪圖模組
  - `plot_graph_usd(df_csv, show=True)` - 繪製 NTD/USD 圖表
  - `plot_graph_jpy(df_csv, show=True)` - 繪製 NTD/JPY 圖表
  - `plot_graph_gbp(df_csv, show=True)` - 繪製 NTD/GBP 圖表
  - 所有繪圖函式返回 `(fig, ax)` 並接受 `show` 參數控制是否阻塞顯示

- **`gui_main.py`**：GUI 主程式（推薦使用）
  - tkinter 實作，美化 UI 設計
  - 整合日誌視窗、錯誤處理、進度提示
  - `run_task()` - 核心業務邏輯
  - `append_log()` - 日誌追加函式

- **`main.py`**：CLI 介面
  - 互動式命令列操作
  - `run()` - 主要流程控制

## 關鍵約定與模式

### CSV 格式
- **編碼**：`utf-8-sig`（帶 BOM）- 所有讀寫必須指定此編碼
- **Period 格式**：原始 `YYYYM##` → 處理成 `YYYY-##` → 轉換為 `pd.to_datetime(format='%Y-%m')`
- **欄位順序**：`Period, NTD/USD, NTD/JPY, NTD/GBP`

### Period 處理標準流程
```python
df_csv["Period"] = (
    df_csv["Period"].astype(str)
    .str.strip()
    .str.replace("M", "-", regex=False)
    .str.replace("\uFEFF", "")  # 移除 BOM
)
df_csv["Period"] = pd.to_datetime(df_csv["Period"], format="%Y-%m", errors="coerce")
```

### 繪圖模式
- `show=False` 用於組合多圖（避免阻塞）
- `show=True` 用於最後一張圖或單圖顯示
- ALL 模式：前面圖表用 `show=False`，最後一張用 `show=True`

### 錯誤處理
- `build_csv()` 失敗時會 `exit(1)` - 修改時需注意避免中斷整個流程
- GUI 使用 `try-except` + `messagebox.showerror()` 顯示錯誤
- CLI 使用簡單 print 輸出

## 開發工作流

### 依賴安裝
```bash
pip install -r requirements.txt
```
必要套件：`requests`, `pandas`, `matplotlib`

### 執行方式
```bash
# GUI（推薦）
python gui_main.py

# CLI
python main.py

# 建置執行檔
pyinstaller gui_main.spec
```

### 測試資料流
```python
from exchange import build_csv
build_csv(min_period="2000M1", create_csv=True)  # 產生 CSV
```

## 常見陷阱

1. **Period 字串比較**：`build_csv()` 使用字串比較 `if period > min_period` 而非日期比較
2. **編碼一致性**：CSV 讀寫必須都用 `encoding="utf-8-sig"`
3. **BOM 清理**：讀取後必須 `.str.replace("\uFEFF", "")` 移除 BOM 字元
4. **exit(1) 陷阱**：`build_csv()` 錯誤會直接終止程式，GUI 需要額外處理
5. **show 參數**：多圖繪製時務必正確設定，否則會阻塞 UI

## 修改建議

### 新增幣別
1. 在 `exchange.py` 的 `build_csv()` 中解析新欄位
2. 在 `graph.py` 新增對應的 `plot_graph_xxx()` 函式
3. 更新 GUI/CLI 的 Combobox values
4. 更新 CSV 欄位說明

### 改善錯誤處理
建議將 `build_csv()` 的 `exit(1)` 改為 `raise Exception()`，讓呼叫端決定如何處理錯誤。

### UI 優化
`gui_main.py` 已經是美化版本，包含：
- 置中佈局 (`place(relx=0.5, rely=0.5, anchor="center")`)
- emoji 圖示增強可讀性
- 按鈕狀態管理（處理中...）
- 完整錯誤提示

## 檔案命名歷史
- ~~`excahnge2.py`~~ → `exchange.py`（已修正錯字）
- ~~`gui_mainv2.py`~~ → `gui_main.py`（已合併保留 v2）

## 參考資料
- 央行 API：`https://cpx.cbc.gov.tw/API/DataAPI/Get?FileName=BP01M01`
- PyInstaller 規格：`gui_main.spec`
