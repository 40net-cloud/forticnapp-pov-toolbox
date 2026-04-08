
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

<br>

### FortiCNAPP IaC Scan (OPAL) — Simple Steps
| Step | Action | Command | Result |
|------|--------|---------|--------|
| 1 | Install FortiCNAPP CLI | `curl -sSL https://raw.githubusercontent.com/lacework/go-sdk/main/cli/install.sh \| bash` | CLI installed |
| 2 | Configure authentication | `lacework configure -a <account>.lacework.net -k <api_key> -s <api_secret>` | CLI authenticated |
| 3 | Install IaC component | `lacework component install iac` | OPAL engine enabled |
| 4 | Prepare IaC code | (Terraform / YAML / JSON files) | IaC files ready |
| 5 | Run IaC scan | `lacework iac scan -d .` | Findings displayed in terminal |
| 6 | Export report (optional) | `lacework iac scan -d . --format json --save-result result.json` | JSON report generated |
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
