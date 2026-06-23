# Terraform for integrating an OCI Tenancy with FortiCNAPP for cloud resource configuration assessment (CSPM)

provider "oci" {
  # Direct API-key authentication (no ~/.oci/config file required).
  # All values are supplied via terraform.tfvars.
  tenancy_ocid     = var.tenancy_id
  user_ocid        = var.user_ocid
  fingerprint      = var.fingerprint
  private_key_path = var.private_key_path
  region           = var.region
}

# The Lacework/FortiCNAPP provider reads credentials from ~/.lacework.toml

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
