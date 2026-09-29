# API設計書

## 概要

FastAPI で実装したRESTful API。  
ベースURL：`http://localhost:8000`（ローカル） / `http://<EC2パブリックIP>:8000`（AWS）  
API仕様の自動生成ドキュメント：`/docs`（Swagger UI）

---

## エンドポイント一覧

### HTMLルート（Jinja2テンプレートを返す）

| メソッド | パス | 説明 |
|---|---|---|
| GET | `/` | ダッシュボード画面 |
| GET | `/expenses/new` | 支出登録フォーム画面 |
| POST | `/expenses/new` | 支出登録（フォーム送信→リダイレクト） |
| GET | `/incomes/new` | 収入登録フォーム画面 |
| POST | `/incomes/new` | 収入登録（フォーム送信→リダイレクト） |

### 支出 API（`/expenses`）

| メソッド | パス | 説明 | ステータスコード |
|---|---|---|---|
| GET | `/expenses/` | 支出一覧取得 | 200 |
| GET | `/expenses/{id}` | 支出1件取得 | 200 / 404 |
| POST | `/expenses/` | 支出登録 | 201 |
| PUT | `/expenses/{id}` | 支出更新 | 200 / 404 |
| DELETE | `/expenses/{id}` | 支出削除 | 204 / 404 |

### 収入 API（`/incomes`）

| メソッド | パス | 説明 | ステータスコード |
|---|---|---|---|
| GET | `/incomes/` | 収入一覧取得 | 200 |
| GET | `/incomes/{id}` | 収入1件取得 | 200 / 404 |
| POST | `/incomes/` | 収入登録 | 201 / 409（同月重複時） |
| PUT | `/incomes/{id}` | 収入更新 | 200 / 404 |
| DELETE | `/incomes/{id}` | 収入削除 | 204 / 404 |

---

## リクエスト・レスポンス仕様

### 支出（ExpenseCreate）

```json
{
  "category": "食費",
  "amount": 3000,
  "date": "2026-09-30"
}
```

### 支出レスポンス（ExpenseResponse）

```json
{
  "id": 1,
  "category": "食費",
  "amount": 3000,
  "date": "2026-09-30",
  "created_at": "2026-09-30T12:00:00"
}
```

### 収入（IncomeCreate）

```json
{
  "amount": 250000,
  "month": "2026-09"
}
```

### 収入レスポンス（IncomeResponse）

```json
{
  "id": 1,
  "amount": 250000,
  "month": "2026-09"
}
```

---

## エラーレスポンス

| ステータスコード | 説明 |
|---|---|
| 404 | 指定IDのリソースが存在しない |
| 409 | 同一月の収入が既に登録済み（`POST /incomes/`） |
| 422 | バリデーションエラー（Pydantic） |
