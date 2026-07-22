output "db_endpoint" {
  description = "Connection endpoint for the PostgreSQL database"
  value       = aws_db_instance.postgres.endpoint
}

output "redis_endpoint" {
  description = "Connection endpoint for the Redis cache"
  value       = aws_elasticache_cluster.redis.cache_nodes[0].address
}
