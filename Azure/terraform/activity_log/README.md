:wave: [Overview](#overview) • [Requirments](#requirments) • [Instructions](#instructions) 

# Terraform for Integrating Azure Activity Logs with FortiCNAPP

## Overview 

### What Does the Activity Log Provide? 

Microsoft Azure Activity Log provides visibility into all operations within your Azure environment, helping you track and audit changes across your subscription.

FortiCNAPP uses these logs to:

- Detect resource changes (create, update, delete)
- Generate cloud activity insights (Polygraph)
- Establish normal behavior baselines
- Identify anomalies and potential threats

This enables continuous monitoring and improved security across your cloud workloads. 

For more details, see the [Azure Activity Log Integration – Configuration Workflow](https://github.com/40net-cloud/forticnapp-pov-toolbox/blob/main/Azure/CLOUD%20(CSPM%2C%20CIEM%2C%20UEBA)/cloud-api.md#-azure-activity-log-integration--configuration-workflow).

### What Does Terraform Create in Azure?

- Azure AD / Entra application with client secret and Service principal (creat_application is set to true) or use an existing one (creat_application is set to false).
- Create and assign the following roles to service principal:
   - Dirctory readers role (only with creat_application is set to true) :Read-only access to Entra ID (users, groups, apps, metadata). If enable_directory_reader = false , LQL datasources and related IAM compliance policies will not be assessed. By default, this setting is true.
   - Custom Azure role definition with permissions to read the storage account, queue, event subscription, list storage keys, read blobs, read queue messages, and delete queue messages
- Storage Queue for notifications about new log files
- Event Grid on the storage account that sends blob-created events into that queue
- Private Endpoint for the storage account

Creates only if you are not reusing existing storage account (use_existing_storage_account = false)

- Resource Group
- Storage Account (StorageV2, Standard, LRS, TLS 1.2, HTTPS only, nested public access disabled)

Creates only if you enable storage network restrictions (use_storage_account_network_rules = true)

- Storage account network rules

Creates only if you are not reusing existing subnet (use_existing_subnet = false)

- Virtual Network
- Subnet with Microsoft.Storage service endpoint

Creates only if you don't use existing Diagnostic Settings (use_existing_diagnostic_settings = false)
- Diagnostic Settings on one or more subscriptions to export Azure Activity Log categories to the storage account: Administrative, Security, Alert, Policy, and ResourceHealth

## Requirments

The following is a list of requirements to run FortiCNAPP Terraform modules for Azure:

- Azure Owner Role - An Azure portal account with the Owner role in all subscriptions that you want to monitor.
- Azure CLI - The Terraform provider for Azure leverages configuration from the Azure CLI to configure resources in Azure.
- FortiCNAPP Administrator - A FortiCNAPP account with administrator privileges.
- Terraform - >= 0.14
- Ensure that you are deploying the integration to a supported Azure region.

## Instructions

Follow these steps to deploy:

1. Copy all Terraform configuration files into your working directory. Then, rename the file `terraform.tfvars.txt` to `terraform.tfvars`. 
   The terraform.tfvars file contains all configurable input variables for the deployment. Each variable is already populated with a default value, so modifying them is optional. Update these values only if you need to customize the deployment for your environment. 
2. Terraform code will integrate the primary azure subscription (You can verify it with command line: az account show). You can change that behavior with subscription scope variables.
3. (Optional) If you plan to use an existing application, set create_application to false and provide values for all variables related to Your Provisioned Application.
4. (Optional) Customize your deployment: Default values are provided for all variables, but you may want to customize some of them:
    - lacework_integration_name
    - application name and owner (creat_application to true)
    - Prefix for created resources
    - Tags
    - Storage account variables (location, name,..)
    - Storage Network Rules variables (only when use_storage_account_network_rules = true)
    - Networking variables
    - Diagnostic Settings variables

5. Run the following commands:
<code><pre>
   terraform init
   terraform plan
   terraform apply
</code></pre>

You can delete the integration and remove all created resources using the following command:
<code><pre>
   terraform destroy
</code></pre>