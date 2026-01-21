# ☁️ Azure: Cloud API Integration


### 🧾 Onboarding Requirements (Just for deployment phase - Terraform) 

| Role | Description |
|------|--------------|
| **Azure Global Administrator** | An Azure portal account that has the **Global Administrator** role (In Microsoft Entra ID) for your tenant's directory: https://entra.microsoft.com/ |
| **Azure Owner Role** | An Azure portal account with the **Owner** role in all subscriptions that you want to monitor. |
| **Lacework FortiCNAPP Administrator** | A Lacework account with **administrator privileges** to create and manage cloud integrations. |
| ⚡ **Deployment Methods** | Supported installation environments and automation options:<br>• **Azure Cloud Shell**<br>• **Host connected to Azure subscription being used** | — |


## 🧠 Why Cloud API Integration ?

### ☁️ Azure Integration Overview

| Description |
|--------------|
| Integrates with your Azure Cloud API environment to provide visibility into **Configuration Compliance**, **Cloud Identity Risk Management**, and **Threat Detection** across your cloud environment. |
| FortiCNAPP connects to Azure through a secure **service principal and role-based access** to collect **configuration**, **identity**, and **activity** data. |
| The following integrations — **CSPM**, **Activity Log**, and **CIEM** — work together to deliver unified visibility and risk analysis across your Azure environment. |


## ☁️ Azure Cloud Security Posture Management (CSPM) — Configuration Workflow

| Aspect | Description |
|--------|--------------|
| **Purpose** | Provides comprehensive visibility into Azure configuration risks, misconfigurations, and compliance posture across subscriptions, tenants, and resources. |
| **Data Source** | **Reader Role (Subscription Level)** – Grants read-only access to view Azure resources and their configurations within a subscription, without the ability to modify them. This allows FortiCNAPP to collect posture and compliance data across supported Azure services such as compute, networking, storage, and security configurations.<br>**Key Vault Reader Role (Subscription Level)** – Allows FortiCNAPP to access metadata of all Key Vaults in the subscription. Any new Key Vaults added will automatically be included for compliance monitoring.<br>**Directory Reader Role (Microsoft Entra ID)** – Enables FortiCNAPP to collect directory objects (users, groups, members, and app registrations) from Microsoft Entra ID using Microsoft Graph API calls. This identity data supports LQL (Lacework Query Language) datasources and IAM compliance policies. |
| **Workflow** | FortiCNAPP connects using the Azure service principal with the above roles. It reads configuration and identity data from Azure services and evaluates them against built-in security and compliance frameworks (CIS, NIST, PCI-DSS, ISO, etc.). When Directory Reader is granted, identity-based posture and IAM compliance checks are also performed. |
| **Findings** | Identifies misconfigurations such as open Network Security Groups (NSGs), publicly accessible storage or Key Vaults, disabled encryption, missing diagnostic settings, and non-compliant access policies. |
| **Outcome** | Provides continuous configuration visibility, compliance scoring, and least-privilege posture assessment across all Azure subscriptions and directories. |
| **Notes** | If the **Directory Reader** role is **disabled**, FortiCNAPP will not collect Entra ID (Azure AD) user, group, or app registration data. As a result, related **LQL datasources** and **IAM compliance policies** will not be evaluated—this may be required in environments with strict privacy or regulatory controls. |


<img width="1358" height="563" alt="Screenshot 2025-11-10 at 5 39 47 PM" src="https://github.com/user-attachments/assets/a016647f-a8c1-49f3-800c-c8b9ea6bd7f7" />

<img width="1316" height="342" alt="Screenshot 2025-11-10 at 5 40 53 PM" src="https://github.com/user-attachments/assets/544d96a8-8463-4bbd-bc65-94857bdc23de" />

-----
-----

## 📜 Azure Activity Log Integration — Configuration Workflow

### 🔁  Azure Activity - Terms Definition notes (General)

| Stage | What It Does | Data Type |
|--------|---------------|-----------|
| **Azure Monitor Diagnostic Settings** | Exports Azure Activity Logs from each subscription to a centralized Storage Account under `insights-activity-logs/` | Activity Log JSON files |
| **Event Grid** | Detects creation of new Activity Log blobs in the Storage Account and triggers notifications when new data is available | Event notification |
| **Storage Queue** | Receives and stores notifications from Event Grid containing the blob path and metadata about newly created log files | JSON message |

-----
### 📜 Azure Activity - Configuration Workflow
| Aspect | Description |
|--------|--------------|
| **Purpose** | Collects and analyzes Azure subscription activity for anomaly detection, behavioral analysis, and forensic visibility. |
| **Data Source** | **Azure Activity Logs** – Captures control-plane operations.<br>**Custom Role (Resource Group Level)** – Allows FortiCNAPP to read storage, queues, Event Grid, and keys via Azure APIs. |
| **Workflow** | Azure Monitor exports Activity Logs → logs written hourly to a central Storage Account (`insights-activity-logs`) → Event Grid detects new blobs → sends notifications to a Storage Queue → Lacework FortiCNAPP leverages an Event Grid subscription that creates Queue messages → Lacework FortiCNAPP pulls the new logs as soon as they appear. |
| **Findings** | Detects suspicious admin actions, unauthorized changes, and unusual control-plane activity. |
| **Outcome** | Provides near real-time visibility into Azure operations with correlated identity and configuration insights. |


<img width="740" height="391" alt="512059150-e00561bc-520a-42b9-b701-4265a795cfdc" src="https://github.com/user-attachments/assets/db8763db-0809-4fcd-974c-9e73bf94df05" />
<img width="1149" height="462" alt="Screenshot 2025-11-10 at 5 36 18 PM" src="https://github.com/user-attachments/assets/7c45487c-bdd5-41ec-acde-f2a4809a9eee" />

-----
-----

### 🔐 Cloud Infrastructure Entitlement Management (CIEM) — Configuration Workflow (Azure)

| Aspect | Description |
|--------|--------------|
| **Purpose** | Analyzes Azure users, roles, and assignments to identify excessive permissions, risky access, and privilege escalation paths. |
| **Data Source** | Data from **CSPM** and **Activity Log** integrations mentioned above, no additional or special integration required for CIEM. |
| **Workflow** | CIEM uses Entra-ID Directory Reader to list users/groups/roles/etc.. and Azure Activity log to check which permissions and excessive privileges, etc... are used . |
| **Findings** | Detects unused or excessive role assignments, custom roles with high privilege scope, inherited access chains, and potential privilege escalation risks. |
| **Outcome** | Provides complete Azure IAM visibility, access path mapping, and least-privilege recommendations to improve identity security and compliance posture. |

-----
-----

### 🧱 FortiCNAPP Terraform Deployment Options (In this document we will follow Guided UI Configuration followed by FortiCNAPP CLI Integration):

> 💡 **Note:**  
> You can start with **Guided Configuration** for the Cloud API setup and, if needed, continue using the **FortiCNAPP CLI** — all required tools will be already installed through the Guided Configuration process.  
> Under the hood, the **Guided Configuration** workflow automatically leverages the **FortiCNAPP CLI** to perform deployment actions.
> If you want to go directly with FortiCNAPP CLI, you can use the Guided UI Script only to install all required tools ( Terraform , API-Key & FortiCNAPP CLI).

| Deployment Method | Description | Supported Capabilities |
|--------------------|--------------|--------------------------|
| ⚡ **Automated Configuration** | Deploy FortiCNAPP using a **prebuilt Terraform automation flow** that provisions all required resources automatically at the **Azure subscription level**. <br><br>⚙️ **Note:** Currently supports **Subscription-level integrations only**. | ✅ Single Azure Subscription <br>✅ Cloud API Configuration Visibility <br>✅ Agentless Workload Scanning |
| 🎯 **Terraform via Guided Configuration (UI)** | Deploy and manage FortiCNAPP integrations through the **FortiCNAPP Web Console** using a **wizard-based guided setup**. <br><br>Supports connecting Azure environments **without direct CLI interaction**, simplifying onboarding for multiple subscriptions or management groups. | ✅ Single, Multiple, or All Subscriptions <br>✅ Management Group Level Integration <br>✅ Cloud API Configuration Visibility |
| ⚙️ **Terraform via FortiCNAPP CLI** | Lacework FortiCNAPP CLI is an open source project written in Golang and released as separate binaries for Linux, macOS, and Windows**. <br><br>Ideal for all deployments with advanced automation. | ✅ Single, Multiple, or All Subscriptions <br>✅ Management Group Level Integration <br>✅ Cloud API Configuration Visibility <br>✅ Agentless Workload Scanning |

-----
-----

#### 🧱 FortiCNAPP Terraform Deployment using Guided UI Configuration followed by FortiCNAPP CLI Integration (if needed):

-----
<img width="1267" height="395" alt="Guided-config" src="https://github.com/user-attachments/assets/72d88d48-fc60-4b97-ae4e-6b64c48c1948" />

-----

<img width="661" height="466" alt="Screenshot 2025-11-10 at 12 59 23 PM" src="https://github.com/user-attachments/assets/eb53de80-e1b8-46c4-bde8-8a39db6440ac" />

-----

<img width="1303" height="669" alt="Screenshot 2025-11-11 at 12 32 10 PM" src="https://github.com/user-attachments/assets/709e66b5-d8a7-4289-9790-1f4ea6806cbf" />

-----

<img width="679" height="556" alt="Screenshot 2025-11-10 at 1 00 43 PM" src="https://github.com/user-attachments/assets/74e76cda-f946-4760-b239-639c5589d063" />

-----

<img width="1030" height="85" alt="Screenshot 2025-11-11 at 12 57 51 PM" src="https://github.com/user-attachments/assets/8acf70f9-3e58-491b-b40a-c00602ee134d" />

-----

<img width="1097" height="134" alt="Screenshot 2025-11-11 at 12 55 08 PM" src="https://github.com/user-attachments/assets/b31838f7-3750-4873-b2f6-e643e954f135" />

-----
**Save the Terraform files or make sure you have mounted storage to cloudshell for persistence storage else no files will persist beyond current session** 
> 💡 **Note:**  You will use terraform files later for checking, rebuild or destroying the environment.

-----
<img width="578" height="148" alt="Screenshot 2025-11-10 at 1 07 40 PM" src="https://github.com/user-attachments/assets/aec0b263-ff63-4c31-ac94-344d1614f358" />

-----
-----

#### 🧱 FortiCNAPP Terraform Deployment using FortiCNAPP CLI-Interactive Integration:
-----



<img width="1021" height="400" alt="Screenshot 2025-11-11 at 10 45 51 PM" src="https://github.com/user-attachments/assets/9f57ef24-255e-43f5-9832-ef185a7cea44" />


-----
-----

### 🧱 FortiCNAPP Main Advanced configuration Guided UI Configuration:

| Options                       | Description                                                                 |
| ----------------------------- | --------------------------------------------------------------------------- |
| Specify list of subscriptions | Requires **Owner role** on each selected subscription.                      |
| Enable all subscriptions      | Requires **Owner role** on all subscription in the tenant.                  |
| Specify management group ID   | Requires **Management Group Owner role** for management group–level access. |   

- For Subscription  It will deploy Storage/RG in the default Subscription and IAM Role in each Subcription.
- For Management: It will Inherit IAM role to subscriptions under Management and Storage/RG in the default Subscription.


| Additional Options       | Description                                                                                                                                                                                                                                                                                      |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Existing storage account | You can use an existing or manually create new storage account within a resource group for FortiCNAPP                                                                                                                                                                                                          
| Follow steps for storage | Manual setup guide: [https://docs.fortinet.com/document/forticnapp/latest/administration-guide/521511/azure-activity-log-integration-manual-configuration](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/521511/azure-activity-log-integration-manual-configuration) |




<img width="824" height="460" alt="Screenshot 2026-01-20 at 4 39 09 PM" src="https://github.com/user-attachments/assets/75aba5d6-24f4-4788-abfc-55f24b6bad37" />





### 📘 Reference Links

| Topic | Documentation Link |
|--------|---------------------|
| **Azure Integration – Guided Configuration** | [FortiCNAPP Azure Integration (Guided Configuration)](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/644240/azure-integration-guided-configuration) |
| **Azure App for Integration** | [About Entra ID Permissions and Azure App Setup](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/644235#about-entra-id-permissions) |
| **Lacework FortiCNAPP for Azure FAQ** | [FortiCNAPP for Azure – FAQ](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/318933/lacework-forticnapp-for-azure-faq) |
| **Azure Activity Log Integration – Manual Configuration** | [Manual Configuration for Azure Activity Log Integration](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/521511/azure-activity-log-integration-manual-configuration) |

