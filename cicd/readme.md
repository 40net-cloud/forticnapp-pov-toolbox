
## vuln-java-lab structure

| Path | What it is | Why it exists | Who uses/scans it |
|---|---|---|---|
| `vuln-java-lab/pom.xml` | Maven project file | Defines Java project metadata, dependencies, and build behavior | Maven uses it to build; SCA reads it to identify dependencies |
| `vuln-java-lab/src/main/java/com/example/app/App.java` | Main Java class | Entry point for the sample application | Java compiler/build uses it; SAST scans it as source code |
| `vuln-java-lab/src/main/java/com/example/app/LoginController.java` | Sample application logic | Represents business/application logic for the demo | Java compiler/build uses it; SAST scans it |
| `vuln-java-lab/src/main/java/com/example/app/UnsafeQueryService.java` | Intentionally vulnerable demo code | Used to trigger security findings for the lab | Java compiler/build uses it; SAST scans it |
| `vuln-java-lab/src/main/resources/application.properties` | Application configuration | Stores application settings and demo configuration values | Application runtime may read it; secrets scanning may flag sensitive values if present |
| `vuln-java-lab/test-data/fake-secrets.txt` | Fake secrets file | Intentionally contains non-real secrets for testing secret detection safely | Secrets scanning reads it |
| `vuln-java-lab/README.md` | Lab-specific documentation | Explains what this demo app is for and how to use it | Human readers |
| `README.md` or `readme.md` at repo/folder level | General documentation | Explains the broader repo or section | Human readers |
