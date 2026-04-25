# 🚀 FortiCNAPP Code Security with GitLab (Step-by-Step Guide)

---

## 🚀 Final Workflow

```
Write Code → Commit → Push → Pipeline → Runner → Scan → Results in FortiCNAPP
```

---
## 🧠 Architecture Overview

```
Your Machine (Mac/Linux)
   ↓ (git add)
Prepare files
   ↓ (git commit)
Save version locally
   ↓ (git push)
Send to GitLab
   ↓
GitLab Pipeline 🚀
   ↓
GitLab Runner (execution engine)
   ↓
FortiCNAPP Code Security Scan
```

---

## ⚙️ Core Concepts

| Component  | Role                                   |
| ---------- | -------------------------------------- |
| GitLab     | 🧠 Control plane (UI, pipelines, repo) |
| Runner     | 👷 Execution engine (runs scans)       |
| FortiCNAPP | 🔐 Security analysis platform          |

---

## 📦 Basic Git Workflow

```bash
# 1. Prepare files
git add .

# 2. Save locally
git commit -m "Add files to scan"

# 3. Send to GitLab
git push
```

---

## 🔁 Trigger Pipeline Manually

GitLab only runs pipelines on **new commits**.

```bash
echo "trigger scan" >> README.md
git add README.md
git commit -m "Trigger FortiCNAPP scan"
git push
```

---

## 🏗️ GitLab Setup

### ✅ Prerequisites

* GitLab Server running
* Project created
* Git repository initialized

---

## 🧪 CI/CD Pipeline Configuration

Create file in repo:

```bash
.gitlab-ci.yml
```

Example:

```yaml
include:
  - remote: 'https://gitlab.com/lacework-security/code-security/code-security-gitlab/-/raw/main/lacework-code-security.yaml'

stages:
  - security-scan
```

---

## 🔑 Required Variables

Go to:

```
Project → Settings → CI/CD → Variables
```

| Variable        | Required               | Example                        | Purpose            |
| --------------- | ---------------------  | ------------------------------ | ------------------ |
| LW_ACCOUNT      | ✅                     | mycompany                      | FortiCNAPP account |
| LW_API_KEY      | ✅                     | abc123                         | Authentication     |
| LW_API_SECRET   | ✅                     | xyz456                         | Authentication     |
| LW_GITLAB_TOKEN | ✅                     | glpat-xxxx                     | GitLab API access  |
| GITLAB_URL      | ⚠️ (self-hosted only)  | http://gitlab.example.com      | GitLab instance    |

---

## 🔐 Create GitLab Token

```
Project → Settings → Access Tokens
```

| Field | Value            |
| ----- | ---------------- |
| Name  | forticnapp-token |
| Role  | Maintainer       |
| Scope | api              |

---

## 🏃 Runner Setup

### When to register runner?

| Scenario              | Action            |
| --------------------- | ----------------- |
| Runner already exists | ❌ Do NOT register |
| No runner exists      | ✅ Register        |

---

### Register Runner

```bash
sudo gitlab-runner register
```

Use:

```
GitLab URL: http://gitlab.example.com:8081
Token: glrt-xxxx
Executor: docker
Image: alpine:latest
```

✅ Enable:

```
Run untagged jobs
```

---

## 📊 Expected Scan Output

```
✔ Vulnerabilities detected
✔ Weaknesses detected
✔ Secrets detected
✔ Results uploaded to FortiCNAPP
```

Example:

| Type     | Count |
| -------- | ----- |
| Critical | 7     |
| High     | 28    |
| Medium   | 20    |
| Low      | 4     |

---

## ☁️ FortiCNAPP Verification

Go to:

```
FortiCNAPP → Code Security
```

Search:

```
<namespace>/<project-name>
```

---

## 🔄 CI/CD vs Manual Scan

| Mode                      | Upload Behavior          |
| ------------------------- | ------------------------ |
| CLI (`lacework sca scan`) | ❌ Needs `--save-results` |
| GitLab Pipeline           | ✅ Auto upload            |

---

## 🎯 Key Takeaways

* GitLab = control plane
* Runner = execution engine
* Pipelines trigger scans
* Commits trigger pipelines
* Submodules must be converted to real files
* Self-hosted GitLab requires `GITLAB_URL`

---

## ✅ Status Checklist

| Step                 | Status |
| -------------------- | ------ |
| GitLab Setup         | ✅      |
| Runner Connected     | ✅      |
| Variables Configured | ✅      |
| Pipeline Running     | ✅      |
| Results in CNAPP     | ✅      |

---

# 🎉 Done

You now have a fully working GitLab + FortiCNAPP Code Security pipeline.
