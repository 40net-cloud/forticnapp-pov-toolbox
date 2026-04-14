# Terraform for integrating Azure Subscriptions and Tenants with FortiCnapp for cloud resource configuration assessment
provider "azurerm" {
  features {}
}


module "az_ad_application" {
  source  = "lacework/ad-application/azure"
  version = "~> 2.0"

  create                  = var.create_application

  application_name        = var.application_name
  application_owners      = var.application_owners

  enable_directory_reader = var.enable_directory_reader
}

module "az_activity_log" {
  source  = "lacework/activity-log/azure"
  version = "~> 3.0"

  ########################################
  # Lacework Integration
  ########################################
  lacework_integration_name = var.lacework_integration_name

  ########################################
  # Subscription Scope
  ########################################
  all_subscriptions       = var.all_subscriptions
  subscription_ids        = var.subscription_ids
  subscription_exclusions = var.subscription_exclusions

  ########################################
  # General Azure Settings
  ########################################
  prefix   = var.prefix
  tags = var.tags

  ########################################
  # Azure AD Application
  ########################################
  use_existing_ad_application = true
  application_id              = var.create_application ? module.az_ad_application.application_id : var.Provisioned_application_id
  application_name            = var.create_application ? var.application_name : var.Provisioned_application_name
  application_password        = var.create_application ? module.az_ad_application.application_password : var.Provisioned_application_password
  service_principal_id        = var.create_application ? module.az_ad_application.service_principal_id : var.Provisioned_service_principal_id

  ########################################
  # Storage Account
  ########################################
  use_existing_storage_account          = var.use_existing_storage_account
  location                              = var.location
  storage_account_name                  = var.storage_account_name
  storage_account_resource_group        = var.storage_account_resource_group
  log_retention_days                    = var.log_retention_days
  infrastructure_encryption_enabled     = var.infrastructure_encryption_enabled

  ########################################
  # Storage Network Rules
  ########################################
  use_storage_account_network_rules              = var.use_storage_account_network_rules
  storage_account_network_rule_action            = var.storage_account_network_rule_action
  storage_account_network_rule_bypass            = var.storage_account_network_rule_bypass
  storage_account_network_rule_ip_rules          = var.storage_account_network_rule_ip_rules
  storage_account_network_rule_lacework_ip_rules = var.storage_account_network_rule_lacework_ip_rules
  storage_account_network_rule_subnet_ids        = var.storage_account_network_rule_subnet_ids

  ########################################
  # Networking (VNet / Subnet / Private Endpoint)
  ########################################
  use_existing_subnet                       = var.use_existing_subnet
  existing_subnet_id                        = var.existing_subnet_id
  subnet_address_prefixes                   = var.subnet_address_prefixes
  virtual_network_address_space             = var.virtual_network_address_space
  private_endpoint_network_policies_enabled = var.private_endpoint_network_policies_enabled

  ########################################
  # Diagnostic Settings
  ########################################
  use_existing_diagnostic_settings = var.use_existing_diagnostic_settings
  diagnostic_settings_name         = var.diagnostic_settings_name

  ########################################
  # Timing / Deployment Behavior
  ########################################
  wait_time = var.wait_time
}
