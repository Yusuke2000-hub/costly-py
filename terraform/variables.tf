variable "aws_region" {
  description = "AWSリージョン"
  type        = string
  default     = "ap-northeast-1"
}

variable "project_name" {
  description = "プロジェクト名（リソース名のプレフィックスに使用）"
  type        = string
  default     = "costly-py"
}

variable "vpc_cidr" {
  description = "VPCのCIDRブロック"
  type        = string
  default     = "10.1.0.0/16"
}

variable "public_subnet_cidr" {
  description = "パブリックサブネットのCIDRブロック"
  type        = string
  default     = "10.1.1.0/24"
}

variable "availability_zone" {
  description = "アベイラビリティゾーン"
  type        = string
  default     = "ap-northeast-1a"
}

variable "my_ip" {
  description = "SSHアクセスを許可する自分のグローバルIP（CIDR形式）"
  type        = string
  default     = "133.32.224.255/32"
}

variable "key_name" {
  description = "EC2接続用のキーペア名"
  type        = string
  default     = "costly-py-key"
}

variable "instance_type" {
  description = "EC2インスタンスタイプ"
  type        = string
  default     = "t3.micro"
}
