
🧠 Rule (GitHub Actions)


---

# 🔁  Rule (GitHub Actions)
```markdown
## 🔁 GitHub Actions Structure

```text
repo-root/
│
├── .github/workflows/        ← REQUIRED location
│       └── workflow.yml
│
└── cicd/vuln-java-lab/       ← your application (working directory)

```
# vuln-java-lab


| File                      | Main purpose                                                  |
| ------------------------- | ------------------------------------------------------------- |
| `pom.xml`                 | SCA, SBOM, license data                                       |
| `App.java`                | basic Java structure                                          |
| `LoginController.java`    | hardcoded secrets, weak randomness                            |
| `UnsafeQueryService.java` | SQL injection, command injection, weak crypto, unsafe parsing |
| `application.properties`  | config secrets and insecure settings                          |
| `fake-secrets.txt`        | strong secret-detection results                               |



## 🧠 GitHub Actions Master Reference Table


| Component                 | Mandatory?                         | What it is (Simple)      | Why GitHub requires it               | Mental Model (How to think about it) | Used later in your pipeline |
| ------------------------- | ---------------------------------- | ------------------------ | ------------------------------------ | ------------------------------------ | --------------------------- |
| `.github/workflows/*.yml` | ✔ YES                              | Workflow file location   | GitHub only scans this folder        | “Where pipeline is defined”          | ALL stages                  |
| Valid YAML syntax         | ✔ YES                              | Proper YAML format       | GitHub must parse it                 | “Code must compile”                  | ALL                         |
| `name`                    | ❌ No                               | Workflow label           | For UI readability                   | “Label of pipeline”                  | ALL                         |
| `on`                      | ✔ YES                              | Trigger definition       | Workflow must know when to run       | “WHEN should this start?”            | PR, push, deploy            |
| `push`                    | ❌ No                               | Trigger on code push     | Event-driven automation              | “Code changed → run”                 | main scan, build, deploy    |
| `pull_request`            | ❌ No                               | Trigger on PR events     | Pre-merge validation                 | “Before merge check”                 | SCA/SAST PR                 |
| `schedule`                | ❌ No                               | Time-based trigger       | Continuous security checks           | “Run even if no changes”             | daily scans                 |
| `workflow_dispatch`       | ❌ No                               | Manual trigger           | On-demand execution                  | “Run now button”                     | debugging, manual deploy    |
| `jobs`                    | ✔ YES                              | Container of work        | Workflow must define tasks           | “WHAT work exists?”                  | ALL                         |
| At least one job          | ✔ YES                              | Minimum execution unit   | Otherwise nothing runs               | “Pipeline must do something”         | ALL                         |
| Job ID (`run-analysis`)   | ✔ YES                              | Job name identifier      | Required for structure               | “Name of stage”                      | ALL                         |
| `runs-on`                 | ✔ YES                              | Runner machine           | GitHub must allocate compute         | “WHERE does it run?”                 | ALL                         |
| `steps`                   | ✔ YES                              | Ordered actions          | Job must contain execution           | “WHAT to do step by step?”           | ALL                         |
| Step `name`               | ❌ No                               | Step label               | Readability/debugging                | “What is this step doing?”           | ALL                         |
| `uses`                    | ❌ No                               | External action          | Reuse prebuilt logic                 | “Use ready-made tool”                | checkout, FortiCNAPP        |
| `run`                     | ❌ No                               | Shell command            | Custom execution                     | “Run my own command”                 | docker, kubectl             |
| `with`                    | ❌ No (depends)                     | Action inputs            | Configure action behavior            | “Pass settings to tool”              | `target: push`, login       |
| `env`                     | ❌ No (but common)                  | Environment variables    | Centralized config                   | “Shared variables”                   | secrets, configs            |
| `secrets.*`               | ❌ No (but required for secure ops) | Secure values            | Avoid hardcoding secrets             | “Hidden sensitive data”              | API keys, passwords         |
| `permissions`             | ❌ No (recommended)                 | Token access control     | Security principle (least privilege) | “What can this workflow do?”         | PR comments, SARIF          |
| `needs`                   | ❌ No                               | Job dependency           | Control execution order              | “Wait for previous stage”            | build → scan → deploy       |
| `if`                      | ❌ No                               | Conditional logic        | Flexible execution                   | “Run only if condition met”          | deploy only on main         |
| `strategy`                | ❌ No                               | Matrix execution         | Run variations                       | “Repeat with different inputs”       | PR old/new comparison       |
| `outputs`                 | ❌ No                               | Pass values between jobs | Data sharing                         | “Send result to next stage”          | image tags                  |
| `timeout-minutes`         | ❌ No                               | Max runtime              | Prevent hanging jobs                 | “Kill stuck processes”               | scans                       |
| `continue-on-error`       | ❌ No                               | Ignore failure           | Non-blocking checks                  | “Don’t break pipeline”               | optional scans              |
| `working-directory`       | ❌ No                               | Subfolder execution      | Support monorepos                    | “Run inside folder”                  | app/k8s dirs                |
| `shell`                   | ❌ No                               | Command interpreter      | Control execution env                | “Use bash/powershell”                | OS-specific                 |
| `artifacts` (pattern)     | ❌ No                               | Save files               | Preserve outputs                     | “Keep reports”                       | SARIF, logs                 |
| `concurrency`             | ❌ No                               | Limit parallel runs      | Avoid conflicts                      | “Only one deploy at a time”          | deploy stage                |


## 🧠 GitHub Actions Execution Flow

```text
Your Laptop
     ↓ (push / PR / manual)
GitHub
     ↓
GitHub-hosted runner (ephemeral VM)
     ↓
Run pipeline steps
     ↓
VM is destroyed
