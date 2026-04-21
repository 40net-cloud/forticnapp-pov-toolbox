## FortiCNAPP Local Code Security Scan (SCA, SAST, SBOM, Secrets, license-detection )
<br>


### 📘 Reference Links

| Topic | Documentation Link |
|--------|---------------------|
| **FortiCNAPP CLI Reference** | [https://docs.fortinet.com/document/forticnapp/latest/cli-reference/68020/get-started-with-the-lacework-forticnapp-cli) |
| **FortiCNAPP Requirements**  |  [https://docs.fortinet.com/document/forticnapp/latest/administration-guide/681609/requirements) |


                    

<br>

## FortiCNAPP Local SCA Scan — Simple Steps

| Step | Action | Command | Result |
|------|--------|---------|--------|
| 1 | Install CLI | `curl -sSL https://raw.githubusercontent.com/lacework/go-sdk/main/cli/install.sh \| bash` | CLI installed |
| 2 | Configure FortiCNAPP authentication | `lacework configure -a <account>.lacework.net -k <api_key> -s <api_secret>` | API Keys |
| 3 | Run local scan | `lacework sca scan .` | Findings shown in terminal |
| 4 | Export SARIF report | `lacework sca scan . -f sarif -o result.sarif` | SARIF file created |
| 5 | Upload results to FortiCNAPP UI | `lacework sca scan . --save-results` | Results uploaded to UI |
|   | Example | `lacework sca scan . -f lw-json -o test.json --save-results`  |

or Install CLI from:
Open a new PowerShell terminal to read the updated system PATH and use the FortiCNAPP CLI.

Homebrew (macOS/Linux)
brew install lacework/tap/lacework-cli
For more details, see the Lacework Homebrew Tap.

Chocolatey (Windows):
choco install lacework-cli
For more details, see the Lacework CLI Chocolatey package.
<br>

### FortiCNAPP lacework sca scan —  Addtional Flags Table (  `lacework sca scan` )

| Flag                   | Type        | Allowed Values                  | Default | Description                                          |
| ---------------------- | ----------- | ------------------------------- | ------- | ---------------------------------------------------- |
| `--acf`                | bool        | `true`, `false`                 | `false` | Enable Application Context Filtering                 |
| `--acf-locations`      | int         | any integer                     | `5`     | Number of code references per vulnerability          |
| `--acf-locations-full` | string list | package names or `name@version` | —       | Full references for selected packages                |
| `--basic-auth`         | string      | `username:password/token`       | —       | HTTPS authentication for git repo scanning           |
| `--basic-env-auth`     | bool        | `true`, `false`                 | `false` | Use environment variables for HTTPS auth             |
| `--exceptions`         | string list | CVE / CWE / path rules          | —       | Ignore specific vulnerabilities or paths             |
| `--exclude`            | string list | gitignore-style patterns        | —       | Exclude files/folders from scan                      |
| `-h, --help`           | flag        | —                               | —       | Show help                                            |
| `--license-detection`  | bool        | `true`, `false`                 | `true`  | Detect licenses in dependencies                      |
| `--lines-of-code`      | bool        | `true`, `false`                 | `true`  | Count lines of code                                  |
| `--sast`               | bool        | `true`, `false`                 | `true`  | Enable SAST analysis                                 |
| `--save-results`       | bool        | `true`, `false`                 | `false` | Upload results to FortiCNAPP UI (repo root required) |
| `--scr`                | bool        | `true`, `false`                 | `true`  | Include source code references                       |
| `--secret`             | bool        | `true`, `false`                 | `true*` | Enable secret scanning (*enabled when SAST is true*) |
| `--ssh-auth`           | string      | `path[:password]`               | —       | SSH private key authentication                       |
| `--ssh-env-auth`       | bool        | `true`, `false`                 | `false` | Use SSH key from environment variable                |
| `--vuln-evaluation`    | bool        | `true`, `false`                 | `true`  | Enable vulnerability evaluation                      |


🌍 Global Flags

| Flag            | Type        | Allowed Values                                                                   | Default     | Description                          |
| --------------- | ----------- | -------------------------------------------------------------------------------- | ----------- | ------------------------------------ |
| `--config`      | string      | file path                                                                        | auto-detect | Load `.lacework/codesec.yaml` config |
| `--deployment`  | string      | `ci`, `offprem`, `ide`, `local`                                                  | `local`     | Deployment environment type          |
| `-f, --formats` | string list | `sarif`, `lw-json`, `cdx-json`, `cdx-xml`, `spdx-*`, `md-summary`, `gitlab-json` | `lw-json`   | Output format(s)                     |
| `-j, --jobs`    | int         | any integer                                                                      | `10`        | Parallel scan jobs                   |
| `-o, --output`  | string      | file or directory path                                                           | —           | Output file location                 |
| `--quiet`       | bool        | `true`, `false`                                                                  | `false`     | Suppress console output              |




