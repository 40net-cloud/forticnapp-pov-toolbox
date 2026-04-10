output "created_application" {
  value       = var.create_application
  description = "Was the Active Directory Application created"
}

output "enable_directory_reader" {
  value       = var.enable_directory_reader
  description = "Was the Active Directory Application granted Directory Reader role in Azure AD?"
}

output "application_password" {
  value       = var.create_application ? module.az_ad_application.application_password : var.Provisioned_application_password
  description = "The Lacework AD Application password"
  sensitive   = true
}

output "application_id" {
  value       = var.create_application ? module.az_ad_application.application_id : var.Provisioned_application_id
  description = "The Lacework AD Client id"
}

output "service_principal_id" {
  value       = var.create_application ? module.az_ad_application.service_principal_id : var.Provisioned_service_principal_id
  description = "The Lacework Service Principal id"
}