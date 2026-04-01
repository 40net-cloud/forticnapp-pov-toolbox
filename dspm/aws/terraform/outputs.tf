output "output_bucket_name" {
  description = "Name of the S3 output bucket (for scan results)"
  value       = module.lacework_dspm.output_bucket_name
}

output "output_bucket_arn" {
  description = "ARN of the S3 output bucket"
  value       = module.lacework_dspm.output_bucket_arn
}

output "ecs_cluster_names" {
  description = "Map of region to ECS cluster name"
  value       = module.lacework_dspm.ecs_cluster_names
}

output "ecs_cluster_arns" {
  description = "Map of region to ECS cluster ARN"
  value       = module.lacework_dspm.ecs_cluster_arns
}

output "ecs_task_definition_arns" {
  description = "Map of region to ECS task definition ARN"
  value       = module.lacework_dspm.ecs_task_definition_arns
}

output "vpc_ids" {
  description = "Map of region to VPC ID"
  value       = module.lacework_dspm.vpc_ids
}

output "eventbridge_rule_names" {
  description = "Map of region to EventBridge rule name"
  value       = module.lacework_dspm.eventbridge_rule_names
}

output "eventbridge_schedule" {
  description = "EventBridge schedule expression"
  value       = module.lacework_dspm.eventbridge_schedule
}

output "dspm_scan_role_arns" {
  description = "Map of region to IAM role ARN that the scanner assumes for S3 access"
  value       = module.lacework_dspm.dspm_scan_role_arns
}

output "ecs_task_role_arns" {
  description = "Map of region to ECS task role ARN"
  value       = module.lacework_dspm.ecs_task_role_arns
}

output "scanning_account_id" {
  description = "AWS Account ID being scanned"
  value       = module.lacework_dspm.scanning_account_id
}

output "security_group_ids" {
  description = "Map of region to security group ID for ECS tasks"
  value       = module.lacework_dspm.security_group_ids
}

output "subnet_ids" {
  description = "Map of region to list of public subnet IDs"
  value       = module.lacework_dspm.subnet_ids
}

output "dynamodb_table_names" {
  description = "Map of region to DynamoDB table name"
  value       = module.lacework_dspm.dynamodb_table_names
}

output "lacework_integration_id" {
  description = "ID of the FortiCNAPP DSPM integration"
  value       = module.lacework_dspm.lacework_integration_id
}

output "secret_arns" {
  description = "Map of region to DSPM scan secret ARN"
  value       = module.lacework_dspm.secret_arns
}

output "lacework_hostname" {
  description = "Lacework hostname for the integration (e.g., my-tenant.lacework.net)"
  value       = module.lacework_dspm.lacework_hostname
}