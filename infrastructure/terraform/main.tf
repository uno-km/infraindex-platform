terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC Configuration
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = {
    Name = "infraindex-vpc-${var.environment}"
  }
}

# ECS Cluster for API and Worker
resource "aws_ecs_cluster" "main" {
  name = "infraindex-cluster-${var.environment}"
}

# RDS PostgreSQL Instance
resource "aws_db_instance" "postgres" {
  identifier        = "infraindex-db-${var.environment}"
  engine            = "postgres"
  engine_version    = "16"
  instance_class    = "db.t4g.micro"
  allocated_storage = 20
  db_name           = "infraindex"
  username          = var.db_username
  password          = var.db_password
  
  skip_final_snapshot = true
}

# ElastiCache Redis
resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "infraindex-redis-${var.environment}"
  engine               = "redis"
  node_type            = "cache.t4g.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379
}
