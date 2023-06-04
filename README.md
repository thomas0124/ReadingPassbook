# ReadingPassbook
- 技育camp2023vol4にて作成した図書館の借りた本の合計金額やおすすめ本のレコメンドするWebアプリケーション


# プロジェクトの立ち上げ方

### 1. リポジトリのクローン
```bash
$ git clone https://github.com/thomas0124/ReadingPassbook
```
### 2. 環境の立ち上げ

```
$ docker-compose build
$ docker-compose up
```
もしくは
```
$ flask run
```

# 使様スタック
- Python
- Flask
- OpenCV
- SQLite3
- Docker
# 使用したAPI
- 楽天API
# コーディング規則

### ブランチ名
`feature/#1/create_new_page`
feature/#1/create_components_and_pages

### コミット名
`feat: #1 タイトル`
feat: #1 ボタンコンポーネントの作成

- `chore`
    - タスクファイルなどプロダクションに影響のない修正
- `docs`
    - ドキュメントの更新
- `feat`
    - ユーザー向けの機能の追加や変更
- `fix`
    - ユーザー向けの不具合の修正
- `refactor`
    - リファクタリングを目的とした修正
- `style`
    - フォーマットなどのスタイルに関する修正
- `test`
    - テストコードの追加や修正
(https://zenn.dev/itosho/articles/git-commit-message-2023)

### タスク管理
- GitHub Project