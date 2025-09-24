# uv + GitHub によるコード開発デモ

GitHubではこのようにマークダウン形式でドキュメントをかくことができます。

# 環境整備のやり方

このリポジトリはPython用パッケージ管理ツール`uv`の使用が前提となっています。

Macの場合、uvは以下のコマンドでインストール可能です。

```zsh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

`uv`が入ったら、このリポジトリを自分PC（ローカル）へ落としてくる。

gitが入っていれば以下のコマンドでローカルに持ってくること（クローン）ができます。

```zsh
git clone https://github.com/FumiHubCNS/demo.git
```

すると`demo`というディレクトリが作成されているはずなので、以下のコマンドで準備完了です。

```zsh
cd demo
uv sync 
```

あとは以下のコマンで実行が可能です。

```
uv run python src/demo/draw_ktuy.py
```

うまく整備できていたら核図表が描画されます。