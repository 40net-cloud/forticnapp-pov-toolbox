# See: https://registry.terraform.io/providers/lacework/lacework/latest/docs

module "lacework_dspm" {
  source = "lacework/dspm/aws"
  version = "~> 0.3.0"

 # Required Variables
  scanning_account_id               = var.scanning_account_id
  regions                           = var.regions

  # Optional Variables
  global_region                     = var.global_region
  resource_prefix                   = var.resource_prefix
  tags                              = var.tags
  manage_s3_public_access_block     = var.manage_s3_public_access_block

  lacework_integration_name         = var.lacework_integration_name
  lacework_hostname                 = var.lacework_hostname
  lacework_domain                   = var.lacework_domain

  scan_frequency_hours              = var.scan_frequency_hours
  max_file_size_mb                  = var.max_file_size_mb
  scanner_image                     = var.scanner_image

  ecs_task_cpu                      = var.ecs_task_cpu
  ecs_task_memory                   = var.ecs_task_memory

  datastore_filters                 = var.datastore_filters
  additional_trusted_role_arns      = var.additional_trusted_role_arns
  additional_environment_variables  = var.additional_environment_variables


  
}