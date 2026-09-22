output "vpc_id" {
  description = "VPCのID"
  value       = aws_vpc.main.id
}

output "public_subnet_id" {
  description = "パブリックサブネットのID"
  value       = aws_subnet.public.id
}

output "ec2_instance_id" {
  description = "EC2インスタンスのID"
  value       = aws_instance.main.id
}

output "ec2_public_ip" {
  description = "EC2インスタンスのパブリックIP"
  value       = aws_instance.main.public_ip
}

output "fastapi_url" {
  description = "FastAPI エンドポイント"
  value       = "http://${aws_instance.main.public_ip}:8000"
}

output "ssh_command" {
  description = "SSH接続コマンド"
  value       = "ssh -i ~/.ssh/${var.key_name}.pem ec2-user@${aws_instance.main.public_ip}"
}
