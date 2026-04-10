# Terraform for integrating Azure Subscriptions and Tenants with FortiCnapp for cloud resource configuration assessment
provider "azurerm" {
  features {}
}


module "az_ad_application" {
  source  = "lacework/ad-application/azure"
  version = "~> 2.0"

  application_name        = var.application_name
  application_owners      = var.application_owners
  enable_directory_reader = var.enable_directory_reader
  create                  = var.create_application
}

module "az_config" {
  source                      = "lacework/config/azure"
  version                     = "~> 3.0"
  
  lacework_integration_name   = var.lacework_integration_name

  subscription_ids            = var.subscription_ids

  all_subscriptions           = var.all_subscriptions
  subscription_exclusions     = var.subscription_exclusions

  use_existing_ad_application = true
  application_id              = var.create_application ? module.az_ad_application.application_id : var.Provisioned_application_id
  application_name            = var.create_application ? var.application_name : var.Provisioned_application_name
  application_password        = var.create_application ? module.az_ad_application.application_password : var.Provisioned_application_password
  service_principal_id        = var.create_application ? module.az_ad_application.service_principal_id : var.Provisioned_service_principal_id
  
  use_management_group        = var.use_management_group
  management_group_id         = var.management_group_id

  wait_time                   = var.wait_time
}
