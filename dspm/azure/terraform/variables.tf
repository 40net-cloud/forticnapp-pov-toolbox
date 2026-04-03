variable "lacework_hostname" {
  description = "Hostname for the Lacework account (e.g., my-tenant.lacework.net). If not provided, will use the URL associated with the default Lacework CLI profile."
  type        = string
  default     = ""
}

variable "lacework_integration_name" {
  type        = string
  description = "The name of the Lacework cloud account integration."
  default     = "azure-dspm"
}

variable "rg_name" {
  type        = string
  default     = "dspm-rg"
  description = "Name suffix for the Azure resource group that will contain all DSPM resources."
}

variable "resource_prefix" {
  type        = string
  description = "Prefix for resource names."
  // Azure's default is shorter than AWS's ("forticnapp" vs "forticnapp-dspm") to stay within Azure's resource name character limits.
  default = "forticnapp"

  validation {
    condition     = length(var.resource_prefix) <= 20
    error_message = "resource_prefix must not exceed 20 characters to stay within Azure resource name limits."
  }
}

variable "tags" {
  type = map(string)
  default = {
    ManagedBy = "terraform"
  }
  description = "Set of tags which will be added to the resources managed by the module."
}

variable "scanner_image" {
  type        = string
  default     = "lacework/dspm-scanner:latest"
  description = "Docker image for the DSPM scanner"
}

variable "regions" {
  type        = list(string)
  description = "List of Azure regions where DSPM scanners are deployed."
  validation {
    condition     = length(var.regions) > 0
    error_message = "At least one region must be specified."
  }
}

variable "global_region" {
  type        = string
  default     = ""
  description = "Region for global (shared) resources. Defaults to the first region in var.regions."
  validation {
    condition     = var.global_region == "" || contains(var.regions, var.global_region)
    error_message = "global_region must be one of the values in var.regions."
  }
}

variable "additional_environment_variables" {
  type = list(object({
    name  = string
    value = string
  }))
  default     = []
  description = "Optional list of additional environment variables passed to the task."
}

variable "tenant_id" {
  type        = string
  default     = ""
  description = "TenantId where DSPM is deployed"
}

variable "scanning_subscription_id" {
  type        = string
  default     = ""
  description = "SubcriptionId where FortiCNAPP DSPM is deployed. Leave blank to use the current one used by Azure Resource Manager. Show it through `az account show`"
}

variable "owner_id" {
  type        = string
  default     = ""
  description = "Owner for service account created. Azure recommends having one"
  validation {
    condition     = can(regex("^[a-z0-9-]*$", var.owner_id))
    error_message = "Owner id needs to be of format xxxx-xxxx-xxxx-xxxx-xxxxx."
  }
}

variable "scan_frequency_hours" {
  type        = number
  default     = null
  description = "How often the DSPM scanner runs, in hours. Valid values: 24 (1 day), 72 (3 days), 168 (7 days), 720 (30 days)."

  validation {
    condition     = try(contains([24, 72, 168, 720], var.scan_frequency_hours), var.scan_frequency_hours == null)
    error_message = "scan_frequency_hours must be one of: 24 (1 day), 72 (3 days), 168 (7 days), 720 (30 days)."
  }
}

variable "max_file_size_mb" {
  type        = number
  default     = null
  description = "Maximum file size to scan, in megabytes. Valid values: 1 to 50."

  validation {
    condition     = try(var.max_file_size_mb >= 1 && var.max_file_size_mb <= 50, var.max_file_size_mb == null)
    error_message = "max_file_size_mb must be between 1 and 50."
  }
}

variable "datastore_filters" {
  type = object({
    filter_mode     = string
    datastore_names = optional(list(string), [])
  })
  default     = null
  description = "Filter which datastores are scanned. filter_mode must be 'INCLUDE', 'EXCLUDE', or 'ALL'. datastore_names is required for INCLUDE/EXCLUDE and must not be set for ALL."

  validation {
    condition     = try(contains(["INCLUDE", "EXCLUDE", "ALL"], var.datastore_filters.filter_mode), var.datastore_filters == null)
    error_message = "filter_mode must be one of: INCLUDE, EXCLUDE, ALL."
  }

  validation {
    condition = try(
      var.datastore_filters.filter_mode == "ALL"
      ? length(var.datastore_filters.datastore_names) == 0
      : length(var.datastore_filters.datastore_names) > 0,
      var.datastore_filters == null
    )
    error_message = "datastore_names must not be set when filter_mode is 'ALL', and must contain at least one entry when filter_mode is 'INCLUDE' or 'EXCLUDE'."
  }
}

variable "integration_level" {
  type        = string
  description = "If we are integrating into a subscription or tenant. Valid values are 'SUBSCRIPTION' or 'TENANT'"
  default     = "SUBSCRIPTION"
  validation {
    condition     = upper(var.integration_level) == "SUBSCRIPTION" || upper(var.integration_level) == "TENANT"
    error_message = "Valid values are 'SUBSCRIPTION' or 'TENANT'."
  }
}