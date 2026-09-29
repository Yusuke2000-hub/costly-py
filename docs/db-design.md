# DB設計書

## 概要

costly-py のデータベースは MySQL 8.4 を採用し、SQLAlchemy（ORM）＋ Alembic（マイグレーション）で管理する。

---

## テーブル一覧

| テーブル名 | 説明 |
|---|---|
| expenses | 支出データ |
| incomes | 収入データ（月ごとに1件） |

---

## テーブル定義

### expenses（支出）

| カラム名 | 型 | NOT NULL | デフォルト | 説明 |
|---|---|---|---|---|
| id | INT | ○ | AUTO_INCREMENT | 主キー |
| category | VARCHAR(100) | ○ | - | 費目（例：食費、光熱費） |
| amount | INT | ○ | - | 金額（円） |
| date | DATE | ○ | - | 支出日 |
| created_at | DATETIME | ○ | utcnow | 登録日時 |

### incomes（収入）

| カラム名 | 型 | NOT NULL | デフォルト | 説明 |
|---|---|---|---|---|
| id | INT | ○ | AUTO_INCREMENT | 主キー |
| amount | INT | ○ | - | 月収（円） |
| month | VARCHAR(7) | ○ | - | 対象月（例：2026-09）、UNIQUE |

---

## ER図

```
┌──────────────────────┐       ┌──────────────────────┐
│       expenses       │       │       incomes        │
├──────────────────────┤       ├──────────────────────┤
│ PK  id         INT   │       │ PK  id         INT   │
│     category VARCHAR │       │     amount     INT   │
│     amount     INT   │       │     month  VARCHAR(7)│
│     date       DATE  │       └──────────────────────┘
│     created_at DATETIME      
└──────────────────────┘
```

> expensesとincomesは直接のリレーションを持たない。  
> ダッシュボードでは同一の対象月（YYYY-MM）をキーに集計する。

---

## マイグレーション

Alembicで管理。初回は以下のコマンドで実行する。

```bash
python -m alembic upgrade head
```

マイグレーションファイルは `alembic/versions/` 以下に格納されている。
