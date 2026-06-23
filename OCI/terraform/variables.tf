########################################
# OCI Provider
########################################

variable "user_ocid" {
  type        = string
  description = "OCID of the OCI user used to authenticate the provider (the admin running this Terraform)"
}

variable "fingerprint" {
  type        = string
  description = "Fingerprint of the API signing key uploaded to the OCI user above"
}

variable "private_key_path" {
  type        = string
  description = "Path to the PEM private key matching the fingerprint (e.g. C:/Users/.oci/oci_api_key.pem)"
}

variable "region" {
  type        = string
  description = "OCI region to operate in (e.g. eu-frankfurt-1)"
}

########################################
# Required
########################################

variable "tenancy_id" {
  type        = string
  description = "OCID of the OCI tenancy to be integrated with FortiCNAPP"
}

variable "user_email" {
  type        = string
  description = "Email associated with the IAM user created for the integration"
}

########################################
# FortiCNAPP Integration
########################################

variable "integration_name" {
  type        = string
  default     = "OCI CSPM Integration"
  description = "Label for the OCI integration as shown within the FortiCNAPP platform"
}

########################################
# Resource Naming
########################################

variable "name_prefix" {
  type        = string
  default     = "lw_cspm"
  description = "The OCI resources will be named $${name_prefix}_{user,group,policy}"
}

variable "user_name" {
  type        = string
  default     = ""
  description = "Name of the IAM user used for the integration (overrides name_prefix)"
}

variable "group_name" {
  type        = string
  default     = ""
  description = "Name of the IAM group for the integration user (overrides name_prefix)"
}

variable "policy_name" {
  type        = string
  default     = ""
  description = "Name of the policy that governs the integration user's permissions (overrides name_prefix)"
}

########################################
# Tagging / Deployment Behavior
########################################

variable "freeform_tags" {
  type        = map(any)
  default     = {}
  description = "Freeform tags applied to the resources created for the CSPM integration"
}

variable "create" {
  type        = bool
  default     = true
  description = "Set to false to prevent the module from creating any resources"
}

variable "wait_time" {
  type        = string
  default     = "10s"
  description = "Amount of time to wait before the next resource is provisioned"
}
