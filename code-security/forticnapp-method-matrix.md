
## This Section will discuss FortiCNAPP Application Code Security:

```bash
https://docs.fortinet.com/document/forticnapp/latest/administration-guide/957505/integration-and-feature-matrix
```


## 🛡️ FortiCNAPP Capabilities Overview

| Capability | Description |
|-----------|------------|
| **SAST** (Static Application Security Testing) | Analyzes source code to identify security weaknesses and coding flaws during development. |
| **SCA** (Software Composition Analysis) | Identifies vulnerabilities in third-party libraries and dependencies used in the application. |
| **SmartFix** | Provides intelligent, actionable remediation recommendations for vulnerabilities, including fixes that can resolve multiple issues across dependencies. |
| **SBOM** (Software Bill of Materials) | Generates a complete inventory of all components (libraries, versions, licenses) used in the application. |
| **Secrets Scanning** | Detects exposed secrets such as API keys, tokens, and credentials within the codebase. |
| **License Compliance** | Ensures all third-party libraries comply with organizational and legal licensing requirements. |

---

### 🧠 SCA (SmartFix (Advanced Remediation Engine))

- Recommends **practical and prioritized fixes** for identified vulnerabilities  
- Can **resolve multiple vulnerabilities with a single upgrade or change**  
- Helps reduce remediation effort and improve efficiency across dependency management  


## 🧠 Code Security (SCA/SAST/SBOM) — Deployment Matrix

For Detailed Updated Matrix: 
```bash
https://docs.fortinet.com/document/forticnapp/latest/administration-guide/957505/integration-and-feature-matrix
```

| Feature ↓ \ Mode →                 | SCM Integration (SaaS repos)                                                       | CI/CD Pipeline                                                                               | Local (CLI on dev machine)                             | IDE Extension                                              | **Self-Hosted SCM (With Internet Connection)**                                                                                     | **Self-Hosted SCM (No Internet Connection)**                                             |
| ---------------------------------- | ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------ | ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **What runs**                      | SCA, SAST, Secrets                                                                 | SCA, SAST, Secrets, SBOM (optional)                                                          | SCA, SAST, Secrets                                     | SCA, SAST, Secrets (per IDE support)                       | SCA, SAST, Secrets (via CI/CD job or CLI)                                                                                          | ❌ Not possible                                                                           |
| **Where analysis runs**            | SaaS backend (after repo connect)                                                  | CI runner/agent                                                                              | Dev workstation / dev container                        | In-IDE + SaaS services                                     | CI runner/agent inside your network (with outbound HTTPS to FortiCNAPP)                                                            | ❌ No analysis possible (CLI/agents require FortiCNAPP auth via internet)                 |
| **How you deploy**                 | Connect GitHub / GitLab / Bitbucket in **Code security → Integrate code scanning** | Add job/step that runs CLI (`lacework sca scan <dir> --save-results --deployment=ci`)        | Run CLI on repo (`lacework sca scan . --save-results`) | Install Lacework Code Security VS Code extension & sign in | Use CI/CD runner (GHES Actions runner, Jenkins, GitLab CI, etc.) with CLI scan job; requires outbound HTTPS/proxy                  | ❌ Not possible (cannot install/authenticate CLI without internet)                        |
| **What is uploaded**               | Findings + metadata (per policy)                                                   | Results JSON (+ optional SBOM); source stays in CI                                           | Nothing unless `--save-results`                        | Findings linked to project/repo                            | Same as CI/CD → JSON (+ SBOM) uploaded if runner has HTTPS egress                                                                  | ❌ Nothing (no connectivity to upload results)                                            |
| **Typical triggers**               | On PRs, on push, scheduled                                                         | On PR/merge/build                                                                            | On demand (pre-commit / before PR)                     | On save / on demand in IDE                                 | On PR/merge/build (runner controlled)                                                                                              | ❌ None                                                                                   |
| **Saved to UI**                    | Repositories / Violations (PR checks)                                              | Pipelines / Violations (+ CI logs)                                                           | CLI output + UI if saved                               | IDE panel + UI (linked results)                            | Pipelines / Violations (+ CI logs)                                                                                                 | ❌ Not supported                                                                          |
| **Supported integrations / tools** | **Git providers:** GitHub, GitLab, Bitbucket                                       | **CI systems:** GitHub Actions, GitLab CI, Azure DevOps, Jenkins (beta), Bitbucket Pipelines | **OS:** Linux, macOS, Windows (CLI)                    | **IDE:** Visual Studio Code & Cursor                               | **SCM:** GitHub Enterprise Server, GitLab Self-Managed, Bitbucket Server. **CI/CD:** self-hosted runners/agents with HTTPS/proxy   | ❌ None                                                                                   |
| **Support status**                 | ✅ Supported                                                                        | ✅ Supported                                                                                  | ✅ Supported                                            | ✅ Supported                                                | ⚠️ Supported (works if internet connection + FortiCNAPP account; check all SCM/CI versions  tested)              | ❌ Not supported                                                                          |
| **Air-gapped / Offline Mode**      | ❌ Not applicable                                                                   | ❌ Not supported (no upload to UI)                                                            | ⚠️ CLI can generate JSON/SBOM locally but not uploaded | ❌ Not supported (extension requires SaaS login)            | ⚠️ CLI/CI can generate JSON/SBOM locally but upload requires internet; results won’t reach FortiCNAPP UI without outbound internet | ❌ Not possible (air-gapped SCMs cannot authenticate CLI or upload results to FortiCNAPP) |
