variable "registry_domain" {
  type        = string
  default     = ""
  description = "The registry domain to configure"
}

variable "use_existing_iam_role" {
  type        = bool
  default     = false
  description = "Set this to true to use an existing IAM role"
}

variable "iam_role_arn" {
  type        = string
  default     = ""
  description = "The IAM role ARN. required when setting use_existing_iam_role to true"
}

variable "iam_role_external_id" {
  type        = string
  default     = ""
  description = "The external ID configured inside the IAM role. required when setting use_existing_iam_role to true"
}

variable "iam_role_name" {
  type        = string
  default     = ""
  description = "The IAM role name. Required to match with iam_role_arn if use_existing_iam_role is set to true"
}

variable "limit_by_tags" {
  type        = list(string)
  default     = []
  description = "A list of tags to limit the assessment of images with matching tags. If you specify limit_by_tags and limit_by_label limits, they function as an AND."
}

variable "limit_by_labels" {
  type = list(object({
    key   = string
    value = string
  }))
  default     = []
  description = "A list of objects with image labels to limit the assessment of images with matching labels. If you specify limit_by_tags and limit_by_label limits, they function as an AND."
}

variable "limit_by_repositories" {
  type        = list(string)
  default     = []
  description = "A list of repositories to assess"
}

variable "limit_num_imgs" {
  type        = number
  default     = 5
  description = "The maximum number of newest container images to assess per repository. Must be one of 5, 10, or 15. Defaults to 5."
}

variable "lacework_aws_account_id" {
  type        = string
  default     = "434813966438"
  description = "The Lacework AWS account that the IAM role will grant access"
}

variable "tags" {
  type        = map(string)
  description = "A map/dictionary of Tags to be assigned to created resources"
  default     = {}
}

variable "wait_time" {
  type        = string
  default     = "15s"
  description = "Amount of time to wait before the next resource is provisioned"
}

variable "lacework_integration_name" {
  type        = string
  default     = "TF ECR IAM Role"
  description = "The name of the external ECR integration"
}

variable "non_os_package_support" {
  type        = bool
  default     = true
  description = "Whether or not the integration should check non-os packages in the container for vulnerabilities"
}
