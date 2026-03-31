└── SCA Component (lacework component install sca)
    ├── Software Composition Analysis (SCA)
    ├── Static Application Security Testing (SAST)
    ├── Secrets Detection
    ├── SBOM Generation
    └── License Compliance


  | Aspect        | SCA (Software Composition Analysis) | SAST (Static Application Security Testing) |
| ------------- | ----------------------------------- | ------------------------------------------ |
| What it scans | Dependencies / libraries            | Your source code                           |
| Focus         | Third-party risk                    | Coding mistakes                            |
| Example       | vulnerable `log4j`, `openssl`       | SQL injection, hardcoded password          |
| Input         | `package.json`, `pom.xml`, etc.     | `.java`, `.js`, `.py` files                |
| Ownership     | External code                       | Your code                                  |
| Output        | CVEs in libraries                   | Vulnerabilities in logic                   |
| When used     | Dependency management               | Development phase                          |
| Fix type      | Update/replace library              | Fix code                                   |
