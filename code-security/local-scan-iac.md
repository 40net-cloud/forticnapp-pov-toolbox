
## FortiCNAPP Local Code Security IAC 
<br>


### 📘 Reference Links

| Topic | Documentation Link |
|--------|---------------------|
| **FortiCNAPP CLI Reference** | [https://docs.fortinet.com/document/forticnapp/latest/cli-reference/68020/get-started-with-the-lacework-forticnapp-cli) |
| **FortiCNAPP Requirements**  |  [https://docs.fortinet.com/document/forticnapp/latest/administration-guide/274660/opal-overview) |
                    
<br>


### FortiCNAPP IaC Scan (OPAL) — Simple Guide
🔹 What is OPAL (IaC scanning)
OPAL is FortiCNAPP’s IaC static analyzer
It scans Terraform, Kubernetes, CloudFormation, etc.
It uses OPA + Rego policies to detect misconfigurations before deploymen


### FortiCNAPP IaC Scan (OPAL) — Simple Steps
| Step | Action | Command | Result |
|------|--------|---------|--------|
| 1 | Install FortiCNAPP CLI | `curl -sSL https://raw.githubusercontent.com/lacework/go-sdk/main/cli/install.sh \| bash` | CLI installed |
| 2 | Configure authentication | `lacework configure -a <account>.lacework.net -k <api_key> -s <api_secret>` | CLI authenticated |
| 3 | Install IaC component | `lacework component install iac` | OPAL enabled |
| 4 | Prepare IaC code | (Terraform / YAML / JSON files) | IaC files ready |
| 5 | Run IaC scan | `lacework iac scan .` | Findings in terminal |
| 6 | Export report (optional) | `lacework iac scan . -f json -o result.json` | JSON report |
| 7 | Use in CI/CD | (GitHub / Jenkins / etc.) | Shift-left IaC security |
