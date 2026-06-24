########################################
# OCI Provider
########################################

########################################
# OCI Provider
########################################
# Use EITHER config-file auth (config_file_profile) OR direct API-key auth
# (oci_user_ocid + oci_fingerprint + oci_private_key_path). For direct auth,
# set config_file_profile = "".

variable "config_file_profile" {
  type        = string
  default     = "DEFAULT"
  description = "Profile in ~/.oci/config to authenticate with. Set to \"\" when using direct API-key auth"
}

variable "oci_user_ocid" {
  type        = string
  default     = ""
  description = "Direct auth: OCID of the user running this Terraform"
}

variable "oci_fingerprint" {
  type        = string
  default     = ""
  description = "Direct auth: fingerprint of the API signing key for the user above"
}

variable "oci_private_key_path" {
  type        = string
  default     = ""
  description = "Direct auth: path to the matching PEM private key (use forward slashes on Windows)"
}

variable "region" {
  type        = string
  description = "OCI region for the provider. Use your tenancy HOME region for IAM writes (e.g. eu-amsterdam-1)"
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
# FortiCNAPP / Lacework Provider
########################################
# Leave any value empty ("") to fall back to ~/.lacework.toml or LW_* env vars.

variable "lw_profile" {
  type        = string
  default     = ""
  description = "Profile name in ~/.lacework.toml to use"
}

variable "lw_account" {
  type        = string
  default     = ""
  description = "FortiCNAPP account subdomain (the ACME in https://ACME.lacework.net)"
}

variable "lw_subaccount" {
  type        = string
  default     = ""
  description = "FortiCNAPP sub-account name (organizations only)"
}

variable "lw_api_key" {
  type        = string
  default     = ""
  sensitive   = true
  description = "FortiCNAPP API key. Prefer the env var TF_VAR_lw_api_key over committing this"
}

variable "lw_api_secret" {
  type        = string
  default     = ""
  sensitive   = true
  description = "FortiCNAPP API secret. Prefer the env var TF_VAR_lw_api_secret over committing this"
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
