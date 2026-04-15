# FortiCNAPP PoV Toolbox – Vulnerable Java Lab

This lab demonstrates how to:
- Detect vulnerabilities in code (SCA/SAST)
- Build a vulnerable Docker image
- Enforce CI/CD blocking using FortiCNAPP
- Push and scan container images

---

## 📁 Project Structure

```
forticnapp-pov-toolbox/
└── cicd/
    └── vuln-java-lab/
        ├── pom.xml
        ├── Dockerfile
        ├── README.md
        └── src/
            └── main/
                ├── java/com/example/app/
                │   ├── App.java
                │   ├── LoginController.java
                │   └── UnsafeQueryService.java
                └── resources/
                    └── application.properties
```

---

## 🧪 Lab Overview

This intentionally vulnerable application includes:

- ❌ Outdated dependencies (CVE exposure)
- ❌ Insecure coding practices (e.g., unsafe query handling)
- ❌ Vulnerable container base image

---

## ⚙️ Step 1 – Build the Java Application

```bash
cd cicd/vuln-java-lab
mvn package
```

Expected output:

```
target/*.jar
```

---

## 🐳 Step 2 – Build Docker Image

```bash
docker build -t hello-app:latest .
```

---

## ▶️ Step 3 – Run Locally (Optional)

```bash
docker run -p 8080:8080 hello-app:latest
```

---

## 🔐 Step 4 – FortiCNAPP Code Security Scan

```bash
lacework sca scan . --save-results
```

---

## 🚫 Step 5 – CI/CD Enforcement (Block on Vulnerabilities)

Pipeline logic:

- If **Critical or High vulnerabilities exist → FAIL**
- If clean → continue

---

## 🚀 Step 6 – Docker Hub Integration

Pipeline flow:

```
Code Scan → Enforce Policy → Build Image → Push to Docker Hub
```

---

## 🔁 CI/CD Workflow Summary

```
Checkout
   ↓
FortiCNAPP SCA Scan
   ↓
Policy Enforcement (Block if vulnerable)
   ↓
Build Java App (Maven)
   ↓
Build Docker Image
   ↓
Push to Docker Hub
```

---

## 🎯 Expected Demo Outcome

In FortiCNAPP UI:

- Code Security:
  - CVEs from vulnerable dependencies
  - Weaknesses from insecure code

- Container Security:
  - OS/package vulnerabilities
  - Image-level CVEs

---

## ⚠️ Important Note

This is an intentionally vulnerable application for demo purposes only.  
Do not use in production environments.

---

## 📌 Next Steps

- Add Terraform (IaC) vulnerabilities
- Integrate runtime protection (RiskWatch)
- Expand CI/CD enforcement policies
