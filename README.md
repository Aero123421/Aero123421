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

3.  **Discordボットの作成とトークン取得:**
    -   [Discord Developer Portal](https://discord.com/developers/applications) にアクセスします。
    -   右上の「New Application」ボタンをクリックし、アプリケーション名（例: My Gemini Bot）を入力して「Create」をクリックします。
    -   作成されたアプリケーションのページで、左側のメニューから「Bot」を選択します。
    -   「Add Bot」ボタンをクリックし、表示される確認ダイアログで「Yes, do it!」を選択します。
    -   ボットの設定ページが表示されます。「TOKEN」セクションにある「Copy」ボタンをクリックしてボットトークンをコピーし、安全な場所に保管してください。このトークンは後述の `.env` ファイルで使用します。
        -   **注意: このトークンは絶対に他人に教えたり、公開したりしないでください。**
    -   同じページ内の「Privileged Gateway Intents」の項目までスクロールします。
    -   「MESSAGE CONTENT INTENT」のトグルスイッチをオン（有効化）にします。変更を保存するボタンが表示された場合はクリックしてください（通常、変更は自動的に保存されます）。この設定が有効でないと、ボットはユーザーからのメッセージ内容を読み取ることができません。

4.  **ボットをサーバーに招待する:**
    -   Discord Developer Portalの同じアプリケーションページで、左側のメニューから「OAuth2」を選択し、その下のサブメニューから「URL Generator」を選択します。
    -   「SCOPES」セクションで、「`bot`」のチェックボックスを選択します。
    -   「BOT PERMISSIONS」セクションが表示されるので、ボットに必要な権限を選択します。最低限、以下の権限が必要です:
        -   `Send Messages` (メッセージを送信)
        -   `Read Message History` (メッセージ履歴を読む)
        -   もしスレッド内でボットを使用する場合は `Send Messages in Threads` (スレッドでメッセージを送信) も選択してください。
    -   ページ下部に「GENERATED URL」が生成されるので、そのURLをコピーします。
    -   コピーしたURLをブラウザのアドレスバーに貼り付けてアクセスします。
    -   ボットを追加したいDiscordサーバーを選択し、「認証」ボタンをクリックします。指示に従って認証を完了してください。

5.  **`.env` ファイルの作成と設定:**
    -   プロジェクトのルートディレクトリに `.env` という名前の新しいファイルを作成します。
    -   `.env` ファイルを開き、以下の形式でAPIキーとDiscordボットトークンを追加します:
        ```env
        DISCORD_BOT_TOKEN=あなたのDiscordボットトークン
        GEMINI_API_KEY=あなたのGemini APIキー
        TAVILY_API_KEY=あなたのTavily APIキー
        ```
    -   `あなたのDiscordボットトークン` には、ステップ3でコピーした実際のボットトークンを貼り付けます。
    -   `あなたのGemini APIキー`, `あなたのTavily APIキー` の部分を、実際のAPIキーに置き換えてください。

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
