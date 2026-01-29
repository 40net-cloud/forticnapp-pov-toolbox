




https://registry.terraform.io/modules/lacework/agentless-scanning/azure/latest


This Terraform module installs global and regional resources. The global resources are installed once per integration. The regional resources are installed in each region where workloads will be scanned. This ensures that no cross-region traffic occurs and reduces latency.


| Step | Description |
|-----:|-------------|
| 1 | The customer deploys the **Agentless AWLS Terraform module for Azure**, which provisions all required resources in the customer subscription. |
| 2 | Terraform provisions the following components: <br><br>• **Microsoft Entra ID application & service principal (Global)** <br>• **Azure RBAC role assignments (Subscription / Resource Group)** <br>• **Storage Account (Global – scan artifacts & metadata)** <br>• **Container Apps Environment (Per Region)** <br>• **Container App Jobs (Per Region)** <br>• **Virtual Network, Subnet, NAT Gateway, NSG (Per Region)** |
| 3 | A **Container App Job** is executed in the customer’s Azure subscription to initiate the scan. |
| 4 | The job enumerates customer workloads, identifies attached managed disks, and creates **temporary read-only snapshots** for scanning. |
| 5 | Snapshots are securely attached to the scanning job environment and analyzed **without deploying agents inside customer workloads**. |
| 6 | Scan metadata and results are written to the **customer-owned Azure Storage Account**. |
| 7 | **FortiCNAPP retrieves scan results and metadata** from the customer storage account using **least-privilege, identity-based access**. |
| 🧹 Automatic Cleanup | Temporary snapshots, scan artifacts, and stale jobs are automatically removed to minimize footprint and cost. |
| ⏱ Scan Frequency | By default, scans run **every 24 hours**. |
| 🔒 Privacy-First Design | FortiCNAPP has **no direct network or OS-level access** to customer workloads. All interactions occur through Azure APIs and customer-controlled resources. |
| 🎯 Selective Scanning | Customers can limit which workloads are scanned using **filters, tags, or resource queries**. |
| ☁ Powered by Azure | Built using **Azure Container Apps**, **Azure Managed Identity**, and **Azure-native networking and storage services**. |

