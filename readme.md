# in_campus_print_gui

大学キャンパス内のプリントサービスを簡単に利用できるGUIアプリケーションです。  
PDFファイルの選択、印刷設定、送信までを直感的なUIで操作できます。

---

## 主な機能

- PDFファイルの選択（ディレクトリツリーまたはパス入力）
- 用紙サイズ、両面/片面、ページレイアウト等の印刷設定
- 設定内容の保存と送信
- レイアウトのプレビュー表示

---

## 必要要件

- Python 3.8 以上
- [Textual](https://github.com/Textualize/textual)
- campus_print モジュール（`campus_print.in_campus_print`, `campus_print.settings`）

---

## インストール

```sh
pip install textual
# campus_print モジュールも適宜インストールまたは配置してください
```

---

## 使い方

1. このリポジトリをクローンまたはダウンロードします。
2. 必要な認証情報や設定ファイル（例: `key.key`, `userdata.txt` など）を `.gitignore` に従い配置します。
3. アプリを起動します。

```sh
python main.py
```

4. 画面左側で印刷したいPDFファイルと各種設定を選択します。
5. 「送信」ボタンを押すと、設定内容が保存され、印刷ジョブが送信されます。
6. 右側にレイアウトのプレビューや送信結果が表示されます。

---

## ファイル構成

- `main.py` … アプリ本体
- `css/style.tcss` … UIスタイル定義
- `.gitignore` … 認証情報や一時ファイルの除外設定

---

## 注意事項

- campus_print モジュールが別途必要です（[こちら](https://github.com/ktsgsg/in_campus_print/tree/v2) から取得可能）。
- 本アプリは学内プリントサービス専用です。

---

## ライセンス

本リポジトリの内容は、各ファイルのヘッダー等に記載されたライセンスに従います。