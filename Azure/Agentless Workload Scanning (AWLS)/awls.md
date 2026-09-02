
Azure AWLS Terraform Modules and Examples:
A Terraform Module to configure the Lacework Agentless Scanner on Azure.
https://github.com/lacework/terraform-azure-agentless-scanning
Examples:
https://github.com/lacework/terraform-azure-agentless-scanning/tree/main/examples

https://registry.terraform.io/modules/lacework/agentless-scanning/azure/latest
This Terraform module installs global and regional resources. The global resources are installed once per integration. 
The regional resources are installed in each region where workloads will be scanned. This ensures that no cross-region traffic occurs and reduces latency.

https://registry.terraform.io/modules/lacework/agentless-scanning/azure/latest/examples/custom-vnet

## 🧠 Why Agentless Workload Scanning ?

| Section | Description |
|----------|--------------|
| **Overview** | **Agentless Workload Scanning (AWLS)** provides comprehensive visibility into **vulnerability risks** and **secrets** across your cloud workloads — without installing agents. |
| **Flexibility & Coverage** | Offers broad scanning capabilities for both **hosts** and **container images**, including:<br>• Scanning **running containers**<br>• Scanning **images stored on disk** |
| **Key Benefits** | • Gain insight into **CVEs** on hosts and containers.<br>• Eliminate the need to install or manage agents.<br>• Maintain **private-by-design** scanning within your own AWS environment.<br>• Improve coverage for **container and host vulnerability detection**. |
| ⚠️ **Note** | • **AWLS does not provide workload activity monitoring.**<br>• To gain full runtime visibility and behavioral analytics, you must also deploy the **FortiCNAPP Agent**.<br>• Agentless is **complementary** to the agent — designed to **co-exist**, not replace it. |
| 🧾 **Supported Operating Systems (Linux & macOS)** | [View Documentation →](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/818980/container-image-support#supported-language-libraries-and-package-managers)<br>Lists supported Linux distributions and macOS versions for FortiCNAPP agent and agentless workload scanning. |
| 🪟 **Agentless Scanning for Windows** | [View Documentation →](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/838971/agentless-scanning-for-windows)<br>Details supported Windows operating systems for agentless workload scanning. |
| 🧠 **Host OS and Language Library Support for Vulnerability Assessment** | [View Documentation →](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/999307/host-os-and-language-library-support-for-vulnerability-assessment#supported-linux-operating-systems-packages-and-language-libraries)<br>Reference list of supported operating systems, packages, and language libraries used in FortiCNAPP vulnerability assessments. |

## Agentless Scanning Overview

| **Feature / Description** | **Details** |
|----------------------------|--------------|
| **Default Behavior** | Agentless scans the **root volume** of a host for vulnerabilities by default. |
| **Secondary Volumes** | Any volumes mounted by **filesystem UUID** or **label** will also be scanned if scanning of secondary volumes is enabled. |
| **Kubernetes Persistent Volumes** | Agentless **does not yet scan persistent volumes in Kubernetes**, specifically those tagged with `kubernetes.io/created-for/pv/name`. |
| **Scanning Method** | Agentless workload scanning creates **snapshots** of disk volumes and analyzes them **without impacting** the performance of the primary volumes. |
| **Snapshot Process** | Snapshots are requested for each volume on each instance. A **job queue**




## Azure Agentless Scanning Overview
Azure Agentless Workload Scanning deploys scheduled, customer-owned scanning infrastructure that clones virtual machine disks, scans them using ephemeral virtual machines, stores results in customer storage, and ingests findings into FortiCNAPP without deploying agents or accessing running workloads.  

|                    Step | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ----------------------: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|                       1 | The customer deploys the **Azure Agentless Workload Scanning (AWLS) Terraform module**, which provisions all required resources in the customer’s Azure environment.                                                                                                                                                                                                                                                                                                         |
|                       2 | Terraform provisions the following components: <br><br>• **Microsoft Entra ID application and service principal** (Global) <br>• **Customer-owned Azure Storage Account** (Global / scan artifacts and metadata) <br>• **Container Apps Environment** (per region) <br>• **Container App Jobs** (per region) <br>• **Virtual Network, Subnet, NAT Gateway, and Network Security Group** (per region) <br>.  **Azure RBAC role assignments** (subscription and/or resource group scope) • |
|                       3 | The **Container App Job is triggered on a schedule**, without interactive action from the FortiCNAPP platform.                                                                                                                                                                                                                                                                                                                                                               |
|                       4 | The Container App Job determines which virtual machines should be scanned based on the configured tenant or subscription scope.                                                                                                                                                                                                                                                                                                                                              |
|                       5 | For each selected virtual machine, the scanner identifies the attached **Azure managed disks** and creates **temporary read-only snapshots**.                                                                                                                                                                                                                                                                                                                                |
|                       6 | The snapshots are cloned into the **scanner’s resource group**, and **ephemeral scanning virtual machines** are launched in that same resource group.                                                                                                                                                                                                                                                                                                                        |
|                       7 | The scanning virtual machines attach the cloned disks, mount them in the file system, and perform **agentless scanning** without installing software inside customer workloads.                                                                                                                                                                                                                                                                                              |
|                       8 | The scanning virtual machines upload scan metadata and results to the **customer-owned Azure Blob Storage account**.                                                                                                                                                                                                                                                                                                                                                         |
|                       9 | A FortiCNAPP ingestion service runs on a schedule and **retrieves scan results and metadata** from the customer storage account for processing in the FortiCNAPP platform.                                                                                                                                                                                                                                                                                                   |
|    🧹 Automatic Cleanup | Temporary snapshots, ephemeral scanning virtual machines, and stale scan artifacts are automatically removed to minimize footprint and cost.  



# Deployment: Agentless Workload Scanning for Subscriptions

This configuration enables **agentless workload scanning** for selected Azure subscriptions. It scans workloads in the configured Azure region without installing an agent on each workload.

> Replace every `xxx` value with the appropriate value for your environment before deployment.

## Configuration

| Setting | Value | Description |
|---|---|---|
| Subscription ID for Lacework resources | `xxx` | Azure subscription used to provision the required Lacework resources. |
| Configure additional subscriptions | `No` | Whether to configure more subscriptions during this setup. |
| Configuration integration | `No` | Enables collection of Azure configuration data. |
| Activity Log integration | `No` | Enables collection of Azure Activity Log events. |
| Agentless integration | `Yes` | Enables agentless workload scanning. |
| Agentless integration level | `SUBSCRIPTION` | Applies scanning configuration at the subscription level. |
| Global agentless scanning | `Yes` | Enables agentless scanning across the configured scope. |
| Create Log Analytics workspace | `No` | Creates a new Log Analytics workspace if one is required. |
| Regions for scanning | `West US` | Azure regions where agentless workload scanning will run. |
| Subscription IDs for scanning | `xxx` | Comma-separated Azure subscription IDs to scan. |
| Entra ID Activity Log integration | `No` | Enables Microsoft Entra ID Activity Log collection. |
| Output location | _Optional_ | Directory where generated deployment output is written. |
| Run Terraform plan | `Yes` | Runs `terraform plan` to preview the deployment. |

## Example CLI Flow

```powershell
lacework generate cloud-account azure
```

When prompted, use the values in the table above. After configuration is complete, allow Terraform to initialize the required providers and review the generated plan before applying it.

## Notes

- Keep subscription IDs out of source control; use `xxx` in documentation and examples.
- Limit regions and subscriptions to the workload scope you intend to scan.
- Review the Terraform plan to confirm the resources and permissions match your environment.

## Example

The following example reflects an agentless workload-scanning setup for a single Azure subscription in **West US**:

```text
Subscription ID to be used to provision Lacework resources: xxx
Configure Subscriptions (optional): No
[Configuration] Enable Configuration integration: No
[Activity Log] Enable Activity Log integration: No
[Agentless] Enable Agentless integration: Yes
[Agentless] Select integration level: SUBSCRIPTION
[Agentless] Enable global Agentless scanning: Yes
[Agentless] Create Log Analytics Workspace: No
[Agentless] List of regions for scanning: West US
[Agentless] List of subscription IDs for scanning: xxx
[Entra ID Activity Log] Enable Entra ID Activity Log Integration: No
Provide the location for the output to be written: (optional)
Run Terraform plan now: Yes
```
