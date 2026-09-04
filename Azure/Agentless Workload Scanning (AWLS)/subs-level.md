# FortiCNAPP Agentless Workload Scanning for Microsoft Azure

This guide documents subscription-level deployment of FortiCNAPP Agentless Workload Scanning (AWLS) on Microsoft Azure using the FortiCNAPP CLI and the official Terraform module.

AWLS scans supported Azure virtual-machine disks for host vulnerabilities, container-image vulnerabilities, and supported secrets without installing an agent inside the monitored workload. It does not provide runtime activity monitoring or behavioral telemetry; deploy the FortiCNAPP agent when those capabilities are required.

> [!IMPORTANT]
> Replace the masked subscription IDs and region names in all examples. Review every Terraform plan before applying it.

## How Azure AWLS works

1. Terraform creates the global and regional scanning infrastructure in a customer-controlled Azure scanning subscription.
2. A regional Azure Container App Job periodically identifies eligible virtual machines in the configured scope.
3. The service clones the relevant VM disks into the scanning subscription.
4. Temporary scanning VMs mount the cloned disks and inspect their contents without installing software in the source VM.
5. Scan artifacts and metadata are written to the customer-owned Azure Storage Account and made available to FortiCNAPP for evaluation.
6. Temporary scanning resources and stale artifacts are cleaned up automatically.

The Container App Job checks hourly whether work is due. The configured scan frequency controls collection frequency; vulnerability results are evaluated and published by FortiCNAPP on its evaluation schedule.

## Azure resource model

Azure subscriptions are ownership, authorization, policy, quota, and billing boundaries. Azure regions are physical deployment locations. A region is not above a subscription in the Azure hierarchy.

### Azure hierarchy

```mermaid
flowchart TB
    tenant[Microsoft Entra tenant]
    sub1[Subscription A<br/>Scanning and monitored]
    sub2[Subscription B<br/>Optional additional monitored subscription]
    rg[AWLS scanning resource group]
    west[West US resources]
    east[East US resources]
    workloads1[Workloads in Subscription A]
    workloads2[Workloads in Subscription B]

    tenant --> sub1
    tenant --> sub2
    sub1 --> rg
    rg --> west
    rg --> east
    sub1 --> workloads1
    sub2 --> workloads2
    west -. Azure RBAC permits regional scanning .-> workloads1
    west -. Azure RBAC permits regional scanning .-> workloads2
    east -. Azure RBAC permits regional scanning .-> workloads1
    east -. Azure RBAC permits regional scanning .-> workloads2
```

The subscription is the Azure ownership and authorization boundary. The region describes where an individual Azure resource or workload is physically deployed. AWLS infrastructure can reside in one scanning subscription while Azure RBAC permits it to scan workloads in other subscriptions within the configured scope.

### Global resources

Global resources are created once per AWLS integration by the module where `global = true`. In a multi-region deployment, the first generated regional module is the global module.

- FortiCNAPP cloud-account integration
- Microsoft Entra ID application and service principal
- User-assigned managed identity
- Azure Key Vault and secret
- Customer-owned Azure Storage Account and blob container
- Shared custom role definitions and role assignments
- Shared integration metadata used by regional modules

“Global” is a logical Terraform role. These Azure resources still have a physical Azure location, normally the first region listed during generation.

### Regional resources

Regional resources are created in every region containing workloads that must be scanned.

- Azure Container Apps Environment
- Azure Container App Job
- Virtual network and subnet
- Network Security Group
- NAT Gateway and public IP when NAT is enabled
- Optional Log Analytics workspace
- Temporary scanning VMs, cloned disks, snapshots, and network interfaces created during scanning

For multi-region deployments, only the first module uses `global = true`. Additional regional modules use `global = false` and receive `global_module_reference` from the first module.

## Deployment topology comparison

### One subscription, two regions

```mermaid
flowchart TB
    tenant[Microsoft Entra tenant]
    subA[Subscription A<br/>Scanning and monitored]
    global[Global/shared AWLS resources<br/>Identity, Key Vault, storage, integration]
    west[West US regional scanner<br/>Container App Job and network]
    east[East US regional scanner<br/>Container App Job and network]
    westVMs[West US workloads]
    eastVMs[East US workloads]

    tenant --> subA
    subA --> global
    global --> west
    global --> east
    subA --> westVMs
    subA --> eastVMs
    west -->|scans same-region disks| westVMs
    east -->|scans same-region disks| eastVMs
```

This design has one monitored subscription, one set of global resources, and one regional scanner deployment in each of the two regions.

### Two subscriptions, two regions

```mermaid
flowchart TB
    tenant[Microsoft Entra tenant]
    subA[Subscription A<br/>Scanning and monitored]
    subB[Subscription B<br/>Monitored]
    global[Global/shared AWLS resources in Subscription A<br/>Identity, Key Vault, storage, integration]
    west[West US regional scanner in Subscription A]
    east[East US regional scanner in Subscription A]
    aWest[Subscription A<br/>West US workloads]
    aEast[Subscription A<br/>East US workloads]
    bWest[Subscription B<br/>West US workloads]
    bEast[Subscription B<br/>East US workloads]

    tenant --> subA
    tenant --> subB
    subA --> global
    global --> west
    global --> east
    subA --> aWest
    subA --> aEast
    subB --> bWest
    subB --> bEast
    west -->|scans through RBAC| aWest
    west -->|scans through RBAC| bWest
    east -->|scans through RBAC| aEast
    east -->|scans through RBAC| bEast
```

Adding Subscription B does **not** create another complete AWLS stack when both subscriptions use the same scanning subscription and regions. The same West US and East US regional scanners can scan eligible same-region workloads across both monitored subscriptions through Azure RBAC.

| Area | One subscription, two regions | Two subscriptions, two regions |
|---|---|---|
| Global AWLS integration | One | One |
| Scanning subscription | One | One |
| Regional scanner deployments | Two | Two |
| Monitored subscriptions | One | Two |
| `included_subscriptions` entries | One | Two |
| Cross-subscription authorization | Not needed for a separate monitored subscription | Required for Subscription B |
| Workload coverage | Eligible workloads in Subscription A | Eligible workloads in Subscriptions A and B |
| Scanner-infrastructure billing | Scanning subscription | Same scanning subscription |
| Expected scan volume and cost | Based on workloads in one subscription | May increase because both subscriptions contribute workloads |

The number of regional scanner deployments follows the number of configured regions, not the number of monitored subscriptions. Adding a subscription mainly expands authorization and workload scope. Adding a region creates another regional Container Apps and networking stack.

## Prerequisites

- FortiCNAPP administrator access
- FortiCNAPP CLI installed and configured
- Terraform 1.9 or later
- Azure CLI installed and authenticated
- Deployment permissions required by the official Azure AWLS documentation
- Access to create role definitions and role assignments in the scanning and monitored subscriptions
- Adequate regional Azure vCPU and public-IP quotas for scanner workloads
- TCP 443 egress from scanner infrastructure to required Azure and FortiCNAPP endpoints
- All subscriptions in a subscription-level integration should be accessible in the same Microsoft Entra tenant

Verify the active Azure context before deployment:

```powershell
az account show --query "{Subscription:name,SubscriptionId:id,Tenant:tenantId,User:user.name}" -o table
```

List workload regions before choosing scanner regions:

```powershell
az vm list --subscription "<MONITORED_SUBSCRIPTION_ID>" --query "[].{VM:name,Region:location,ResourceGroup:resourceGroup}" -o table
```

Deploy regional scanner infrastructure only in regions containing workloads that need to be scanned.

## CLI deployment examples

The following examples enable only AWLS. Configuration, Activity Log, and Entra ID Activity Log integrations are not enabled.

### One subscription, one region

```powershell
lacework generate cloud-account azure --agentless --integration_level "SUBSCRIPTION" --agentless_subscription_ids "<SCANNING_SUBSCRIPTION_ID>" --subscription_id "<SCANNING_SUBSCRIPTION_ID>" --regions "<PRIMARY_REGION>" --global=true --noninteractive --output "/home/<USER>/azure-agentless-single-sub-single-region"
```

### Two subscriptions, one region

```powershell
lacework generate cloud-account azure --agentless --integration_level "SUBSCRIPTION" --agentless_subscription_ids "<SCANNING_SUBSCRIPTION_ID>,<SECOND_MONITORED_SUBSCRIPTION_ID>" --subscription_id "<SCANNING_SUBSCRIPTION_ID>" --regions "<PRIMARY_REGION>" --global=true --noninteractive --output "/home/<USER>/azure-agentless-two-subs-single-region"
```

### Two subscriptions, two regions

```powershell
lacework generate cloud-account azure --agentless --integration_level "SUBSCRIPTION" --agentless_subscription_ids "<SCANNING_SUBSCRIPTION_ID>,<SECOND_MONITORED_SUBSCRIPTION_ID>" --subscription_id "<SCANNING_SUBSCRIPTION_ID>" --regions "<PRIMARY_REGION>,<SECOND_REGION>" --global=true --noninteractive --output "/home/<USER>/azure-agentless-two-subs-two-regions"
```

In these commands:

- `--agentless_subscription_ids` lists the subscriptions whose workloads will be monitored.
- `--subscription_id` identifies the subscription where AWLS infrastructure is deployed and billed.
- `--regions` lists the regions in which regional scanner infrastructure is created.
- The first region is used by the module containing the shared global resources.
- Subscription IDs and regions are comma-separated, with no curly quotation marks.

## Generate, review, and deploy

Use a separate directory for each independent Terraform deployment. Do not mix a new configuration with a state file belonging to another deployment.

```powershell
Set-Location "/home/<USER>/<GENERATED_OUTPUT_DIRECTORY>"
terraform init
terraform fmt
terraform validate
terraform plan -out awls.tfplan
terraform apply awls.tfplan
```

Do not commit these files to source control:

- `terraform.tfstate`
- `terraform.tfstate.backup`
- saved plan files such as `awls.tfplan`
- FortiCNAPP or Azure credentials

Terraform state can contain sensitive values. Use a protected remote backend for production or team-managed deployments.

## Multi-region Terraform structure

A generated two-region deployment should follow this pattern:

```hcl
module "awls_primary_region" {
  source  = "lacework/agentless-scanning/azure"
  version = "~> 1.6"

  global                   = true
  integration_level        = "SUBSCRIPTION"
  region                   = "<PRIMARY_REGION>"
  scanning_subscription_id = "<SCANNING_SUBSCRIPTION_ID>"

  included_subscriptions = [
    "/subscriptions/<SCANNING_SUBSCRIPTION_ID>",
    "/subscriptions/<SECOND_MONITORED_SUBSCRIPTION_ID>",
  ]
}

module "awls_second_region" {
  source  = "lacework/agentless-scanning/azure"
  version = "~> 1.6"

  global                   = false
  global_module_reference  = module.awls_primary_region
  integration_level        = "SUBSCRIPTION"
  region                   = "<SECOND_REGION>"
  scanning_subscription_id = "<SCANNING_SUBSCRIPTION_ID>"
}
```

Set `included_subscriptions` only on the global module. Regional modules inherit the shared configuration through `global_module_reference`.

## Important module inputs

The official module README is the source of truth for inputs, types, and defaults.

| Input | Description | Type | Default |
|---|---|---:|---:|
| [`create_log_analytics_workspace`](https://github.com/lacework/terraform-azure-agentless-scanning/tree/main#input_create_log_analytics_workspace) | Creates a Log Analytics workspace to see container logs. Defaults to `false` to avoid charging. | `bool` | `false` |
| [`global`](https://github.com/lacework/terraform-azure-agentless-scanning/tree/main#input_global) | Creates shared global resources for this deployment. Only one module in a multi-region integration should set this to `true`. | `bool` | `false` |
| [`global_module_reference`](https://github.com/lacework/terraform-azure-agentless-scanning/tree/main#input_global_module_reference) | Passes shared outputs from the global module to an additional regional module. | `object` | Empty object |
| [`included_subscriptions`](https://github.com/lacework/terraform-azure-agentless-scanning/tree/main#input_included_subscriptions) | Subscription resource IDs monitored by a `SUBSCRIPTION`-level integration. Set only on the global module. | `set(string)` | `[]` |
| [`integration_level`](https://github.com/lacework/terraform-azure-agentless-scanning/tree/main#input_integration_level) | Integration scope: `SUBSCRIPTION` or `TENANT`. | `string` | Required |
| [`region`](https://github.com/lacework/terraform-azure-agentless-scanning/tree/main#input_region) | Azure region where the regional scanner is deployed. | `string` | `westus2` |
| [`scan_containers`](https://github.com/lacework/terraform-azure-agentless-scanning/tree/main#input_scan_containers) | Enables scanning of supported container images found on workload disks. | `bool` | `true` |
| [`scan_frequency_hours`](https://github.com/lacework/terraform-azure-agentless-scanning/tree/main#input_scan_frequency_hours) | Number of hours between scheduled scans. | `number` | `24` |
| [`scan_host_vulnerabilities`](https://github.com/lacework/terraform-azure-agentless-scanning/tree/main#input_scan_host_vulnerabilities) | Enables host vulnerability scanning. | `bool` | `true` |
| [`scan_multi_volume`](https://github.com/lacework/terraform-azure-agentless-scanning/tree/main#input_scan_multi_volume) | Enables scanning of supported secondary volumes in addition to the root volume. | `bool` | `false` |
| [`scan_stopped_instances`](https://github.com/lacework/terraform-azure-agentless-scanning/tree/main#input_scan_stopped_instances) | Enables scanning of stopped instances. | `bool` | `true` |
| [`scanning_subscription_id`](https://github.com/lacework/terraform-azure-agentless-scanning/tree/main#input_scanning_subscription_id) | Subscription in which AWLS scanner infrastructure is deployed. | `string` | Current AzureRM subscription when blank |
| [`use_nat_gateway`](https://github.com/lacework/terraform-azure-agentless-scanning/tree/main#input_use_nat_gateway) | Uses a NAT Gateway rather than assigning public IP addresses to individual scanning instances. | `bool` | `true` |

> [!NOTE]
> `create_log_analytics_workspace = false` does not disable AWLS. It only prevents the module from creating the optional Log Analytics workspace used to view Container App logs.

## Validate the deployment

Confirm Terraform has no pending differences:

```powershell
terraform plan
```

Expected result after a successful apply:

```text
No changes. Your infrastructure matches the configuration.
```

Confirm the FortiCNAPP integration:

```powershell
lacework cloud-account list
```

List regional Container App Jobs:

```powershell
az containerapp job list --subscription "<SCANNING_SUBSCRIPTION_ID>" --query "[].{Name:name,ResourceGroup:resourceGroup,Location:location,State:properties.provisioningState}" -o table
```

Inspect job executions:

```powershell
az containerapp job execution list --name "<JOB_NAME>" --resource-group "<SCANNING_RESOURCE_GROUP_NAME>" -o table
```

Start a job manually for troubleshooting when appropriate:

```powershell
az containerapp job start --name "<JOB_NAME>" --resource-group "<SCANNING_RESOURCE_GROUP_NAME>"
```

In FortiCNAPP, view agentless vulnerability results under **Vulnerabilities > Hosts** or **Vulnerabilities > Containers**. For container results, group by image ID and filter **Scanner type** to **Agentless**.

## Container-discovery requirements

For Docker workloads, agentless scanning supports the `overlay2` storage driver and recognized Docker storage locations such as `/var/lib/docker`.

Check an Ubuntu Docker host:

```bash
sudo docker info | grep -E 'Server Version|Storage Driver|Docker Root Dir'
findmnt -T /var/lib/docker
sudo docker ps
```

If `/var/lib/docker` is on the root disk, `scan_multi_volume` is unnecessary. If it is on a supported secondary Azure managed disk, review the official requirements and enable `scan_multi_volume` when applicable.

Agentless scanning is periodic rather than real-time. Keep short-lived test containers running through a complete scan and evaluation cycle.

## Troubleshooting

### Azure CLI access token expired

Symptoms:

```text
Error: building client: unable to obtain access token: running Azure CLI: exit status 1
```

Refresh Azure CLI authentication and select the scanning subscription:

```powershell
az login
az account set --subscription "<SCANNING_SUBSCRIPTION_ID>"
az account show --query "{Subscription:id,Tenant:tenantId,User:user.name}" -o table
az account get-access-token --resource "https://management.azure.com/" --query expiresOn -o tsv
az account get-access-token --resource "https://graph.microsoft.com/" --query expiresOn -o tsv
```

Then resume from the same Terraform directory:

```powershell
terraform plan
terraform apply
```

The `azuread` provider requires a Microsoft Graph token. An `end_date_relative` deprecation warning from an older module/provider combination is not the cause of an Azure CLI authentication failure.

### Cloud Shell disconnected or timed out

Cloud Shell can disconnect during a long operation. Terraform normally records each completed resource in state, so resume rather than regenerate the deployment.

1. Reopen Cloud Shell.
2. Return to the same persistent directory.
3. Confirm the state file exists.
4. Refresh Azure authentication.
5. Run `terraform plan` to reconcile actual infrastructure with state.
6. Resume `terraform apply` or `terraform destroy` as appropriate.

```powershell
Set-Location "/home/<USER>/<GENERATED_OUTPUT_DIRECTORY>"
Get-ChildItem -Force
terraform state list
az login
az account set --subscription "<SCANNING_SUBSCRIPTION_ID>"
terraform plan
```

Do not start a second Terraform operation while the first is still running. Do not regenerate into a different directory and expect it to manage resources recorded in the original state.

For long-running production deployments, use a persistent runner and a protected remote Terraform backend rather than relying on local Cloud Shell state.

### State file exists but lists no resources

`terraform.tfstate` can exist while containing zero managed objects. Confirm with:

```powershell
terraform state list
terraform state list -state="./terraform.tfstate.backup"
```

If the current state is empty but the backup lists the correct deployment resources, preserve both files and carefully restore the matching backup before attempting to destroy or update the deployment. Never substitute a state file from another AWLS deployment.

If both states are empty, check whether Azure or FortiCNAPP resources still exist before applying another integration:

```powershell
az group list --query "[?contains(name, 'lacework-agentless')].{Name:name,Location:location}" -o table
lacework cloud-account list
```

### Destroy is slow or appears stuck

Azure RBAC, networking, Key Vault, managed identities, and Entra resources can take several minutes to delete. Avoid interrupting Terraform unless necessary.

Before destroying, preserve the state:

```powershell
Copy-Item ./terraform.tfstate ./terraform.tfstate.before-destroy
terraform plan -destroy
terraform destroy
```

If Cloud Shell times out, reopen it, return to the same directory, refresh `az login`, and rerun `terraform plan -destroy`. Terraform will plan only the remaining resources.

### Destroy fails with `InUseSubnetCannotBeDeleted`

This can occur when AWLS is destroyed while a scan is running, leaving temporary scanner VMs attached to the subnet. First list the VMs in the scanner resource group:

```powershell
az vm list --resource-group "<SCANNING_RESOURCE_GROUP_NAME>" --subscription "<SCANNING_SUBSCRIPTION_ID>" --show-details -o table
```

Only after confirming they are temporary AWLS scanner VMs, delete them:

```powershell
$vmIds = @(az vm list --resource-group "<SCANNING_RESOURCE_GROUP_NAME>" --subscription "<SCANNING_SUBSCRIPTION_ID>" --query "[].id" -o tsv)
if ($vmIds.Count -gt 0) {
  az vm delete --ids $vmIds --yes
}
```

Resume the destroy from the original Terraform directory:

```powershell
terraform destroy
```

Do not manually delete the entire scanning resource group before Terraform finishes. Resources such as Entra applications, service principals, subscription-scoped roles, role assignments, and the FortiCNAPP integration exist outside that resource group.

### No container vulnerabilities appear

Check all of the following:

- The cloud-account integration status is **Success**.
- `scan_containers` is `true`.
- Each monitored subscription is present in `included_subscriptions` on the global module.
- Regional scanner resources exist in every workload region.
- The regional Container App Job has a successful execution.
- No LQL workload filter excludes the VM.
- Docker uses `overlay2` and stores data in a supported path.
- The container persisted on disk through a complete scan cycle.
- FortiCNAPP is viewed under **Vulnerabilities > Containers**, grouped by image ID, with **Scanner type: Agentless**.

## Deprovisioning safely

Always destroy from the directory containing the state that created the deployment:

```powershell
Set-Location "/home/<USER>/<GENERATED_OUTPUT_DIRECTORY>"
terraform state list
terraform plan -destroy
terraform destroy
```

Running `terraform destroy` from a newly generated directory with an empty state will report:

```text
No changes. No objects need to be destroyed.
```

That message does not prove that Azure contains no AWLS resources; it only means the current Terraform state manages none.

## Reference documentation

| Reference | Purpose |
|---|---|
| [Official Azure AWLS Terraform module](https://github.com/lacework/terraform-azure-agentless-scanning/tree/main) | Authoritative module inputs, outputs, resources, requirements, preflight checks, and deprovisioning guidance |
| [Azure AWLS module examples](https://github.com/lacework/terraform-azure-agentless-scanning/tree/main/examples) | Single-region, multi-region, tenant-level, subscription-level, and custom-network examples |
| [Terraform Registry: Azure agentless scanning](https://registry.terraform.io/modules/lacework/agentless-scanning/azure/latest) | Published module version and generated documentation |
| [Subscription-level single-region example](https://github.com/lacework/terraform-azure-agentless-scanning/tree/main/examples/subscription-single-region) | Global and regional resources in one region |
| [Subscription-level multi-region example](https://github.com/lacework/terraform-azure-agentless-scanning/tree/main/examples/subscription-multi-region) | One global module with additional regional modules |
| [Custom VNet example](https://github.com/lacework/terraform-azure-agentless-scanning/tree/main/examples/custom-vnet) | Deploying AWLS with existing/custom networking |
| [FortiCNAPP: Integrating your Azure environment](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/729300/integrating-your-azure-environment) | Azure scanning workflow and global/regional deployment model |
| [FortiCNAPP: Preparing for Azure integration](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/991151/preparing-for-integration) | Permissions, quotas, limitations, and preflight guidance |
| [FortiCNAPP: Deploying AWLS on Azure](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/42109/deploying-agentless-workload-scanning-on-azure) | Deployment procedure and validation |
| [FortiCNAPP: Viewing agentless results](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/692150) | Host and container result locations and filters |
| [FortiCNAPP: Agentless scanning FAQ](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/269317/agentless-workload-scanning-faqs) | Scan behavior, timing, container support, storage, and cleanup |

## Security and cost notes

- Use a dedicated scanning subscription for larger or production deployments when practical.
- Grant only the documented permissions required by AWLS.
- Keep Terraform state and FortiCNAPP credentials out of source control.
- Review regional vCPU, public-IP, NAT Gateway, Storage Account, Container Apps, temporary VM, disk, snapshot, and optional Log Analytics costs.
- `create_log_analytics_workspace = false` avoids the cost of a module-created workspace but reduces access to Container App logs.
- Reduce scan frequency only after considering the additional Azure snapshot and scanning costs.
- Deploy scanner infrastructure only in required workload regions.
