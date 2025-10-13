# Deploying FortiCNAPP Window Server Agent using Lacework PowerShell Script 

 Windows agent provides threat detection, file and Windows registry integrity monitoring, vulnerability detection, and host-based intrusion detection for your cloud or on-premise Windows Server operating system (OS)-based workloads.
After you install the agent, the agent and Lacework FortiCNAPP server communicate with each other. The agent scans your host and securely forwards select metadata to the server to build a baseline of normal behavior. From this, Lacework FortiCNAPP provides alerts for anomalous behavior.


#### Windows Agent System & Deployment Requirements

| **Category** | **Requirement / Details** |
|---------------|----------------------------|
| **Operating System Requirements** | - Must support **Transport Layer Security (TLS) 1.2**.<br>- **Do NOT install** on personal or consumer Windows editions (e.g., Windows 10/11 Home, Pro, etc.).<br>- Recommended: **Windows Server 2012 R2**, **2016**, **2019**, **2022**. |
| **Software Prerequisites** | - **PowerShell 5.0 or later**.<br>Check version: <br>`$PSVersionTable.PSVersion` |
| **Hardware Requirements & Usage** | - **CPU:** 2-core processor.<br>- **Memory (RAM):** 4 GB minimum.<br>- **Agent Average CPU Usage:** Less than **10%** (typically much lower).<br>- **Agent Memory Usage:** Less than **200 MB** (typically much lower). |
| **Performance Notes** | The agent runs as a lightweight background service and typically consumes minimal CPU and memory resources. |
| **Deployment Recommendations** | - Ensure servers meet minimum hardware and OS requirements before installation.<br>- Verify network and security configurations support outbound TLS 1.2 traffic.<br>- Maintain PowerShell and Windows updates for stability and compatibility. |

---
#### ✅ Deployment using Lacework PowerShell Script Fil Flow:
Fits All Clouds: Install the Windows Agent on Hosts Using Lacework PowerShell Script, Quick Easy installion method on few machines during Lab/POC.
There are many other methods as above, but this can fit a quick easy way for this kind of deployments if there are few machines and multicloud deployments.

```bash
Deployment using Lacework PowerShell Script Flow
├ 1. Create New Access Token. 
├ 2. Download/Install Using Lacework PowerShell Script via FortiCNAPP Console.
├ 3. Deployment using Lacework PowerShell Script  without a Configuration File.
├ 4. Verify.
✅ Reference Links
```
#### ✅ 1. Create New Access Token:

- Lacework FortiCNAPP Console, go to Settings > Configuration > Agent Tokens.
- Add Name and Description.
- Select Windows as the Operating System.
- Click Save to create your new access token for Windows agent.
  
* Note: An access token can be re-used for multiple agent installations.

#### ✅ 2. Download/Install Using Lacework PowerShell Script via FortiCNAPP Console:
 In the Lacework FortiCNAPP Console, go to Settings > Configuration > Agent Tokens.
- Select = the Windows access token created and that you want to use for your agent installation.
- Click the Install tab.
- Click  installation method, Lacework PowerShell Script:
- Do either of the following:
  - Click Download script to download the file (powershell.zip file).
  - Unzip "powershell.zip" and you get 3 files (Azure-Deploy-LW-Win.ps1, Install-LWDataCollector.ps1 & lwminisign.exe).
<img width="434" height="103" alt="Screenshot 2025-07-30 at 1 43 34 PM" src="https://github.com/user-attachments/assets/01b0b44c-b2e1-4a39-84ef-240a22070ea4" />

#### ✅ 3. Deployment using Lacework PowerShell Script:
Instead of specifying configuration parameters for the agent installation in a config.json file, you can specify them directly in the command line:

 - 1. Open PowerShell terminal as an administrator.
 - 2. Navigate to the directory containing the Install-LWDataCollector.ps1 script on your host.
 - 3. Run the script using the following command in the PowerShell command line, C:\Users\Administrator>:
```bash
.\Install-LWDataCollector.ps1 -MSIURL Agent_MSI_Download_URL -AccessToken Your_Access_Token -ServerURL Your_API_Endpoint -Defender

```
Example for Windows Agent Release 1.7.2:
```bash
.\Install-LWDataCollector.ps1 -MSIURL https://updates.lacework.net/win-1.7.2.3973-2023-11-05-release-1.7.0-cc74651519014fec0f7502858b06895a4cf0d802/LWDataCollector.msi  -AccessToken b2fxxxxxx -ServerURL https://lwxx-eu.lacework.net  -Defender
```

Where:
Your_Access_Token:  Specifies your agent access token. Token Details under Agent Token (example: b2fe1bb5axxxxx). Step.1.
Your_API_Endpoint: Specifies your Lacework FortiCNAPP agent server URL. (example: https://xx-eu.lacework.net )
-Defender option: Excludes the Windows agent from scanning with Windows Defender.
Agent_MSI_Download_URL: Copy the URL for Lacework Windows Agent MSI Package from:
```bash
https://github.com/lacework/lacework-windows-agent-releases/releases
```
A config.json file  that contains the options you specified in the command line is created in the C:\ProgramData\Lacework\ directory. 
You can modify this file to change the settings for the agent. If you modify the file, you must restart the agent for the changes to take effect. For more information, see Restart the Windows Agent.

#### ✅ 3. Deployment using Lacework PowerShell Script (with Proxy settings) :

To configure the agent to use a specific proxy during installation in the command line, use the following command:C:\Users\Administrator>  
```bash
msiexec.exe /i LWDataCollector.msi ACCESSTOKEN=Your_Access_Token SERVERURL=Your_API_Endpoint PROXYURL=http://Your_Proxy_Server:Your_Port
```
- Where Your_Proxy_Server is the URL or IP address of your HTTP proxy server and Your_Port is the port number of your proxy server.

If the agent should not use a proxy, regardless of the machine’s configuration, use the following command during installation:

#### ✅ 4. Verify, Restart, Troubleshoot: C:\Users\Administrator>

Enter the following command to check status for the lwdatacollector service: 
- In Powersehll:
```bash
sc.exe query lwdatacollector
```
or
- In Command Prompt
```bash
sc query lwdatacollector
```

Stop the window agent with the following command:  

```bash
sc.exe stop lwdatacollector
```

Restart the window agent with the following command:  

```bash
sc.exe start lwdatacollector
```

Unistall the window agent with the following powershell command:  
 - Do not downgrade to an earlier version of the agent. Downgrading can cause data incompatibility.

```bash
## Script to uninstall the Lacework Windows agent
$app = Get-WmiObject -Class Win32_Product -Filter "Name like '%Lacework%'"
$app.Uninstall()
```

### ✅ Reference Links

| **Topic** | **Description** | **Link** |
|------------|-----------------|----------|
| 🛡️ **Windows Agent Overview & System Requirements** | Detailed documentation on agent architecture, supported OS versions, and system requirements. | [View Docs](https://docs.fortinet.com/document/lacework-forticnapp/latest/administration-guide/662064/windows-agent-overview-and-system-requirements) |
| 🛡️ **Windows Agent Installer Methods** | Guide to downloading and installing the Windows Agent using standard installer packages. | [View Docs](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/1455/downloading-the-windows-agent-installer) |
| 🛡️ **Windows Agent PowerShell Installation** | Step-by-step guide for installing the agent using a PowerShell script. | [View Docs](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/169764/installing-the-windows-agent-using-a-powershell-script) |
| 🛡️ **Windows Agent Installation Prerequisites** | Lists prerequisites and dependencies before deploying the Windows Agent. | [View Docs](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/902600/windows-agent-installation-prerequisites) |
| 🛡️ **Network Proxy Configuration for Windows Agent Traffic** | Explains how to configure a proxy for Windows Agent network communications. | [View Docs](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/558949/use-a-network-proxy-for-windows-agent-traffic) |


---

### ✅ Just a Side Note: Other Installation Methods for Windows Servers Supported

| **Environment / Cloud** | **Installation Method** | **Notes** |
|--------------------------|--------------------------|------------|
| **All Clouds** | **Lacework PowerShell Script** | Full guided installation method (refer to the provided setup file). |
| **All Clouds** | **MSI Package Deployment** | Supported if the Windows VM is **domain-joined** or **centrally managed**. Suitable for **mass deployment** via **GPO**, **SCCM**, or **Intune**. |
| **Azure Specific** | **PowerShell Script for Azure VMs** | Installs the Windows Agent directly on Azure VMs within an Azure Resource Group. |
| **Azure Specific** | **Azure Resource Manager (ARM)** | Deploys the agent through **ARM templates** for integrated infrastructure management. |
| **Azure Specific** | **Terraform** | Automates deployment of the Windows Agent on Azure VMs using **Terraform IaC scripts**. |
| **AWS Specific** | **Packer** | Builds AMIs with the Windows Agent pre-installed for AWS EC2 instances. |
| **EKS & AKS Specific** | **Helm Chart** | Deploys the agent on **Kubernetes clusters (EKS/AKS)** via Helm for containerized monitoring. |

---
