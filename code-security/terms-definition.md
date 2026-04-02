


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


Code (SAST scans this)
     ↓ uses
Libraries
     ↓ installed by
Package Manager
     ↓ defined in
Dependency File (SCA scans this)
* A package manager is a tool that downloads, installs, and manages libraries (dependencies) your code needs.
