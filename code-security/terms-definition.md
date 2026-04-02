

## 🔁 SAST vs SCA Flow

```text
Code (.java / .py / .js)
        │
        ▼
Uses Libraries (Dependencies)
        │
        ▼
Installed via Package Manager
(Maven / pip / npm / Composer / Go)
        │
        ▼
Defined in Dependency File
(pom.xml / requirements.txt / package.json)
        │
        ▼
SCA scans dependencies
SAST scans code

```

## 🔁 Code → Dependencies → SAST / SCA Flow (with dependency tree)

```text
Code (.java / .py / .js)
        │
        │  SAST scans code
        ▼
Uses Libraries (Direct Dependencies)
        │
        │  Defined by developer
        ▼
Dependency File
(pom.xml / requirements.txt / package.json)
        │
        │  e.g. you define: mongoose / spring-web
        ▼
Package Manager (Maven / npm / pip / Composer / Go)
        │
        │  Resolves dependencies
        ▼
Direct Dependencies
        │
        │  (libraries you explicitly added)
        ▼
Transitive Dependencies
        │
        │  (libraries required by other libraries)
        │
        │  e.g.
        │    mongoose → mongodb → bson → debug
        ▼
All Installed Libraries (Full Dependency Tree)
        │
        │  stored locally:
        │    node_modules/
        │    ~/.m2/
        ▼
SCA scans ALL libraries
(direct + transitive)
```

```text
Package managers for the same language do the same job (manage dependencies), but differ in flexibility, performance, and complexity.
```

## 🧠 Code, Package Manager, and Dependency Mapping

| Language | Standard Code Location (SAST scans) | Dependency File(s) (SCA scans) | Package Manager / Build Tool | Where Dependency File Lives |
|----------|---------------------------|--------------------------------|------------------------------|-----------------------------|
| Java (Maven) | src/main/java/... | pom.xml | Maven | Project root |
| Java (Gradle) | src/main/java/... | build.gradle / build.gradle.kts / gradle.lockfile | Gradle | Project root |
| Java (Bazel) | src/main/java/... | MODULE.bazel / BUILD.bazel | Bazel | Root + module folders |
| Python | src/ or root | requirements.txt / Pipfile / pyproject.toml | pip / Pipenv / Poetry | Project root |
| JavaScript | src/ or root | package.json + package-lock.json | npm / yarn / pnpm | Project root |
| TypeScript | src/ or root | package.json + lockfile | npm / yarn / pnpm | Project root |
| Go | root or cmd/ | go.mod + go.sum | Go modules | Project root |
| PHP | src/ or public/ | composer.json + composer.lock | Composer | Project root |


## 🧠 SAST, SCA & DAST

| Aspect                          | **SAST (Static Application Security Testing)** | **SCA (Software Composition Analysis)**              | **DAST (Dynamic Application Security Testing)** |
| ------------------------------- | ---------------------------------------------- | ---------------------------------------------------- | ----------------------------------------------- |
| **What it scans (WHAT)**        | Your **source code** (`.java`, `.py`, `.js`)   | Your **dependencies** (`pom.xml`, `package.json`)    | Your **running application (URL)**              |
| **Main purpose (WHY)**          | Find **coding mistakes / weaknesses**          | Find **known vulnerable libraries (CVE)**            | Find **real exploitable issues at runtime**     |
| **How it works (HOW)**          | Analyzes code patterns without running it      | Matches dependencies against vulnerability databases | Sends malicious requests like an attacker       |
| **Example input**               | `LoginController.java`                         | `pom.xml`                                            | `https://app.com/login`                         |
| **Example issue**               | SQL injection in code                          | Vulnerable `log4j` version                           | SQL injection successfully exploited            |
| **Where it runs (CI/CD stage)** | Early (PR / push)                              | Early (PR / push)                                    | Late (after deployment)                         |
| **Needs source code?**          | ✔ Yes                                          | ✔ Yes (dependency files)                             | ❌ No                                            |
| **Needs running app?**          | ❌ No                                           | ❌ No                                                 | ✔ Yes                                           |
| **Focus area**                  | Your logic                                     | Third-party libraries                                | Application behavior                            |
| **Type of findings**            | Weaknesses (potential risks)                   | Vulnerabilities (known CVEs)                         | Confirmed vulnerabilities (real attacks)        |
| **Confidence level**            | Medium (might be exploitable)                  | High (known vulnerability)                           | Very high (proven exploit)                      |
| **Fix approach**                | Fix your code                                  | Upgrade/remove dependency                            | Fix backend logic/config                        |
| **Example question it answers** | “Did I write insecure code?”                   | “Am I using insecure libraries?”                     | “Can my app actually be hacked?”                |
| **When to use**                 | During development                             | During development                                   | After deployment                                |
| **Output format**               | File + line number                             | Library + CVE                                        | URL + endpoint                                  |


