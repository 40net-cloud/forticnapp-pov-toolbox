
https://docs.fortinet.com/document/forticnapp/latest/cli-reference/68020/get-started-with-the-lacework-forticnapp-cli

# FortiCNAPP Local SCA Scan — Simple Guide

| Step | Action | Command | Result |
|------|--------|---------|--------|
| 1 | Install CLI | `curl -sSL https://raw.githubusercontent.com/lacework/go-sdk/main/cli/install.sh \| bash` | CLI installed |
| 2 | Configure authentication | `lacework configure -a <account>.lacework.net -k <api_key> -s <api_secret>` | CLI authenticated |
| 3 | Run local scan | `lacework sca scan .` | Findings shown in terminal |
| 4 | Export SARIF report | `lacework sca scan . -f sarif -o result.sarif` | SARIF file created |
| 5 | Upload results to FortiCNAPP UI | `lacework sca scan . --save-results` | Results uploaded to UI |


### 📘 Reference Links

| Topic | Documentation Link |
|--------|---------------------|
| **Azure Integration – Guided Configuration** | [https://docs.fortinet.com/document/forticnapp/latest/cli-reference/68020/get-started-with-the-lacework-forticnapp-cli) |
