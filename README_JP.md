<h1 align="center">x-search-cli</h1>

<p align="center">
  Hermes x_search_tool の実用的な CLI ラッパー
</p>

<p align="center">
  <strong>日本語</strong> | <a href="./README.md">English</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/uv-managed-6E56CF" alt="uv">
  <img src="https://img.shields.io/badge/xAI-Responses_API-black" alt="xAI Responses API">
</p>

## 概要

X Premium ユーザーは [Hermes Agent](https://github.com/nousresearch/hermes-agent) 経由で
X 検索を使えるようになりました。
この CLI は Hermes Agent の認証情報を再利用し、xAI Responses API 経由で `x_search` ツールを呼び出し、
X 内の情報を検索して Grok の要約付きで返します。

## 特徴

- Hermes Agent を起動する必要がありません。
- 既定モデルを `grok-4.20-reasoning` から `grok-4.3` に変更しています。
  - 応答時間が短くなります。
  - 回答が短めになります。
- グローバルインストールでき、どのディレクトリからでも呼び出せます。

## 前提

- `uv`
- `hermes-agent` で認証済みの `xai-oauth`、または `XAI_API_KEY`

まだ認証していない場合は、先に以下を実行してください。

認証例:

```sh
uvx --from hermes-agent hermes auth add xai-oauth
```

## セットアップ

どのディレクトリからでも使えるようにインストールする:

```sh
./install_x_search.sh
x-search 'What are people saying about xAI on X?'
```

同じことを手動で行う:

```sh
uv tool install --editable /path/to/x-search-cli
x-search 'What are people saying about xAI on X?'
```

このリポジトリ内だけで試す:

```sh
uv run x-search 'What are people saying about xAI on X?'
```

Hermes 環境から単発で呼び出す:

```sh
uvx --from hermes-agent python x_search_cli.py \
  'What are people saying about xAI on X?'
```

## Agent Skill

このリポジトリには Agent Skills 形式の `SKILL.md` も同梱しています。

- スキルファイル: [`x-search-skill/SKILL.md`](x-search-skill/SKILL.md)
- 参照ファイル: [`x-search-skill/references/COMMANDS.md`](x-search-skill/references/COMMANDS.md)
- スキル名: `x-search-skill`
- 想定用途:
  - X 上の反応を要約したい
  - 引用 URL 付きで X 投稿を集めたい
  - ハンドル、日付、画像、動画で X 検索を絞りたい
- Agent向け運用ルール:
  - X を主ソースとして扱い、補足が必要なときだけ非 X ソースを足す
  - 回答前に期間、話題、証拠の十分さが依頼と一致しているか確認する
  - 未導入、引数不正、認証不備、結果が空・広すぎる・根拠が弱い場合を分けて扱う

このスキルは `x-search` コマンドがインストール済みであることを前提に、
Agent がローカルの `x-search` CLI を呼び出すための運用ガイドです。

`x-search-skill/SKILL.md` が本体の指示ファイルで、`x-search-skill/references/COMMANDS.md` は
必要なときだけ読む補助的なコマンド集です。スキルを配置するときは、
リンク先の `references/` ディレクトリも一緒に保持してください。

スキルとして使う場合は、`x-search-skill/SKILL.md` を Agent Skills のスキルディレクトリに配置するか、
このリポジトリを参照できる状態で読み込んでください。

## 使い方

基本:

```sh
x-search 'What are people saying about xAI on X?'
```

この CLI の既定モデルは `grok-4.3` です。

モデルを明示指定する:

```sh
x-search --model grok-4.20-reasoning 'What are people saying about xAI on X?'
```

JSON 全体を出力する:

```sh
x-search --mode json 'What are people saying about xAI on X?'
```

引用 URL だけを出力する:

```sh
x-search --mode urls 'What are people saying about xAI on X?'
```

引用番号付き一覧を出力する:

```sh
x-search --mode citations 'What are people saying about xAI on X?'
```

ハンドルや日付で絞る:

`YYYY-MM-DD` は実際の日付に置き換えてから実行してください。

```sh
x-search \
  --model grok-4.3 \
  --allowed-handle xai \
  --allowed-handle grok \
  --from-date YYYY-MM-DD \
  --to-date YYYY-MM-DD \
  'Summarize recent reactions on X'
```

標準入力からクエリを渡す:

```sh
cat prompt.txt | x-search --mode answer
```

画像や動画の理解を有効にする:

```sh
x-search \
  --image \
  --video \
  'Find posts discussing a demo video and summarize reactions'
```

## オプション

- `--mode answer|json|citations|urls`
- `--model MODEL`
- `--allowed-handle` と `--excluded-handle`
- `--from-date YYYY-MM-DD`
- `--to-date YYYY-MM-DD`
- `--image`
- `--video`

## 補足

- `install_x_search.sh` は既存インストールを `--reinstall` で更新します
- `--model` の既定値は `grok-4.3` です
- `--model` は Hermes の `x_search.model` をその実行時だけ上書きします
- Hermes 側の既定値 `grok-4.20-reasoning` より、この CLI の既定値が優先されます
- モデル、タイムアウト、リトライ回数は Hermes 側の `x_search` 設定に従います
- 認証は `xai-oauth` または `XAI_API_KEY` から自動解決されます

## 謝辞

Python からの利用方法を詳しく解説した X の記事を書いてくださった @MtkN1XBt に感謝します。
