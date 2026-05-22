variable "create_application" {
  type        = bool
  default     = true
  description = "Set to `false` to prevent the module from creating any resources"
}

variable "application_name" {
  type        = string
  description = "The name of the Azure Active Directory Application."
}

variable "application_owners" {
  type = list(string)
  default = []
  description = "The owners of the Azure Active Directory Application. If empty, current user will be owner"
}

variable "enable_directory_reader" {
  type = bool
  description = "CIEM integration 'true' . Enable Directory Reader role for this principal. This will allow Lacework to read Users/Groups/Principals from MS Graph API. **Azure Global Administrator is required**"
}

#####################################################################

variable "lacework_integration_name" {
  type        = string
  description = "The Lacework integration name. This can be seen from FortiCNAPP UI. Go to Settings > Integrations > Cloud accounts."
}

variable "all_subscriptions" {
  type        = bool
  description = "True: grant read access to ALL subscriptions within the selected Tenant (overrides 'subscription_ids'). False (default): grant read access to specific subscription(s) "
}

variable "subscription_ids" {
  type        = list(string)
  description = "List of subscriptions to grant read access to, by default the module will only use the primary subscription ex:[\"subscription-id-1\", \"subscription-id-2\", \"subscription-id-3\"]"
  validation {
    condition     = var.all_subscriptions == false || length(var.subscription_ids) == 0
    error_message = "Do not set 'subscription_ids' when 'all_subscriptions' is true."
  }
  validation {
    condition = alltrue([
      for id in var.subscription_ids :
      can(regex("^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$", id))
    ])
    error_message = "Each subscription_id must be a valid Azure subscription GUID (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)."
  }
}

variable "subscription_exclusions" {
  type        = list(string)
  description = "List of subscriptions to exclude when using the `all_subscriptions` option . Default = [] "
  validation {
    condition     = var.all_subscriptions == true || length(var.subscription_exclusions) == 0
    error_message = "subscription_exclusions can only be used when all_subscriptions is true."
  }
  validation {
    condition = alltrue([
      for id in var.subscription_exclusions :
      can(regex("^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$", id))
    ])
    error_message = "Each subscription_id must be a valid Azure subscription GUID (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)."
  }
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