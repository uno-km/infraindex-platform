variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-northeast-2"
}

variable "environment" {
  description = "Deployment environment (e.g. staging, prod)"
  type        = string
  default     = "staging"
}

variable "db_username" {
  description = "PostgreSQL root username"
  type        = string
  default     = "infraindex_admin"
}

variable "db_password" {
  description = "PostgreSQL root password"
  type        = string
  sensitive   = true
}
