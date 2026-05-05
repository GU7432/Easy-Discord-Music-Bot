# 🎵 Music Bot Client

這是一個串接 Lavalink Server 的 Discord 音樂機器人，提供音樂播放、暫停、繼續等功能。

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

## � Lavalink Server 配置

### 📋 application.yml

Lavalink Server 的主配置文件，要跟 compose.yml 在同一個目錄

已經預先加入了 youtube-plugins

```yaml
server: # REST and WS server
  port: 2333
  address: 0.0.0.0
  http2:
    enabled: false # Whether to enable HTTP/2 support
plugins:
  youtube:
    enabled: true # Whether this source can be used.
    allowSearch: true # Whether "ytsearch:" and "ytmsearch:" can be used.
    allowDirectVideoIds: true # Whether just video IDs can match. If false, only complete URLs will be loaded.
    allowDirectPlaylistIds: true # Whether just playlist IDs can match. If false, only complete URLs will be loaded.
    # The clients to use for track loading. See below for a list of valid clients.
    # Clients are queried in the order they are given (so the first client is queried first and so on...)
    clients:
      - MUSIC
      - ANDROID_VR
      - WEB
      - WEBEMBEDDED 
#  name: # Name of the plugin
#    some_key: some_value # Some key-value pair for the plugin
#    another_key: another_value
lavalink:
  plugins:
    - dependency: "dev.lavalink.youtube:youtube-plugin:1.18.1"
      snapshot: false # Set to true if you want to use a snapshot version.
#    - dependency: "com.github.example:example-plugin:1.0.0" # required, the coordinates of your plugin
#      repository: "https://maven.example.com/releases" # optional, defaults to the Lavalink releases repository by default
#      snapshot: false # optional, defaults to false, used to tell Lavalink to use the snapshot repository instead of the release repository
#  pluginsDir: "./plugins" # optional, defaults to "./plugins"
#  defaultPluginRepository: "https://maven.lavalink.dev/releases" # optional, defaults to the Lavalink release repository
#  defaultPluginSnapshotRepository: "https://maven.lavalink.dev/snapshots" # optional, defaults to the Lavalink snapshot repository
  server:
    password: "example"
    sources:
      # The default Youtube source is now deprecated and won't receive further updates. Please use https://github.com/lavalink-devs/youtube-source#plugin instead.
      youtube: false
      bandcamp: true
      soundcloud: true
      twitch: true
      vimeo: true
      nico: true
      http: true # warning: keeping HTTP enabled without a proxy configured could expose your server's IP address.
      local: false
    filters: # All filters are enabled by default
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
    nonAllocatingFrameBuffer: false # Setting to true reduces the number of allocations made by each player at the expense of frame rebuilding (e.g. non-instantaneous volume changes)
    bufferDurationMs: 400 # The duration of the NAS buffer. Higher values fare better against longer GC pauses. Duration <= 0 to disable JDA-NAS. Minimum of 40ms, lower values may introduce pauses.
    frameBufferDurationMs: 5000 # How many milliseconds of audio to keep buffered
    opusEncodingQuality: 10 # Opus encoder quality. Valid values range from 0 to 10, where 10 is best quality but is the most expensive on the CPU.
    resamplingQuality: LOW # Quality of resampling operations. Valid values are LOW, MEDIUM and HIGH, where HIGH uses the most CPU.
    trackStuckThresholdMs: 10000 # The threshold for how long a track can be stuck. A track is stuck if does not return any audio data.
    useSeekGhosting: true # Seek ghosting is the effect where whilst a seek is in progress, the audio buffer is read from until empty, or until seek is ready.
    youtubePlaylistLoadLimit: 6 # Number of pages at 100 each
    playerUpdateInterval: 5 # How frequently to send player updates to clients, in seconds
    youtubeSearchEnabled: true
    soundcloudSearchEnabled: true
    soundcloudFilterOutPreviewTracks: false
    gc-warnings: true
    #ratelimit:
      #ipBlocks: ["1.0.0.0/8", "..."] # list of ip blocks
      #excludedIps: ["...", "..."] # ips which should be explicit excluded from usage by lavalink
      #strategy: "RotateOnBan" # RotateOnBan | LoadBalance | NanoSwitch | RotatingNanoSwitch
      #searchTriggersFail: true # Whether a search 429 should trigger marking the ip as failing
      #retryLimit: -1 # -1 = use default lavaplayer value | 0 = infinity | >0 = retry will happen this numbers times
    #youtubeConfig: # Required for avoiding all age restrictions by YouTube, some restricted videos still can be played without.
      #email: "" # Email of Google account
      #password: "" # Password of Google account
    #httpConfig: # Useful for blocking bad-actors from ip-grabbing your music node and attacking it, this way only the http proxy will be attacked
      #proxyHost: "localhost" # Hostname of the proxy, (ip or domain)
      #proxyPort: 3128 # Proxy port, 3128 is the default for squidProxy
      #proxyUser: "" # Optional user for basic authentication fields, leave blank if you don't use basic auth
      #proxyPassword: "" # Password for basic authentication
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
#  tags:
#    some_key: some_value
#    another_key: another_value

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

### 🐋 compose.yml

Docker Compose 配置文件，用於快速部署 Lavalink Server：

```yaml
services:
  lavalink:
    # 固定使用 Lavalink v4 版本，並使用 alpine 變體以減少映像檔大小
    image: ghcr.io/lavalink-devs/lavalink:4-alpine
    container_name: lavalink
    restart: unless-stopped
    environment:
      # 在這裡設定 Java 選項（6GB heap 記憶體）
      - _JAVA_OPTIONS=-Xmx6G
      # 設定 Lavalink 伺服器埠號
      # - SERVER_PORT=2333
      # 設定 Lavalink 密碼
      # - LAVALINK_SERVER_PASSWORD=youshallnotpass
    volumes:
      # 掛載同一個目錄下的 application.yml；如果你想改用環境變數，請移除下面這行
      - ./application.yml:/opt/Lavalink/application.yml
      # 在重啟之間保留 plugins，請確認已建立資料夾，並設定好上面提到的正確權限與 user/group id
      - ./plugins/:/opt/Lavalink/plugins/
    networks:
      - lavalink
    expose:
      # Lavalink 會暴露 2333 埠給其他容器連線使用（這裡只是作為文件說明用途）
      - 2333
    ports:
      # 只有當你想讓 Lavalink 從容器外部存取時才需要這個；請注意這會把 Lavalink 暴露到網際網路
      - "2333:2333"
      # 如果你想限制只能從本機 localhost 存取
      # - "127.0.0.1:2333:2333"
networks:
  # 建立一個名為 lavalink 的網路，你可以把其他容器加入這個網路，讓它們可以存取 Lavalink
  lavalink:
    name: lavalink
```

### 🚀 啟動 Lavalink Server

執行

```bash
docker compose up -d
```

---

## 📚 相關資源

- [Discord.py 官方文檔](https://discordpy.readthedocs.io/)
- [Wavelink 文檔](https://wavelink.readthedocs.io/)
- [Lavalink 文檔](https://lavalink.dev/)