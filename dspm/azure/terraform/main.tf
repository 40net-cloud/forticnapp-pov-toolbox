provider "lacework" {
  profile = "default"
}

module "lacework_azure_dspm" {
  source                    = "lacework/dspm/azure"

  regions                   = var.regions

  scanning_subscription_id  = var.scanning_subscription_id
  tenant_id                 = var.tenant_id
  integration_level         = var.integration_level
  global_region             = var.global_region
  rg_name                   = var.rg_name
  resource_prefix           = var.resource_prefix
  owner_id                  = var.owner_id
  lacework_integration_name = var.lacework_integration_name
  tags                      = var.tags

  scan_frequency_hours      = var.scan_frequency_hours
  max_file_size_mb          = var.max_file_size_mb
  scanner_image             = var.scanner_image

  datastore_filters         = var.datastore_filters

  additional_environment_variables = var.additional_environment_variables

  lacework_hostname = var.lacework_hostname
}