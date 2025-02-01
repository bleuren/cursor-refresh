# Cursor 重置工具

這是一個用於重置 Cursor 編輯器機器碼並自動生成新電子郵件別名的工具。此工具可以幫助用戶重新開始 Cursor 的免費試用期。

## 功能特點

- 自動更新 Cursor 的機器識別碼
- 自動管理 addy.io[https://addy.io] 郵件別名
- 自動終止現有的 Cursor 程序
- 完整的日誌記錄功能

## 系統需求

- Python 3.6 或更高版本
- macOS 作業系統
- 有效的 addy.io API 金鑰

## 安裝步驟

1. 克隆儲存庫：
```bash
git clone https://github.com/bleuren/cursor-refresh
cd cursor-refresh
```

2. 安裝必要的套件：
```bash
pip install -r requirements.txt
```

3. 設定環境變數：
```bash
cp .env.example .env
```

4. 修改 `.env` 檔案中的環境變數：
```bash
ADDY_API_KEY=你的API金鑰
```

## 使用方法

1. 確保 Cursor 編輯器已關閉
2. 執行程式：
```bash
python main.py
```

程式會自動：
- 終止所有 Cursor 程序
- 更新機器識別碼
- 刪除舊的 addy.io 別名
- 建立新的郵件別名

## 注意事項

- 請確保在執行程式前已備份重要資料
- 需要有效的 addy.io API 金鑰
- 此工具僅支援 macOS 系統
- 使用此工具時請遵守相關服務條款

## 免責聲明

此工具僅供教育和研究目的使用。使用者需自行承擔使用風險，並確保遵守相關服務的使用條款。