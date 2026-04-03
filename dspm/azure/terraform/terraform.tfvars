############################################################################################################################################
# Required Variables to Integrate DSPM with your Azure Account #
############################################################################################################################################

# List of Azure regions where DSPM scanners are deployed
regions = [""]

############################################################################################################################################
# Optionals Variables to Integrate DSPM with your Azure Account  #
############################################################################################################################################

# SubcriptionId where FortiCNAPP DSPM is deployed. Leave blank to use the current one used by Azure Resource Manager. Show it through `az account show`
scanning_subscription_id  = ""

# Azure TenantId where DSPM is deployed
tenant_id= ""

# If we are integrating into a subscription or tenant. Valid values are 'SUBSCRIPTION' or 'TENANT'
integration_level = "SUBSCRIPTION"

# Region for global (shared) resources. Defaults to the first region in var.regions.
global_region = ""

# Name suffix for the Azure resource group that will contain all DSPM resources
rg_name = "dspm-rg"

# Prefix for resources
resource_prefix = "forticnapp"

# Owner for service account created. Azure recommends having one
owner_id = ""

# The name of the Lacework cloud account integration
lacework_integration_name = "azure-dspm"

# Set of tags which will be added to the resources managed by the module
tags = {
  ManagedBy   = "terraform"
}

# Scan settings:
# How often the DSPM scanner runs, in hours. Valid values: 24 (1 day), 72 (3 days), 168 (7 days), 720 (30 days).
scan_frequency_hours = null
# Maximum file size to scan, in megabytes. Valid values: 1 to 50.
max_file_size_mb     = null
# Docker image for the DSPM scanner
scanner_image = "lacework/dspm-scanner:latest"


# Datastore filtering configuration
datastore_filters = null 

# Optional list of additional environment variables passed to the task.
additional_environment_variables = []

# Hostname for the Lacework account (e.g., my-tenant.lacework.net). If not provided, will use the URL associated with the default Lacework CLI profile.
lacework_hostname = ""
