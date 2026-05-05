# 🎵 Music Bot Client

這是一個串接 Lavalink Server 的 Discord 音樂機器人，提供音樂播放、暫停、繼續等功能。

---

## 📋 目錄

- [快速開始](#快速開始)
- [環境設定](#環境設定)
- [指令列表](#指令列表)
- [相關資源](#相關資源)

---

## 🚀 快速開始

### 1️⃣ 環境準備

需要準備一個 `.env` 檔案在專案根目錄：

```env
DISCORD_TOKEN=your_discord_bot_token_here

LAVALINK_HOST=127.0.0.1
LAVALINK_PORT=2333
LAVALINK_PASSWORD=your_lavalink_password
LAVALINK_SECURE=false
```

### 2️⃣ 安裝依賴

```bash
uv sync
```

### 3️⃣ 啟動機器人

```bash
uv run main.py
```

---

## ⚙️ 環境設定

| 環境變數 | 說明 | 預設值 |
|---------|------|--------|
| `DISCORD_TOKEN` | Discord Bot Token | ✅ 必需 |
| `LAVALINK_HOST` | Lavalink 伺服器位址 | `127.0.0.1` |
| `LAVALINK_PORT` | Lavalink 伺服器埠號 | `2333` |
| `LAVALINK_PASSWORD` | Lavalink 伺服器密碼 | ✅ 必需 |
| `LAVALINK_SECURE` | 是否使用安全連線 | `false` |

---

## 🎛️ 指令列表

**指令前綴：** `0.0`

### 基本指令

| 指令 | 說明 |
|------|------|
| `0.0help` | 顯示所有可用指令 |
| `0.0join` | 加入你所在的語音頻道 |
| `0.0leave` | 離開語音頻道 |

### 音樂控制

| 指令 | 說明 |
|------|------|
| `0.0play` | 播放音樂 |
| `0.0pause` | 暫停播放 |
| `0.0resume` | 繼續播放 |
| `0.0stop` | 停止播放 |

### 使用說明

```
0.0help                    # 查看所有指令
0.0help [指令名稱]         # 查看特定指令的詳細說明
0.0help [類別]            # 查看特定類別的指令
```

---

## 📚 相關資源

- [Discord.py 官方文檔](https://discordpy.readthedocs.io/)
- [Wavelink 文檔](https://wavelink.readthedocs.io/)
- [Lavalink 文檔](https://lavalink.dev/)