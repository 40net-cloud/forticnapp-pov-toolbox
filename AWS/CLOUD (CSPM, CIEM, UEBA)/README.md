### ☁️ AWS & FortiCNAPP Terraform Prerequisites

| **Component / Requirement** | **Description** | **Reference / Link** |
|------------------------------|-----------------|----------------------|
| 🧑‍💻 **AWS Account Admin** | Administrative privileges on each AWS account.<br>Required during onboarding process only. | — |
| 🔧 **AWS CLI** | Install and configure the AWS CLI to connect to your AWS Account. | [AWS CLI Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) |
| 🧰 **Linux Tools** | Ensure basic tools (`curl`, `git`, `unzip`) are available in the system `PATH`. | — |
| ⚙️ **Terraform** | Install Terraform if not already configured. | [Terraform Documentation](https://developer.hashicorp.com/terraform) |
| 🧠 **FortiCNAPP CLI** | Open-source CLI tool written in Golang. Available for **Linux**, **macOS**, and **Windows**.<br>Used to interact with FortiCNAPP via command line. | [FortiCNAPP CLI Guide](https://docs.fortinet.com/document/forticnapp/latest/cli-reference/68020/get-started-with-the-lacework-forticnapp-cli) |
| ⚡ **Deployment Methods** | Supported installation environments and automation options:<br>• **AWS Cloud Shell**<br>• **Hosts Supported by Terraform** | — |


### 🧱 FortiCNAPP Terraform Deployment Options

| **Deployment Method** | **Description** | **Supported Capabilities** |
|------------------------|-----------------|-----------------------------|
| 🧭 **Terraform via Guided Configuration (UI)** | Deploy and manage FortiCNAPP integrations through the **FortiCNAPP Web Console**. Provides a user-friendly, wizard-based experience for onboarding and connecting AWS environments. | ✅ **Single & Multiple AWS Accounts** <br>✅ **Cloud Audit Logs** <br>✅ **EKS Audit Logs** |
| ⚙️ **Terraform via FortiCNAPP CLI** | Command-line–driven automation using the **open-source FortiCNAPP CLI** (written in Go). Ideal for large-scale, organization-wide deployments or DevOps automation. | ✅ **AWS Organization-level Access** <br>✅ **Cloud Audit Logs** <br>✅ **EKS Audit Logs** <br>✅ **Agentless Workload Scanning** |
