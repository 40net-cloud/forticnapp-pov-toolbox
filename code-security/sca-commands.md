📦 FortiCNAPP lacework sca scan — Full Flags Table

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
