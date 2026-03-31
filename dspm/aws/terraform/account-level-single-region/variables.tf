variable "scanning_account_id" {
  description = "AWS Account ID where the DSPM scanner will be deployed"
  type        = string
  validation {
    condition     = length(var.scanning_account_id) > 0
    error_message = "scanning_account_id must be a non-empty string."
  }
}

variable "regions" {
  type        = list(string)
  description = "List of AWS regions where DSPM scanners are deployed."
  validation {
    condition     = length(var.regions) > 0
    error_message = "At least one region must be specified."
  }
}

variable "global_region" {
  type        = string
  default     = ""
  description = "Region for global resources (S3 bucket, etc). Defaults to first region in var.regions."
}

variable "lacework_integration_name" {
  description = "Name of the DSPM integration in FortiCNAPP"
  type        = string
  default     = "aws-dspm"
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default = {
    ManagedBy = "terraform"
  }
}

variable "resource_prefix" {
  description = "Prefix for resource names (also used for S3 bucket name with account ID appended for uniqueness)"
  type        = string
  default     = "forticnapp-dspm"
}

variable "lacework_hostname" {
  description = "Hostname for the Lacework account (e.g., my-tenant.lacework.net). If not provided, will use the URL associated with the default Lacework CLI profile."
  type        = string
  default     = ""
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

variable "ecs_task_cpu" {
  description = "CPU units for ECS task (256, 512, 1024, 2048, 4096)"
  type        = number
  default     = 1024
}

variable "ecs_task_memory" {
  description = "Memory for ECS task in MB (512, 1024, 2048, 4096, 8192, etc.)"
  type        = number
  default     = 2048
}

variable "scanner_image" {
  description = "Docker image for the DSPM scanner"
  type        = string
  default     = "lacework/dspm-scanner:latest"
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

variable "additional_trusted_role_arns" {
  type        = list(string)
  default     = []
  description = "Additional IAM role ARNs allowed to assume the DSPM scan role (e.g., for testing outside of the scheduled ECS task)."
}


variable "additional_environment_variables" {
  type = list(object({
    name  = string
    value = string
  }))
  default     = []
  description = "Optional list of additional environment variables passed to the scanner task."
}

variable "lacework_domain" {
  description = "Lacework domain for API server"
  type        = string
  default     = "lacework.net"
}

variable "lacework_aws_account_id" {
  type        = string
  default     = "434813966438"
  description = "The Lacework AWS account that the IAM role will grant access."
}