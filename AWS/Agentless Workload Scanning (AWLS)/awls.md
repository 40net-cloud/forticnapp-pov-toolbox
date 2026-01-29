
# ☁️ AWS: Agentless Workload Scanning (AWLS)

## Note: Make sure to review the following files before proceeding.

- [AWS CloudShell Size Workaround](../cloudshell-size-workaround.md)
- [FortiCNAPP & AWS Profiles](../forticnapp-aws-profile.md)
- [AWS Terms and Architecture](../aws-terms-arch.md)

-----
-----
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

---
---  

## ☁️ AWS & FortiCNAPP Agentless Workload Scanning- AWLS Terraform Prerequisites

| Component / Requirement | Description | Reference / Link |
|--------------------------|--------------|------------------|
| 👩‍💻 **AWS Account Admin** | Administrative privileges on each AWS account. Required during onboarding process only. | — |
| 🧾 **AWS Service Quotas** | Ensure that your AWS account has sufficient **Service Quotas** to create and support the required resources in each selected region. This includes quotas for **ECS**, **VPC**, and **Internet Gateways**. | — |
| 🔧 **AWS CLI** | Install and configure the AWS CLI to connect to your AWS Account. | [AWS CLI Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) |
| 🧰 **Linux Tools** | Ensure basic tools (`curl`, `git`, `unzip`) are available in the system `PATH`. | — |
| ⚙️ **Terraform** | Install Terraform if not already configured. | [Terraform Documentation](https://developer.hashicorp.com/terraform/docs) |
| 🧠 **FortiCNAPP CLI** | Open-source CLI tool written in Golang. Available for **Linux**, **macOS**, and **Windows**. Used to interact with FortiCNAPP via the command line. | [FortiCNAPP CLI Guide](https://docs.fortinet.com/document/forticnapp/latest/cli-reference/68020/get-started-with-the-lacework-forticnapp-cli) |
| ⚡ **Deployment Methods** | Supported installation environments and automation options:<br>• **AWS Cloud Shell**<br>• **Hosts Supported by Terraform** | — |

---
---  

# 🚀 How Agentless Workload Scanning Is Deployed ? 
CLI: Non-interactive .vs. Interactive.

## 🔧 Option.1.Using direct FortiCNAP CLI code (non-interactive). Can be used for CloudShell.
##### Example single region (region = me-south-1), change region & output only.

```bash
/home/cloudshell-user
mkdir awls 
awls$ chmod +x /home/cloudshell-user/awls
```

```bash
lacework generate cloud-account aws --output='/home/forticnapp/cloud-api' --agentless='true' --aws_region='me-south-1' --noninteractive --apply 
```


##### Example Multi region (region = eu-central-1 (Monitor & Scan) & me-south-1 (Scan Only), change region & output only.
But first you need to create config file profile ( for multiple regions) required for the CLI.

```bash
mkdir -p ~/.aws
cat <<EOF > ~/.aws/config
[default]
region = me-south-1
output = json
[default]
region = me-central-1
[default]
region = eu-central-1
EOF
```


```bash
lacework generate cloud-account aws --output='/tmp/forti' --agentless='true' --aws_region='me-south-1' --agentless_scanning_accounts default:me-south-1,default:me-central-1 --noninteractive --apply
```

----
----

## 🔧 Option.2. Using FortiCNAP CLI (Interactive)


| Step | Description |
|------|-------------|
| **Overview** | In this setup, **Terraform** is used via the **FortiCNAPP CLI** to deploy a **multi-regional, single-account** or **multi-account** environment. |
| ⚠️ **Pre-Deployment Note** | Make sure you have both:<br>🟦 **AWS Profile** — for your **AWS account integration**<br>🟩 **FortiCNAPP (Lacework) Profile** — for your **FortiCNAPP tenant integration**<br><br>📘 For setup instructions and configuration details, see **[Main AWS Folder `README.md`](../README.md)**. |
| **1-2** | 1. Generate the AWS cloud-account integration using the **FortiCNAPP (Lacework) CLI**:<br>` lacework generate cloud-account aws`<br><br>* 2.(Optional)* Specify a profile if you are using multiple:<br>`lacework generate cloud-account aws --profile default` |
| **3** | During setup, you’ll be prompted for configuration options such as:<br><br>• **Enable integrations for AWS organization** → No<br>• **Main AWS account profile** → default<br>• **Main AWS account region** → eu-central-1<br>• **Enable Agentless integration** → Yes<br>• **Add another scanning AWS account** → Yes<br>• **Scanning AWS account profile** → default<br>• **Scanning AWS account region** → me-south-1<br>• **Enable Configuration integration** → No<br>• **Enable CloudTrail integration** → No<br>• **Custom output location** → .<br>• **Run Terraform plan now?** → Yes |
| **4** | Terraform providers installed:<br>• `hashicorp/null`<br>• `hashicorp/aws`<br>• `lacework/lacework`<br>• `hashicorp/random` |
| **5** | Verify the integration:<br>`lacework -p onboarding cloud-account list`<br><br>**Expected output summary:**<br>• **Name:** aws-agentless-scanning<br>• **Type:** AwsSidekick<br>• **Status:** Enabled<br>• **State:** Ok |
| **6** | Delete the deployment (destroy Terraform resources):<br>`terraform destroy` |

---
---  

### 🛡️ Verify from UI (After 24 hours) Vulnerability Tab filter:
<img width="1315" height="681" alt="Screenshot 2025-10-16 at 5 05 39 PM" src="https://github.com/user-attachments/assets/bf5fcd6a-6893-4e16-9286-5c6e216bc34c" />  

### or from the new Agentless Tab (Preview) 

<img width="1273" height="550" alt="Screenshot 2025-10-16 at 5 09 21 PM" src="https://github.com/user-attachments/assets/6d83ed97-93b4-466f-8301-374ab78e1fab" />

---
---  

## 🧩 What Is Deployed in a Workflow ?

### 🛡️ Private-by-Design: 


| Step | Description |
|------|--------------|
| **1** | The customer runs the **Agentless AWLS Terraform module** to deploy the required resources in their AWS environment. |
| **2** | Terraform template provisions:<br>• **IAM Roles / Global**<br>• **S3 Bucket /Global**<br>• **ECS Cluster /Region** (with *Sidekick* container)<br>• **VPC**, **Subnet**, and **Internet Gateway /Region**   |
| **3** | The **Sidekick container** is executed as part of an **ECS Fargate task**. |
| **4** | The task enumerates customer workloads, identifies attached block volumes, securely mounts them, and initiates the scanning process. |
| **5** | Scanning results are written to the customer’s **S3 bucket**. |
| **6** | **FortiCNAPP** reads metadata and scan results from the customer’s **S3 bucket** for further processing. |
| 🧹 **Automatic Cleanup** | The scanner periodically removes **old snapshots** and **stale scan tasks** to maintain efficiency. |
| ⏱️ **Scan Frequency** | By default, scans run **every 24 hours**. |
| 🔒 **Privacy-First Design** | **FortiCNAPP** has **no direct access** to customer workloads — it interacts only with the resources it deploys, using **limited IAM permissions**. |
| 🎯 **Selective Scanning** | You can limit the scanned hosts using an explicit **query filter**. By default, all workloads are scanned. |
| 🐳 **Powered by ECS** | *Amazon Elastic Container Service (Amazon ECS)* is a fully managed container orchestration service that simplifies deployment, scaling, and management of containerized applications. |

#### This creates an ECS cluster, a VPC and VPC IG for that cluster per region (Scanning account, or Security account, where the scanning infrasturcture is installed).
#### The trigger will start a periodic Task to snapshot and analyze EC2 volumes in that region (Monitored account where a role used to create snapshots, and access snapshot data, is installed).

---
---  

## 🔗 Reference Links

| Reference | Description |
|------------|--------------|
| [**Integrating Agentless Workload Scanning for AWS Single Account with Terraform**](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/983212/integrating-agentless-workload-scanning-for-aws-single-account-with-terraform) | Step-by-step guide for deploying Agentless Workload Scanning (AWLS) on a **single AWS account** using Terraform. |
| [**Integrating Agentless Workload Scanning for AWS Organization Account with Terraform**](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/864699/integrating-agentless-workload-scanning-for-aws-organization-account-with-terraform) | Instructions for setting up AWLS for an **AWS Organization (multi-account)** environment using Terraform. |
| [**Integrating Agentless Workload Scanning with AWS using Terraform**](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/744245/terraform) | General integration overview and Terraform usage guide for **Agentless Workload Scanning** on AWS. |
| [**Terraform Module for Lacework & AWS Agentless Scanning**](https://registry.terraform.io/modules/lacework/agentless-scanning/aws/latest) | Official **Terraform Registry** module for configuring an integration between **Lacework** and **AWS** for agentless workload scanning. |
| [**Supported Operating Systems (Linux & macOS)**](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/671486) | Lists **supported Linux distributions and macOS versions** for FortiCNAPP agent and agentless workload scanning. |
| [**Agentless Scanning for Windows**](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/838971/agentless-scanning-for-windows) | Details the **supported Windows operating systems** for agentless workload scanning. |
| [**Host OS and Language Library Support for Vulnerability Assessment**](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/999307/host-os-and-language-library-support-for-vulnerability-assessment#supported-linux-operating-systems-packages-and-language-libraries) | Reference list of **supported operating systems, packages, and language libraries** used in FortiCNAPP vulnerability assessments. |

