# 🎙️ Local Whisper Speech-to-Text

> 浏览器录音 → 本地 Whisper 转文字，全程离线、无需联网、保护隐私。

在 Mac 上通过 Streamlit 网页界面录音，调用 `faster-whisper` 模型进行本地语音识别。所有音频数据停留在本机，不会上传到任何外部服务器。

## 效果

- 打开浏览器 → 点击录音 → 自动转文字
- 支持多语言（中文、英文、日语等）
- 支持不同大小的模型（tiny ~ large-v3），速度和准确度自选

## 前置条件

- macOS（Intel 或 Apple Silicon 均可）
- Python 3.11 / 3.12
- 麦克风权限（浏览器会弹出授权提示）

## 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/<your-username>/whisper-stt.git
cd whisper-stt

# 2. 创建虚拟环境并安装依赖
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. 启动
streamlit run app.py
```

在浏览器打开终端输出的地址（默认 `http://localhost:8501`），点击录音按钮即可。

## 配置 HTTPS（可选）

Chrome 等浏览器对 `http://localhost` 会显示「不安全」提示，可以通过配置本地 SSL 证书消除：

### 方法一：mkcert（推荐）

```bash
# 安装 mkcert
brew install mkcert
mkcert -install     # 需要输入一次 Mac 密码
mkcert localhost 127.0.0.1

# 启动
streamlit run app.py \
  --server.sslCertFile=localhost.pem \
  --server.sslKeyFile=localhost-key.pem
```

### 方法二：OpenSSL（无需额外安装）

```bash
openssl req -x509 -newkey rsa:4096 \
  -keyout localhost.key -out localhost.crt \
  -days 365 -nodes -subj "/CN=localhost"

# 需要将 localhost.crt 添加到系统钥匙串并设为信任
# 打开钥匙串访问 → 导入证书 → 双击设为「始终信任」

streamlit run app.py \
  --server.sslCertFile=localhost.crt \
  --server.sslKeyFile=localhost.key
```

## 模型选择

| 模型 | 速度 | 准确度 | 内存占用 |
|------|------|--------|----------|
| tiny | 最快 | 较低 | ~1GB |
| base | 快 | 一般 | ~1GB |
| small | 适中 | 良好 | ~2GB |
| medium | 较慢 | 优秀 | ~5GB |
| large-v3 | 最慢 | 最佳 | ~10GB |

可在网页左侧边栏随时切换模型。

## 自定义

- **语言检测**：留空可自动检测，指定语言代码（如 `en`、`ja`）可提升准确度
- **Vad 过滤**：如需过滤静音段落，可在 `model.transcribe()` 中添加 `vad_filter=True`
- **设备指定**：`device="auto"` 会自动选择 GPU/MPS/CPU，也可手动设为 `"cpu"`

## 技术栈

- [Streamlit](https://streamlit.io/) — 网页框架
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) — CTranslate2 加速的 Whisper 推理
- [Whisper](https://github.com/openai/whisper) — OpenAI 语音识别模型
