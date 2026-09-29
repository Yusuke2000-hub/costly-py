# インフラ構成書

## 概要

costly-py のインフラは AWS EC2 上に構築し、Terraform（IaC）で管理している。  
Terraform ファイルは `terraform/` ディレクトリに格納。

---

## AWS構成図

```
インターネット
      │
      ▼
┌─────────────────────────────────────────────┐
│  VPC（costly-py-vpc）                        │
│  CIDR: 10.0.0.0/16                          │
│                                              │
│  ┌─────────────────────────────────────────┐ │
│  │  パブリックサブネット                    │ │
│  │  （costly-py-public-subnet）             │ │
│  │                                          │ │
│  │  ┌──────────────────────────────────┐    │ │
│  │  │  EC2インスタンス                 │    │ │
│  │  │  costly-py-ec2                   │    │ │
│  │  │  Amazon Linux 2023 / t2.micro    │    │ │
│  │  │                                  │    │ │
│  │  │  ├── uvicorn（FastAPI）:8000     │    │ │
│  │  │  └── MySQL 8.4（localhost）      │    │ │
│  │  └──────────────────────────────────┘    │ │
│  │         ↑                                │ │
│  │  セキュリティグループ                     │ │
│  │  ・SSH（22）: 自分のIPのみ               │ │
│  │  ・HTTP（8000）: 全世界                  │ │
│  └─────────────────────────────────────────┘ │
│         ↑                                    │
│  インターネットゲートウェイ（costly-py-igw）  │
└─────────────────────────────────────────────┘
```

---

## Terraformリソース一覧

| リソース | 識別子 | 説明 |
|---|---|---|
| VPC | `aws_vpc.main` | アプリ専用VPC |
| サブネット | `aws_subnet.public` | パブリックサブネット（AP-Northeast-1） |
| インターネットGW | `aws_internet_gateway.main` | 外部接続用 |
| ルートテーブル | `aws_route_table.public` | デフォルトルート → IGW |
| セキュリティグループ | `aws_security_group.ec2` | SSH（自分IP）・8000（全世界）・アウトバウンド全許可 |
| EC2インスタンス | `aws_instance.main` | Amazon Linux 2023、t2.micro |

---

## EC2初期セットアップ（user_data）

Terraform の `user_data` で以下を自動実行する。

1. Python 3.12 / pip / git のインストール
2. FastAPI 関連パッケージのインストール（uvicorn, sqlalchemy, alembic, pymysql, pydantic）
3. MySQL 8.4 のインストール・起動・自動起動設定
4. MySQL の root パスワード変更
5. アプリ用データベース・ユーザーの作成と権限付与

---

## デプロイ手順

### インフラ構築

```bash
cd terraform/
terraform init
terraform plan
terraform apply
```

### インフラ削除

```bash
cd terraform/
terraform destroy
```

### アプリの起動・停止（EC2上）

```bash
./start.sh   # バックグラウンドでuvicornを起動
./stop.sh    # 停止
```

---

## 環境変数（.env）

| 変数名 | 説明 |
|---|---|
| `DB_URL` | SQLAlchemy接続文字列（例：`mysql+pymysql://user:pass@localhost/dbname`） |

`.env` は `.gitignore` で管理対象外。`.env.example` を参考に設定する。

---

## 注意事項

- `terraform.tfstate` はGit管理対象外（`.gitignore`）
- Terraformのvariablesにはパスワード類が含まれるため、`terraform.tfvars` もGit管理対象外
- セキュリティグループのSSH許可IPは `var.my_ip` で管理（`terraform.tfvars` に設定）
