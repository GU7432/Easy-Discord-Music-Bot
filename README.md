# Music Bot Client

Discord 音樂機器人，使用 `discord.py`、`wavelink` 串接 Lavalink Server，支援播放、暫停、跳過與播放隊列。

## 功能

- 播放 YouTube / Lavalink 支援的音源
- 暫停、繼續、停止、跳過
- 播放隊列
- Docker / GitHub Actions 建置

## 環境變數

在專案根目錄建立 `.env`：

```env
DISCORD_TOKEN=your_discord_bot_token_here

LAVALINK_HOST=127.0.0.1
LAVALINK_PORT=2333
LAVALINK_PASSWORD=your_lavalink_password
LAVALINK_SECURE=false
```

| 變數 | 說明 | 預設值 |
| --- | --- | --- |
| `DISCORD_TOKEN` | Discord Bot Token | 必填 |
| `LAVALINK_HOST` | Lavalink Server 位址 | `127.0.0.1` |
| `LAVALINK_PORT` | Lavalink Server Port | `2333` |
| `LAVALINK_PASSWORD` | Lavalink Server 密碼 | `youshallnotpass` |
| `LAVALINK_SECURE` | 是否使用 HTTPS 連線 | `false` |

> 如果 bot 跑在 Docker container 裡，而 Lavalink 跑在主機上，`LAVALINK_HOST` 通常要改成 `host.docker.internal`。

## Docker 使用

### 直接執行映像檔

```bash
docker run --env-file .env ghcr.io/gu7432/easy-discord-music-bot:latest
```

### Docker Compose

```yaml
services:
  bot:
    image: ghcr.io/gu7432/easy-discord-music-bot:latest
    container_name: music-bot
    restart: unless-stopped
    env_file:
      - .env
```

### 本機建置

```bash
docker build -t music-bot-client .
docker run --env-file .env music-bot-client
```

## Python 本機執行

需要 Python `3.11`。

```bash
uv sync
uv run main.py
```

## 指令

指令前綴：`0.0`

| 指令 | 說明 |
| --- | --- |
| `0.0help` | 顯示所有可用指令 |
| `0.0join` | 加入你所在的語音頻道 |
| `0.0leave` | 離開語音頻道 |
| `0.0play <歌曲名稱或網址>` | 播放歌曲；播放中時加入隊列 |
| `0.0pause` | 暫停播放 |
| `0.0resume` | 繼續播放 |
| `0.0stop` | 停止播放並清空隊列 |
| `0.0skip` | 跳過目前歌曲 |
| `0.0queue` | 顯示播放隊列 |
| `0.0clear_queue` | 清空播放隊列 |

範例：

```text
0.0play https://youtu.be/LtOJvQ3S0l4
0.0queue
0.0skip
```

## Lavalink Server

### application.yml

`application.yml` 要和 Lavalink 的 `compose.yml` 放在同一個目錄。以下設定已包含 YouTube plugin 範例：

```yaml
server:
  port: 2333
  address: 0.0.0.0
  http2:
    enabled: false

plugins:
  youtube:
    enabled: true
    allowSearch: true
    allowDirectVideoIds: true
    allowDirectPlaylistIds: true
    clients:
      - MUSIC
      - ANDROID_VR
      - WEB
      - WEBEMBEDDED

lavalink:
  plugins:
    - dependency: "dev.lavalink.youtube:youtube-plugin:1.18.1"
      snapshot: false

  server:
    password: "example"
    sources:
      youtube: false
      bandcamp: true
      soundcloud: true
      twitch: true
      vimeo: true
      nico: true
      http: true
      local: false
    filters:
      volume: true
      equalizer: true
      karaoke: true
      timescale: true
      tremolo: true
      vibrato: true
      distortion: true
      rotation: true
      channelMix: true
      lowPass: true
    bufferDurationMs: 400
    frameBufferDurationMs: 5000
    opusEncodingQuality: 10
    resamplingQuality: LOW
    trackStuckThresholdMs: 10000
    useSeekGhosting: true
    youtubePlaylistLoadLimit: 6
    playerUpdateInterval: 5
    youtubeSearchEnabled: true
    soundcloudSearchEnabled: true
    soundcloudFilterOutPreviewTracks: false
    gc-warnings: true
    timeouts:
      connectTimeoutMs: 3000
      connectionRequestTimeoutMs: 3000
      socketTimeoutMs: 3000

metrics:
  prometheus:
    enabled: false
    endpoint: /metrics

sentry:
  dsn: ""
  environment: ""

logging:
  file:
    path: ./logs/
  level:
    root: INFO
    lavalink: INFO
  request:
    enabled: true
    includeClientInfo: true
    includeHeaders: false
    includeQueryString: true
    includePayload: true
    maxPayloadLength: 10000
    beforeRequest: false
  logback:
    rollingpolicy:
      max-file-size: 1GB
      max-history: 30
```

### compose.yml

```yaml
services:
  lavalink:
    image: ghcr.io/lavalink-devs/lavalink:4-alpine
    container_name: lavalink
    restart: unless-stopped
    environment:
      - _JAVA_OPTIONS=-Xmx6G
    volumes:
      - ./application.yml:/opt/Lavalink/application.yml
      - ./plugins/:/opt/Lavalink/plugins/
    networks:
      - lavalink
    ports:
      - "2333:2333"

networks:
  lavalink:
    name: lavalink
```

啟動 Lavalink：

```bash
docker compose up -d
```

如果 bot 和 Lavalink 在同一個 Docker Compose network 裡，`.env` 可設定：

```env
LAVALINK_HOST=lavalink
LAVALINK_PORT=2333
LAVALINK_PASSWORD=example
LAVALINK_SECURE=false
```

## GitHub Actions

專案包含 Docker publish workflow，push 到 `main` 或建立 `v*` tag 時會建置並推送 image 到 GitHub Container Registry。

## 相關資源

- [Discord.py 官方文檔](https://discordpy.readthedocs.io/)
- [Wavelink 文檔](https://wavelink.readthedocs.io/)
- [Lavalink 文檔](https://lavalink.dev/)
