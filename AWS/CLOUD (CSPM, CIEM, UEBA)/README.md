

### 🧱 FortiCNAPP Terraform Deployment Options

| **Deployment Method** | **Description** | **Supported Capabilities** |
|------------------------|-----------------|-----------------------------|
| ⚡ **Automated Configuration** | Deploy FortiCNAPP using a **prebuilt Terraform automation flow** that provisions all required resources automatically in a **single AWS region**.<br><br>🔑 *Note:* Requires **temporary credentials** (AWS Access Key ID & Secret Access Key) for your AWS account. | ✅&nbsp;Single&nbsp;AWS&nbsp;Account <br>✅&nbsp;Cloud&nbsp;Config&nbsp;&amp;&nbsp;Audit&nbsp;Logs <br>✅&nbsp;Agentless&nbsp;Workload&nbsp;Scanning |
| <br> | <br> | <br> |
| 🧭 **Terraform via Guided Configuration (UI)** | Deploy and manage FortiCNAPP integrations through the **FortiCNAPP Web Console**.<br><br>Provides a **wizard-based experience** for onboarding and connecting AWS environments without direct CLI interaction. | ✅&nbsp;Single&nbsp;&amp;&nbsp;Multiple&nbsp;AWS&nbsp;Accounts <br>✅&nbsp;Cloud&nbsp;Config&nbsp;&amp;&nbsp;Audit&nbsp;Logs <br>✅&nbsp;EKS&nbsp;Audit&nbsp;Logs |
| <br> | <br> | <br> |
| ⚙️ **Terraform via FortiCNAPP CLI** | Command-line–driven automation using the **open-source FortiCNAPP CLI** (written in Go).<br><br>Ideal for **organization-wide**, **multi-account**, or **DevOps-integrated** deployments. | ✅&nbsp;AWS&nbsp;Organization-level&nbsp;Access <br>✅&nbsp;Single&nbsp;&amp;&nbsp;Multiple&nbsp;AWS&nbsp;Accounts <br>✅&nbsp;Cloud&nbsp;Config&nbsp;&amp;&nbsp;Audit&nbsp;Logs <br>✅&nbsp;EKS&nbsp;Audit&nbsp;Logs <br>✅&nbsp;Agentless&nbsp;Workload&nbsp;Scanning |





### ☁️ AWS & FortiCNAPP Terraform Prerequisites

| **Component / Requirement** | **Description** | **Reference / Link** |
|------------------------------|-----------------|----------------------|
| 🧑‍💻 **AWS Account Admin** | Administrative privileges on each AWS account.<br>Required during onboarding process only. | — |
| 🔧 **AWS CLI** | Install and configure the AWS CLI to connect to your AWS Account. | [AWS CLI Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) |
| 🧰 **Linux Tools** | Ensure basic tools (`curl`, `git`, `unzip`) are available in the system `PATH`. | — |
| ⚙️ **Terraform** | Install Terraform if not already configured. | [Terraform Documentation](https://developer.hashicorp.com/terraform) |
| 🧠 **FortiCNAPP CLI** | Open-source CLI tool written in Golang. Available for **Linux**, **macOS**, and **Windows**.<br>Used to interact with FortiCNAPP via command line. | [FortiCNAPP CLI Guide](https://docs.fortinet.com/document/forticnapp/latest/cli-reference/68020/get-started-with-the-lacework-forticnapp-cli) |
| ⚡ **Deployment Methods** | Supported installation environments and automation options:<br>• **AWS Cloud Shell**<br>• **Hosts Supported by Terraform** | — |



### ☁️ AWS Prerequisites for FortiCNAPP Integration

| **Component** | **Description** | **FortiCNAPP Usage / Notes** |
|----------------|-----------------|-------------------------------|
| 📨 **SNS Topic** | An **Amazon Simple Notification Service (SNS)** topic is a logical access point that acts as a communication channel, grouping multiple endpoints such as AWS, Amazon SQS, HTTP/S, or email addresses. | Required for **all CloudTrail integrations**.<br>FortiCNAPP can use an **existing SNS topic** or create one automatically if not present. |
| 📬 **SQS Queue** | **Amazon Simple Queue Service (SQS)** enables distributed applications to exchange messages asynchronously. SNS and SQS together deliver notifications immediately while persisting messages for later processing. | Required for **all CloudTrail integrations**.<br>Used alongside SNS to deliver CloudTrail events to FortiCNAPP. |
| 🗃️ **S3 Bucket** | An **Amazon S3 bucket** is a container for objects. CloudTrail stores log files in S3 buckets. | Required for **all CloudTrail integrations**.<br>FortiCNAPP can use an existing S3 bucket or create one in the designated AWS account. |
| ☁️ **CloudTrail** | **AWS CloudTrail** records user, role, or service actions across your AWS account for governance, compliance, and audit purposes. | Required to capture and deliver event logs to FortiCNAPP.<br>FortiCNAPP can use an **existing CloudTrail** or create a new one. |
| 🔐 **IAM Cross-Account Role** | An **IAM cross-account role** grants FortiCNAPP access to AWS resources for configuration assessment and CloudTrail event analysis. | Required for **read-only access**.<br>Includes two policies:<br>• **FortiCNAPP custom audit policy** – read-only access to configuration resources.<br>• **FortiCNAPP custom IAM policy** – read-only access to ingest CloudTrail logs. |
| ⚠️ **Important Note** | Ensure your **IAM cross-account role** and **S3 bucket** are created in the **same AWS account** — regardless of setup method (manual, CloudFormation, or Terraform). | This is due to **legacy AWS access control rules**. Cross-account access alone is **not sufficient** to bypass these S3 restrictions. |

---

> 💡 **Architecture Summary:**  
> These AWS components work together to securely deliver CloudTrail audit data and configuration information to **FortiCNAPP**, enabling continuous compliance, visibility, and threat detection across your cloud environment.
