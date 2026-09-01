


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
| 🧾 **Supported Operating Systems (Linux & macOS)** | [View Documentation →](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/671486)<br>Lists supported Linux distributions and macOS versions for FortiCNAPP agent and agentless workload scanning. |
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
|                       2 | Terraform provisions the following components: <br><br>• **Microsoft Entra ID application and service principal (Global)** <br>• **Customer-owned Azure Storage Account** (Global / scan artifacts and metadata) <br>• **Container Apps Environment** (per region) <br>• **Container App Jobs** (per region) <br>• **Virtual Network, Subnet, NAT Gateway, and Network Security Group** (per region) <br>  **Azure RBAC role assignments** (subscription and/or resource group scope) • |
|                       3 | The **Container App Job is triggered on a schedule**, without interactive action from the FortiCNAPP platform.                                                                                                                                                                                                                                                                                                                                                               |
|                       4 | The Container App Job determines which virtual machines should be scanned based on the configured tenant or subscription scope.                                                                                                                                                                                                                                                                                                                                              |
|                       5 | For each selected virtual machine, the scanner identifies the attached **Azure managed disks** and creates **temporary read-only snapshots**.                                                                                                                                                                                                                                                                                                                                |
|                       6 | The snapshots are cloned into the **scanner’s resource group**, and **ephemeral scanning virtual machines** are launched in that same resource group.                                                                                                                                                                                                                                                                                                                        |
|                       7 | The scanning virtual machines attach the cloned disks, mount them in the file system, and perform **agentless scanning** without installing software inside customer workloads.                                                                                                                                                                                                                                                                                              |
|                       8 | The scanning virtual machines upload scan metadata and results to the **customer-owned Azure Blob Storage account**.                                                                                                                                                                                                                                                                                                                                                         |
|                       9 | A FortiCNAPP ingestion service runs on a schedule and **retrieves scan results and metadata** from the customer storage account for processing in the FortiCNAPP platform.                                                                                                                                                                                                                                                                                                   |
|    🧹 Automatic Cleanup | Temporary snapshots, ephemeral scanning virtual machines, and stale scan artifacts are automatically removed to minimize footprint and cost.   
