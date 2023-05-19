# line2deepl_azfunction
## What
- Azure function Python(Programing Model V2)で動作するLineの対話型Bot
- botに英語を送ると和訳、日本語を送ると英訳を応答する
- botに画像を送ると英語を抜き出して、英語と和訳を応答する
- LINE, DeepL, AzureVision, ChatGPTを利用します。事前にAPI接続用のコードを取得する必要あり

## 参考1
- https://learn.microsoft.com/ja-jp/azure/azure-functions/functions-reference-python?
- https://developers.line.biz/



## 参考２：Cloneせずに1からAzure function開発環境を作る方法

1. プロジェクトフォルダ作成
    ```
    mkdir プロジェクト名
    ```

2. githubのリモートレポジトリを作成

    githubの右上の+でnew repository作成(選択肢デフォルトのままcreate repository)

    プロジェクトフォルダ内で画面上に出てくるコマンドを実行
    ```
    echo "# xxxx" >> README.md
    git init
    git add README.md
    git commit -m "first commit"
    git branch -M main
    git remote add origin git@github.com:xxxx/xxxxx.git
    git push -u origin main
    ```

4. azure portalにてazure functionをcreate

    - azure portalでリソース作成をクリック
    - 検索窓にfunction か関数　を入力し、関数アプリ/functionを選択
    - デプロイ タブでリモートレポジトリに3で作った指定すると、workflowがgithubにアップロードされる

5. workflowをローカルにpull

    ```
    git pull origin main
    ```

6. vscodeでHTTP Triggerの雛形作成1

    - vscodeでプロジェクトフォルダをオープン
    - 左側のAマークをクリックし、雷+ボタン＞Create HTTP function＞Python(Programing Model V2)＞python3.10
    ```
    function_app.py
    host.json
    requirements.txt
    ```
    等のファイルができる

7. vscodeでHTTP Triggerの雛形作成2
    - さらに雷+ボタン＞HTTP Trigger＞Append to function_app.py(Recommended)をクリック

    api/function_app.pyにHTTP Triggerのコードが追加される

8. 試験
    vscodeで雲マークの上矢印を選択してアップロード、Webサイトの確認
    
    (workflowがあるので、git pushでもok)


9. 必要な接続文字列の設定

    Azure functionの関数アプリ>設定>構成＞接続文字列にて、以下を設定
    |名前|値|種類|
    | ----- | ---- | ----- |
    |COMPUTER_VISION_ENDPOINT|https://****.cognitiveservices.azure.com/|Custom|
    |COMPUTER_VISION_SUBSCRIPTION_KEY|********************************|Custom|
    |DEEPL_AUTH_KEY|xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx:fx|Custom|
    |LINE_CHANNEL_ACCESS_TOKEN|xx略xx|Custom
    |LINE_CHANNEL_SECRET|xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|Custom|
    |OPENAI_API_KEY|sk-xxxxxxxxxxxxxxxxxx|Custom|

    上記の接続文字列は、コード上では"CUSTOMCONNSTR_名前"の環境変数で渡される

    例: LINE_CHANNEL_SECRET = os.environ['CUSTOMCONNSTR_LINE_CHANNEL_SECRET']


