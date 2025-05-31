# Azure Text-to-Speech プログラム

Azure AI ServiceのText-to-Speech機能を使用して、テキストを音声に変換するPythonプログラムです。

## セットアップ

1. 依存関係をインストール:
```bash
uv sync
```

2. Azure Speech Serviceのキーを設定:
```bash
cp .env.example .env
# .envファイルを編集してAzure Speech Serviceのキーとリージョンを設定
```

## 使用方法

### 基本的な使用方法

```python
from tts_speech import AzureTTS

# TTSインスタンスを作成
tts = AzureTTS(speech_key="your_key", service_region="japaneast")

# テキストを音声に変換（スピーカーから再生）
tts.text_to_speech("こんにちは、世界！")

# 音声ファイルとして保存
tts.text_to_speech("こんにちは、世界！", output_file="hello.wav")
```

### コマンドラインから実行

```bash
# 環境変数を設定
export AZURE_SPEECH_KEY="your_speech_service_key"
export AZURE_SPEECH_REGION="japaneast"

# プログラムを実行
uv run tts_speech.py
```

## 音声の種類

- `ja-JP-NanamiNeural` - 日本語女性音声（デフォルト）
- `ja-JP-KeitaNeural` - 日本語男性音声
- その他多数の音声が利用可能

## 必要な設定

1. Azure Portal でSpeech Serviceリソースを作成
2. APIキーとリージョンを取得
3. 環境変数またはプログラム内で設定