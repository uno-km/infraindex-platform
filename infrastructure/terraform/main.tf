terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # P2-003: 원격 State 백엔드 (팀 협업 및 잠금 지원)
  # 로컬 개발 시 주석 처리 가능
  # backend "s3" {
  #   bucket         = "infraindex-terraform-state"
  #   key            = "infra/${var.environment}/terraform.tfstate"
  #   region         = "ap-northeast-2"
  #   dynamodb_table = "infraindex-terraform-locks"
  #   encrypt        = true
  # }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project     = "infraindex"
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

# ─────────────────────────────────────────
# VPC
# ─────────────────────────────────────────
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = {
    Name = "infraindex-vpc-${var.environment}"
  }
}

# P2-003: 프라이빗 서브넷 2개 (Multi-AZ) — RDS 필수 요건
resource "aws_subnet" "private_a" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "${var.aws_region}a"
  tags = {
    Name = "infraindex-private-a-${var.environment}"
    Tier = "private"
  }
}

resource "aws_subnet" "private_b" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "${var.aws_region}b"
  tags = {
    Name = "infraindex-private-b-${var.environment}"
    Tier = "private"
  }
}

# P2-003: RDS 서브넷 그룹 (Multi-AZ 위해 서브넷 2개 이상 필요)
resource "aws_db_subnet_group" "postgres" {
  name       = "infraindex-db-subnet-${var.environment}"
  subnet_ids = [aws_subnet.private_a.id, aws_subnet.private_b.id]
  tags = {
    Name = "infraindex-db-subnet-group-${var.environment}"
  }
}

# P2-003: RDS 전용 보안 그룹
resource "aws_security_group" "rds" {
  name        = "infraindex-rds-sg-${var.environment}"
  description = "Allow PostgreSQL access from ECS tasks only"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_tasks.id]
    description     = "PostgreSQL from ECS tasks"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "infraindex-rds-sg-${var.environment}"
  }
}

# ECS Tasks 보안 그룹
resource "aws_security_group" "ecs_tasks" {
  name        = "infraindex-ecs-sg-${var.environment}"
  description = "ECS tasks outbound access"
  vpc_id      = aws_vpc.main.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "infraindex-ecs-sg-${var.environment}"
  }
}

# ─────────────────────────────────────────
# ECS Cluster
# ─────────────────────────────────────────
resource "aws_ecs_cluster" "main" {
  name = "infraindex-cluster-${var.environment}"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# ─────────────────────────────────────────
# RDS PostgreSQL — P2-003 하드닝
# ─────────────────────────────────────────
resource "aws_db_instance" "postgres" {
  identifier        = "infraindex-db-${var.environment}"
  engine            = "postgres"
  engine_version    = "16"
  instance_class    = var.environment == "prod" ? "db.t4g.small" : "db.t4g.micro"
  allocated_storage = var.environment == "prod" ? 100 : 20
  max_allocated_storage = var.environment == "prod" ? 1000 : 100  # Auto Scaling
  db_name           = "infraindex"
  username          = var.db_username
  password          = var.db_password

  # P2-003: 서브넷 그룹 연결 (이전: 누락으로 public 배포)
  db_subnet_group_name   = aws_db_subnet_group.postgres.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  # P2-003: 퍼블릭 노출 차단
  publicly_accessible = false

  # P2-003: 암호화 활성화
  storage_encrypted = true
  # kms_key_id      = aws_kms_key.rds.arn  # 커스텀 KMS 사용 시 활성화

  # P2-003: 자동 백업 (7일 보관)
  backup_retention_period = 7
  backup_window           = "02:00-03:00"  # UTC 새벽 2~3시
  maintenance_window      = "Mon:03:00-Mon:04:00"

  # P2-003: 삭제 보호 활성화 (production accidental drop 방지)
  deletion_protection = var.environment == "prod" ? true : false
  skip_final_snapshot = var.environment == "prod" ? false : true
  final_snapshot_identifier = var.environment == "prod" ? "infraindex-db-final-${var.environment}" : null

  # P2-003: 성능 인사이트
  performance_insights_enabled          = var.environment == "prod" ? true : false
  performance_insights_retention_period = var.environment == "prod" ? 7 : null

  # P2-003: Enhanced Monitoring
  monitoring_interval = var.environment == "prod" ? 60 : 0
  monitoring_role_arn = var.environment == "prod" ? aws_iam_role.rds_monitoring[0].arn : null

  tags = {
    Name        = "infraindex-db-${var.environment}"
    Environment = var.environment
  }
}

# Enhanced Monitoring IAM Role (production only)
resource "aws_iam_role" "rds_monitoring" {
  count = var.environment == "prod" ? 1 : 0
  name  = "infraindex-rds-monitoring-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "monitoring.rds.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "rds_monitoring" {
  count      = var.environment == "prod" ? 1 : 0
  role       = aws_iam_role.rds_monitoring[0].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"
}

# ─────────────────────────────────────────
# ElastiCache Redis
# ─────────────────────────────────────────
resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "infraindex-redis-${var.environment}"
  engine               = "redis"
  node_type            = "cache.t4g.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379
  subnet_group_name    = aws_elasticache_subnet_group.redis.name
  security_group_ids   = [aws_security_group.ecs_tasks.id]
}

resource "aws_elasticache_subnet_group" "redis" {
  name       = "infraindex-redis-subnet-${var.environment}"
  subnet_ids = [aws_subnet.private_a.id, aws_subnet.private_b.id]
}

# ─────────────────────────────────────────
# Outputs
# ─────────────────────────────────────────
output "rds_endpoint" {
  value     = aws_db_instance.postgres.endpoint
  sensitive = true
}

output "redis_endpoint" {
  value = aws_elasticache_cluster.redis.cache_nodes[0].address
}
