
## FortiCNAPP Local Code Security IAC 
<br>


### 📘 Reference Links

| Topic | Documentation Link |
|--------|---------------------|
| **FortiCNAPP CLI Reference** | [https://docs.fortinet.com/document/forticnapp/latest/cli-reference/68020/get-started-with-the-lacework-forticnapp-cli) |
| **FortiCNAPP Requirements**  |  [https://docs.fortinet.com/document/forticnapp/latest/administration-guide/274660/opal-overview) |
                    
<br>

### FortiCNAPP IaC Scan (OPAL) — Simple Guide
OPAL is FortiCNAPP’s IaC static analyzer
It scans Terraform, Kubernetes, CloudFormation, etc.
It uses OPA + Rego policies to detect misconfigurations before deploymen

| Component | Description | Requirement | Behavior |
|-----------|------------|------------|----------|
| OPAL | Native FortiCNAPP IaC scanner (OPA/Rego-based) | No Docker required | Always runs and provides baseline results |
| Checkov | Extended IaC scanner (Bridgecrew) for deeper cloud and Kubernetes checks | Requires Docker | Skipped if Docker is not running |
| tfsec | Terraform-specific security scanner | Requires Terraform files (`.tf`) | Runs only when Terraform code is detected |

<br>


### Upload Results to FortiCNAPP UI: Local Scan configuration variables: 
  * Required variables (Linux/macOS) based on Pipeline structure in UI, follwoing is example, choose variables that fit yours, works w/o Git repository context:

For *Linux/macOS*:
```bash
export CI_PIPELINE_NAME="Github Pipeline"
export CI_BUILD_ID="CLI Build"
export CI_BUILD_URL="https://github.com/hkebbi/IDEs"
export CI_PIPELINE_URL="https://github.com/hkebbi/IDEs"
export CI_PLATFORM=CLI
```

*You can make CI Build_ID Dynamic*:

```bash
export CI_PIPELINE_NAME="Github-2 Pipeline"
export CI_BUILD_ID="Build_$(date +%Y%m%d_%H%M%S)"
export CI_BUILD_URL="https://github.com/hkebbi/IDEs"
export CI_PIPELINE_URL="https://github.com/hkebbi/IDEs"
export CI_PLATFORM="CLI"
```


*For Windows CMD*:
```bash
set CI_PIPELINE_NAME=Github Pipeline
set CI_BUILD_ID=CLI Build
set CI_BUILD_URL=https://github.com/hkebbi/IDEs
set CI_PIPELINE_URL=https://github.com/hkebbi/IDEs
set CI_PLATFORM=CLI
```

*For Windows PowerShell*:
```bash
$env:CI_PIPELINE_NAME="Github Pipeline"
$env:CI_BUILD_ID="CLI Build"
$env:CI_BUILD_URL="https://github.com/hkebbi/IDEs"
$env:CI_PIPELINE_URL="https://github.com/hkebbi/IDEs"
$env:CI_PLATFORM="CLI"
```


### Different example deployements: 
#### Scan current directory and Upload Results to FortiCNAPP UI:
  * --upload value to upload to UI is True by default, you can still add in command:
    
```bash
lacework iac scan -d .
```

#### Scan local folder (Save results locally in same folder with .json format) and upload to FortiCNAPP UI  

```bash
lacework iac scan -d . --upload=true --format json --save-result result.json
```

#### Scan local directory (Save results locally in same folder with .json format) and upload to FortiCNAPP UI 

```bash
lacework iac scan -d /Users/xx/Desktop/scan-iac --format json --save-result /Users/xx/Desktop/scan-iac/result.json
```

<img width="1284" height="444" alt="Screenshot 2026-05-19 at 10 13 47 PM" src="https://github.com/user-attachments/assets/eacfe7c3-fb93-4efb-b701-9d49112c976e" />


<img width="1322" height="659" alt="Screenshot 2026-05-19 at 10 14 16 PM" src="https://github.com/user-attachments/assets/eacada48-65f9-4fe5-a77b-de9ce5124e87" />






### FortiCNAPP IaC Scan (OPAL) — Simple Steps
| Step | Action | Command | Result |
|------|--------|---------|--------|
| 1 | Install FortiCNAPP CLI | `curl -sSL https://raw.githubusercontent.com/lacework/go-sdk/main/cli/install.sh \| bash` | CLI installed |
| 2 | Configure authentication | `lacework configure -a <account>.lacework.net -k <api_key> -s <api_secret>` | CLI authenticated |
| 3 | Install IaC component | `lacework component install iac` | OPAL engine enabled |
| 4 | Prepare IaC code | (Terraform / YAML / JSON files) | IaC files ready |
| 5 | Run IaC scan | `lacework iac scan -d .` | Findings displayed in terminal |
| 6 | Export report (optional) | `lacework iac scan -d . --format json --save-result result.json` | json report generated |
| 7 | Upload results to FortiCNAPP (optional) | `lacework iac scan -d . --upload` | Results available in FortiCNAPP UI |
| 8 | Use in CI/CD | (GitHub / Jenkins / etc.) | Shift-left IaC security |





<br>

| Flag | Shorthand | Type | Default | Allowed Values | Description |
|------|-----------|------|---------|----------------|-------------|
| `--directory` | `-d` | string | `.` | path | Directory containing IaC files to scan |
| `--format` | — | string | `table` | `yaml`, `json`, `csv`, `table`, `none` | Output format |
| `--save-result` | — | string | — | file path | Save scan result to JSON file |
| `--upload` | — | bool | `true` | `true`, `false` | Upload results to FortiCNAPP |
| `--custom-policy-dir` | — | string | — | path | Directory with custom Rego policies |
| `--disable-docker` | — | bool | `false` | `true`, `false` | Disable Docker-based scanning |
| `--disable-tls-verify` | — | bool | `false` | `true`, `false` | Disable TLS verification |
| `--git-base-ref` | — | string | — | git ref | Compare scan results with another branch/reference |
| `--help` | `-h` | flag | — | — | Show help |
