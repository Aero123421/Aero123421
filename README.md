# Gemini & Tavily 連携 Discord AIボット

## 説明
このDiscordボットは、Gemini APIと連携して知的な応答を生成し、Tavily APIを使用してウェブ検索を実行します。ユーザーはDiscord内で直接、情報への迅速なアクセスとAIを活用した会話を利用できます。

## 必要条件
このボットを実行するには、以下が必要です:
- Python 3.8 以降
- Discord ボットトークン (Discord Bot Token)
- Gemini API キー (Gemini API Key)
- Tavily API キー (Tavily API Key)

## セットアップ手順

1.  **リポジトリをクローン:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
    （`<repository_url>` と `<repository_directory>` を実際のリポジトリURLとディレクトリ名に置き換えてください）

2.  **依存関係をインストール:**
    `pip` を使用して必要なPythonライブラリをインストールします:
    ```bash
    pip install -r requirements.txt
    ```

3.  **`.env` ファイルの作成と設定:**
    -   プロジェクトのルートディレクトリに `.env` という名前の新しいファイルを作成します。
    -   `.env` ファイルを開き、以下の形式でAPIキーとDiscordボットトークンを追加します:
        ```env
        DISCORD_BOT_TOKEN=あなたのDiscordボットトークン
        GEMINI_API_KEY=あなたのGemini APIキー
        TAVILY_API_KEY=あなたのTavily APIキー
        ```
    -   `あなたのDiscordボットトークン`, `あなたのGemini APIキー`, `あなたのTavily APIキー` の部分を、実際のトークンとAPIキーに置き換えてください。

## 実行方法

セットアップが完了したら、ターミナルで以下のコマンドを使用してボットを起動できます:
```bash
python bot.py
```
ボットを実行する前に、`.env` ファイルに必要なトークンとキーが正しく設定されていることを確認してください。

## 利用可能なコマンド

ボットはDiscordチャンネルで以下のコマンドに応答します:

-   `!hello`
    -   ボットに挨拶します。
-   `!help`
    -   利用可能なすべてのコマンドとその説明のリストを表示します。
-   `!ask <質問内容>`
    -   Google Gemini APIに質問します。ボットが回答を返します。
    -   例: `!ask フランスの首都は？`
-   `!search <検索クエリ>`
    -   Tavily Search APIを使用してウェブ検索を実行し、結果の要約（通常はタイトルとURL）を表示します。
    -   例: `!search 最新のAIニュース`

## ロギング

ボットは、処理されたコマンド、エラー、APIとのやり取りなど、運用アクティビティを `bot.log` という名前のファイルに記録します。このファイルはプロジェクトのルートディレクトリにあります。トラブルシューティングやボットのアクティビティ監視のために、このログファイルを確認してください。

---

*このREADMEは、Gemini & Tavily連携 Discord AIボットの基本的なセットアップと使用方法を説明するものです。*
