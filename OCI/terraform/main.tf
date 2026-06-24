# Terraform for integrating an OCI Tenancy with FortiCNAPP for cloud resource configuration assessment (CSPM)

provider "oci" {

  # Config-file auth: set config_file_profile, leave the direct fields empty.
  config_file_profile = var.config_file_profile != "" ? var.config_file_profile : null

  # Direct API-key auth: set the fields below, and set config_file_profile = "".
  # tenancy_ocid reuses var.tenancy_id (the tenancy being integrated).
  tenancy_ocid         = var.tenancy_id
  user_ocid            = var.oci_user_ocid != "" ? var.oci_user_ocid : null
  fingerprint          = var.oci_fingerprint != "" ? var.oci_fingerprint : null
  private_key_path     = var.oci_private_key_path != "" ? var.oci_private_key_path : null

  region = var.region
}

# The Lacework/FortiCNAPP provider. Any value left empty falls back to
# ~/.lacework.toml (the selected profile) or LW_* environment variables.
provider "lacework" {
  profile    = var.lw_profile
  account    = var.lw_account
  subaccount = var.lw_subaccount
  api_key    = var.lw_api_key
  api_secret = var.lw_api_secret
}

module "oci_config" {
  source  = "lacework/config/oci"
  version = "~> 0.3"

  # Required
  tenancy_id = var.tenancy_id
  user_email = var.user_email

  # Lacework / FortiCNAPP integration label
  integration_name = var.integration_name

  # Resource naming (name_prefix is used unless an explicit name is given)
  name_prefix = var.name_prefix
  user_name   = var.user_name
  group_name  = var.group_name
  policy_name = var.policy_name

  # Tagging + behavior
  freeform_tags = var.freeform_tags
  create        = var.create
  wait_time     = var.wait_time
}
