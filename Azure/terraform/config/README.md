# Terraform for Integrating Azure Configurations with FortiCNAPP

## Overview

Terraform will create using default values:
- Application id with secret id.
- Service principal with assigned:
    - Dirctory readers role :Read-only access to Entra ID (users, groups, apps, metadata)
    - Key vault reader : View Key Vault metadata (no access to secrets or keys)
    - Reader role: View all Azure resources and configurations (no changes allowed)

Lacework can log in to Azure using client ID (app id) + secret + tenant ID (OAuth).
The App ID identifies the application and holds the secret, while the Service Principal is the actual identity in your tenant that logs in and gets permissions (ex: Directory Readers) to read Azure and Entra data on MS Graph API for security monitoring.

## Requirments

The following is a list of requirements to run FortiCNAPP Terraform modules for Azure:

- Azure Global Administrator - An Azure portal account that has a Global Administrator role for your tenant's directory. (required for Directory Readers role assignement)
- Azure Owner Role - An Azure portal account with the Owner role in all subscriptions that you want to monitor.
- Azure CLI - The Terraform provider for Azure leverages configuration from the Azure CLI to configure resources in Azure.
- FortiCNAPP Administrator - A FortiCNAPP account with administrator privileges.
- Terraform - >= 0.14
- Ensure that you are deploying the integration to a supported Azure region.

## Instructions

Follow these steps to deploy:

1. Rename the file `terraform.tfvars.txt` to `terraform.tfvars`.
2. Terraform code will integrate the primary azure subscription (You can verify it with command line: az account show). You can change that behavior with subscription scope variables.
3. (Optional) Customize your deployment: Default values are provided for all variables, but you may want to customize some of them:
    - lacework_integration_name
    - application name and owner
    If You want use your existing application id, set create_application = fales and fill in Your Provisioned Application variables.

    You can allow Management Group level instead of Subscription level by setting use_management_group = true and provide management_group_id.

4. Run the following commands:
<code><pre>
   terraform init
   terraform plan
   terraform apply
</code></pre>

You can delete the integration and remove all created resources using the following command:
<code><pre>
   terraform destroy
</code></pre>