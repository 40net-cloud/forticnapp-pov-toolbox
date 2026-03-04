






| Environment              | Image Builder              | Runtime             |
| ------------------------ | -------------------------- | ------------------- |
| Developer laptop         | Docker Build               | Docker              |
| CI/CD pipelines          | Docker / BuildKit / Kaniko | N/A (build only)    |
| Kubernetes cluster       | Kaniko / BuildKit          | containerd / CRI-O  |
| OpenShift                | Buildah / Podman           | CRI-O               |
| Enterprise Linux servers | Podman build               | Podman              |
| Cloud VM container host  | Docker / Buildah           | containerd / Docker |







FortiCNAPP provides the ability to assess, identify, and report vulnerabilities found on hosts, containers, and pods within your environment. 
This means you can identify and take action on software vulnerabilities in your environment and manage that risk proactively.

FortiCNAPP continuously assesses vulnerability risks, identifies OS packages, and correlates them with publicly known vulnerabilities 
with risk ratings by severity and CVSS scores

Host vulnerability scanning with FortiCNAPP can be performed using two different methods:

FortiCNAPP Agent for vulnerability scanning on:
Linux hosts, pods, and containers
Windows Server hosts
Agentless Workload Scanning for vulnerability scanning on Linux hosts, **WindowsServers**, pods, and containers.


- FortiCNAPP uses the following CVE Sources for language libraries when using **agentless workload scanning:**

Risk Based Security (RBS) - VulnDB
GitHub Security Advisory (GHSA)
GitLab Advisory Community
FortiCNAPP uses  National Vulnerability Database (NVD) for the severity and CVSS score associated with the CVEs. 
When an NVD CVSS score is not available for a given GitHub Security Advisory (GHSA) package, 
FortiCNAPP uses the CVSS score directly from GHSA for that package.


- FortiCNAPP uses the following CVE sources for Windows OS and applications:
Risk Based Security (RBS) - VulnDB
Microsoft Security Response Center (MSRC)
FortiCNAPP uses multiple CVE / vulnerability sources and will determine the best source for new and existing vulnerabilities.

When a CVSS score is not available, FortiCNAPP reports the value as N/A in the Console, and 0 in the CLI.
FortiCNAPP assigns severities to CVEs based on the following criteria in the following order of preference:

The operating system distribution vendor (such as CentOS, Ubuntu, Alpine, etc.) provides a severity.
Unlike operating system vendors, language library projects do not directly provide vulnerability data. As such, there is no equivalent "vendor" severity.


The FortiCNAPP platform ingests new CVEs daily from OS vendors and the NIST National Vulnerability Database (NVD).




the platform-scanner pulls the entire image to our backend for analysis. The Proxy and inline scanner will also pull the entire image and analyze it, 
but only send the manifest to the Lacework backend


For the on-demand button click
press the button the UI will send a message to our backend to pull and scan the image from the registry that is the origin from the container you select


for proxy-scanner
scanning happens on customer's side and results are sent to us, and evaluation happens on our side.




















https://docs.fortinet.com/document/forticnapp/latest/administration-guide/182307
AWLS - Host Vulnerability - Scanning of Language Libraries and Package Managers


Host OS and language library support for vulnerability assessment:
https://docs.fortinet.com/document/forticnapp/latest/administration-guide/999307
