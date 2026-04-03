output "storage_account_name" {
  description = "The blob storage account for DSPM data"
  value       = module.lacework_azure_dspm.storage_account_name
}

output "dspm_client_id" {
  description = "Client ID of the scanner's managed identity"
  value       = module.lacework_azure_dspm.dspm_client_id
}

output "dspm_principal_id" {
  description = "Principal ID (GUID) of the scanner's managed identity"
  value       = module.lacework_azure_dspm.dspm_principal_id
}

output "dspm_identity_id" {
  description = "Fully qualified resource ID of the scanner's managed identity"
  value       = module.lacework_azure_dspm.dspm_identity_id
}

output "resource_group_name" {
  description = "Name of the resource group hosting the DSPM scanner"
  value       = module.lacework_azure_dspm.resource_group_name
}

output "resource_group_id" {
  description = "ID of the resource group hosting the DSPM scanner"
  value       = module.lacework_azure_dspm.resource_group_id
}

output "suffix" {
  description = "Suffix used to add uniqueness to resource names"
  value       = module.lacework_azure_dspm.suffix
}

output "scanning_subscription_id" {
  description = "The subscription where scanning resources are deployed"
  value       = module.lacework_azure_dspm.scanning_subscription_id
}

output "lacework_hostname" {
  description = "Lacework hostname for the integration (e.g., my-tenant.lacework.net)"
  value       = module.lacework_azure_dspm.lacework_hostname
}

output "lacework_integration_name" {
  description = "The name of the integration"
  value       = module.lacework_azure_dspm.lacework_integration_name
}

output "lacework_integration_id" {
  description = "The ID of the Lacework integration"
  value       = module.lacework_azure_dspm.lacework_integration_id
}

output "key_vault_uri" {
  description = "The URI of the Key Vault storing DSPM secrets"
  value       = module.lacework_azure_dspm.key_vault_uri
}

output "key_vault_secret_name" {
  description = "The name of the secret in Key Vault containing Lacework credentials"
  value       = module.lacework_azure_dspm.key_vault_secret_name
}

output "key_vault_id" {
  description = "The ID of the Key Vault storing DSPM secrets"
  value       = module.lacework_azure_dspm.key_vault_id
}

output "dspm_identity_resource_id" {
  description = "The resource ID of the DSPM identity"
  value       = module.lacework_azure_dspm.dspm_identity_resource_id
}

output "scanner_job_ids" {
  description = "Map of region to scanner job ID"
  value       = module.lacework_azure_dspm.scanner_job_ids
}