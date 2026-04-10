variable "create_application" {
  type        = bool
  default     = true
  description = "Set to `false` to prevent the module from creating any resources"
}

variable "application_name" {
  type        = string
  default     = "lacework_security_audit"
  description = "The name of the Azure Active Directory Application"
}

variable "application_owners" {
  type = list(string)
  default = []
  description = "The owners of the Azure Active Directory Application. If empty, current user will be owner"
}

variable "enable_directory_reader" {
  type = bool
  default = true
  description = "Enable Directory Reader role for this principal. This will allow Lacework to read Users/Groups/Principals from MS Graph API"
}

#####################################################################

variable "all_subscriptions" {
  type        = bool
  default     = false
  description = "If set to true, grant read access to ALL subscriptions within the selected Tenant (overrides 'subscription_ids')"
}
variable "Provisioned_application_id" {
  type        = string
  default     = ""
  description = "The Active Directory Application id to use (required when creat_application is set to false)"
}
variable "Provisioned_application_name" {
  type        = string
  default     = "lacework_security_audit"
  description = "The name of the Azure Active Directory Application (required when creat_application is set to false) "
}
variable "Provisioned_application_password" {
  type        = string
  default     = ""
  description = "The Active Directory Application password to use (required when creat_application is set to false) "
}
variable "lacework_integration_name" {
  type        = string
  default     = "TF config"
  description = "The Lacework integration name"
}
variable "management_group_id" {
  type        = string
  default     = ""
  description = "The Management Group ID to add Reader permissions (required when use_management_group is true)"
}
variable "Provisioned_service_principal_id" {
  type        = string
  default     = ""
  description = "The Enterprise App Object ID related to the application_id (required when creat_application is set to false)"
}
variable "subscription_exclusions" {
  type        = list(string)
  description = "List of subscriptions to exclude when using the `all_subscriptions` option."
  default     = []
}
variable "subscription_ids" {
  type        = list(string)
  description = "List of subscriptions to grant read access to, by default the module will only use the primary subscription"
  default     = []
}
variable "use_existing_ad_application" {
  type        = bool
  default     = true
  description = "Set this to `true` to created Application from az_ad_application module or to use Provisioned Active Directory Application (don't change it)"
}
variable "use_management_group" {
  type        = bool
  default     = false
  description = "If set to `true`, the AD Application will be a Reader on the Management Group level instead of Subscription level"
}
variable "wait_time" {
  type        = string
  default     = "20s"
  description = "Amount of time to wait before the Lacework resources are provisioned"
}