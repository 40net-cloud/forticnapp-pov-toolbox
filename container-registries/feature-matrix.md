




Application Deployment Comparison (Containers vs VM vs Bare Metal)

| Feature              | Traditional OS | VM   | Container  |
| -------------------- | -------------- | ---- | ---------  |
| Dependency isolation | ❌              | ✅    | ✅       |
| Separate OS per app  | ❌              | ✅    | ❌       |
| Resource usage       | Low            | High | Low        |
| Startup time         | Fast           | Slow | Very fast  |



| Stage                              | What It Solved                                   | New Problem Introduced                   |
| ---------------------------------- | ------------------------------------------------ | ---------------------------------------- |
| **Traditional OS (single server)** | Run multiple applications on one OS              | Dependency conflicts between apps        |
| **Virtual Machines (VMs)**         | Isolate each application with its own OS         | Heavy resource usage (CPU, RAM, storage) |
| **Containers**                     | Isolate application environments without full OS | Requires container runtime/orchestrators |



| Category                | **Containers**                    | **Virtual Machines (VMs)**  | **Bare Metal / Traditional Apps**        |
| ----------------------- | --------------------------------- | --------------------------- | ---------------------------------------- |
| Virtualization type     | OS-level virtualization           | Hardware virtualization     | No virtualization                        |
| What is isolated        | Application processes             | Entire operating system     | Nothing (apps share OS directly)         |
| OS requirement          | Share host OS kernel              | Each VM runs its own OS     | All apps share same OS                   |
| Image size              | Small (10MB–500MB)                | Large (GBs)                 | Not packaged                             |
| Startup time            | Seconds                           | Minutes                     | Minutes                                  |
| Resource usage          | Very efficient                    | Heavy (each VM includes OS) | Depends on installed apps                |
| Number per host         | Hundreds possible                 | Usually limited (10–20)     | Depends on system configuration          |
| Portability             | Very portable across environments | Less portable               | Hard to move between systems             |
| Environment consistency | Same image runs everywhere        | Environment may differ      | Highly dependent on server configuration |
| Deployment complexity   | Simple image deployment           | OS provisioning required    | Manual installation                      |
| Scaling applications    | Easy horizontal scaling           | Slower scaling              | Difficult to scale                       |
| Security isolation      | Medium (shared kernel)            | Strong (separate OS)        | Weak (shared OS)                         |
| Typical usage           | Microservices, cloud-native apps  | Legacy apps, OS isolation   | Older applications                       |
| DevOps integration      | Excellent CI/CD support           | Moderate                    | Limited                                  |
| Infrastructure cost     | Lower due to density              | Higher due to OS overhead   | Moderate                                 |
| Common platforms        | Kubernetes, Docker                | VMware, Hyper-V, EC2        | Traditional servers                      |




1️⃣ Container Runtime Comparison (Why you would choose each)
Image Builder vs Container Runtime (Container Ecosystem)

| Environment              | Image Builder              | Runtime             |
| ------------------------ | -------------------------- | ------------------- |
| Developer laptop         | Docker Build               | Docker              |
| CI/CD pipelines          | Docker / BuildKit / Kaniko | N/A (build only)    |
| Kubernetes cluster       | Kaniko / BuildKit          | containerd / CRI-O  |
| OpenShift                | Buildah / Podman           | CRI-O               |
| Enterprise Linux servers | Podman build               | Podman              |
| Cloud VM container host  | Docker / Buildah           | containerd / Docker |

Kubernetes Usage Across Major Platforms

| Platform                                | Kubernetes Service               | Default Container Runtime | Image Build Methods Commonly Used       | Container Registry              | Notes                                                    |
| --------------------------------------- | -------------------------------- | ------------------------- | --------------------------------------- | ------------------------------- | -------------------------------------------------------- |
| **OpenShift (RedHat)**                  | OpenShift Kubernetes             | **CRI-O**                 | Buildah, Podman, OpenShift BuildConfigs | OpenShift Image Registry / Quay | Enterprise Kubernetes with integrated CI/CD and security |
| **AWS**                                 | EKS (Elastic Kubernetes Service) | **containerd**            | Docker, BuildKit, Kaniko, CodeBuild     | AWS ECR                         | Most common cloud Kubernetes runtime environment         |
| **Azure**                               | AKS (Azure Kubernetes Service)   | **containerd**            | Docker, ACR Tasks, BuildKit, Kaniko     | Azure Container Registry (ACR)  | Docker runtime removed; containerd used                  |
| **Google Cloud**                        | GKE (Google Kubernetes Engine)   | **containerd**            | Cloud Build, Docker, Kaniko             | Artifact Registry / GCR         | Google helped create Kubernetes                          |
| **Oracle Cloud (OCI)**                  | OKE (Oracle Kubernetes Engine)   | **containerd**            | Docker, BuildKit                        | OCI Container Registry          | Similar architecture to other managed Kubernetes         |
| **On-Prem Kubernetes**                  | Self-managed clusters            | **containerd / CRI-O**    | Docker, Buildah, Kaniko                 | Harbor, Nexus, Docker Registry  | Used in private data centers                             |
| **VM-based containers (no Kubernetes)** | Docker / Podman environments     | **Docker / Podman**       | Docker Build, BuildKit                  | Docker Hub, private registry    | Simple container deployments                             |


1️⃣ Container Runtime Comparison (Why you would choose each)

| Runtime             | What it is                                | Why people choose it (real reason)                                                                                                                                                  | When you would NOT choose it                                                                         | Typical environments                                |
| ------------------- | ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| **containerd**      | Lightweight container runtime             | Very simple and stable. It only focuses on running containers, so it has fewer components and less overhead. Cloud providers prefer it because it is reliable and easy to maintain. | If you want developer-friendly tools like building images or managing containers easily from CLI.    | Kubernetes clusters in AWS EKS, Azure AKS, GKE, OCI |
| **CRI-O**           | Runtime built specifically for Kubernetes | Designed only for Kubernetes, so it integrates perfectly and removes unnecessary features. RedHat prefers it for enterprise Kubernetes.                                             | If you want to run containers outside Kubernetes or need flexible container tooling.                 | OpenShift and enterprise Kubernetes                 |
| **Docker Engine**   | Full container platform                   | Very easy to use and has the best developer experience. Includes building images, running containers, and registry integration in one tool.                                         | For large production clusters where only a runtime is needed and Docker adds unnecessary complexity. | Developer laptops, CI pipelines                     |
| **Podman**          | Docker alternative runtime                | More secure because it does not use a central daemon and supports rootless containers. This reduces security risks in enterprise environments.                                      | If you need the full Docker ecosystem or compatibility with existing Docker workflows.               | Enterprise Linux, RHEL environments                 |
| **runc**            | Low-level container runtime               | Actually executes the container process according to the OCI standard. It is the core runtime used underneath most systems.                                                         | Not used directly by users; it is usually used through containerd or Docker.                         | Internal component of container platforms           |
| **Kata Containers** | Secure container runtime                  | Runs each container inside a lightweight virtual machine, providing stronger isolation similar to VMs. Useful for multi-tenant environments where security matters.                 | If performance and startup speed are more important than strong isolation.                           | Secure cloud workloads                              |
| **gVisor**          | Sandbox runtime                           | Adds an extra layer between the container and the Linux kernel to reduce the impact of potential container escapes.                                                                 | If you need maximum performance because the extra isolation layer adds overhead.                     | Security-sensitive environments                     |
| **Firecracker**     | Micro-VM runtime                          | Combines container speed with VM isolation. Used in serverless platforms where thousands of workloads start quickly.                                                                | If you need traditional container management rather than serverless environments.                    | AWS Lambda, serverless compute                      |



2️⃣ Container Registry Comparison (Why you would choose each)
| Registry                             | What it is                    | Why people choose it (real reason)                                                                                               | When you would NOT choose it                                                         | Typical environments                |
| ------------------------------------ | ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ----------------------------------- |
| **Docker Hub**                       | Public container registry     | Largest collection of container images available. Easy to share and discover public images.                                      | If you need strict security, private enterprise control, or compliance requirements. | Open source projects                |
| **AWS ECR**                          | Managed container registry    | Fully integrated with AWS security, IAM, and Kubernetes services. Very convenient if your infrastructure already runs in AWS.    | If you are running multi-cloud or on-prem environments.                              | AWS workloads                       |
| **Azure Container Registry (ACR)**   | Managed registry for Azure    | Integrated with Azure DevOps and AKS. Provides automatic builds and scaling without managing infrastructure.                     | If you do not use Azure infrastructure.                                              | Azure cloud deployments             |
| **Google Artifact Registry / GCR**   | Google Cloud registry         | Works seamlessly with GKE and Google Cloud Build pipelines, simplifying automated deployments.                                   | If your workloads are not running in Google Cloud.                                   | GCP environments                    |
| **OCI Container Registry (OCIR)**    | Oracle Cloud registry         | Integrated with Oracle Cloud identity and Kubernetes services.                                                                   | If your workloads are outside Oracle Cloud.                                          | OCI cloud deployments               |
| **Harbor**                           | Enterprise private registry   | Provides strong security features such as role-based access control, vulnerability scanning, and image replication across sites. | If you prefer a fully managed cloud service instead of running your own registry.    | On-prem enterprise environments     |
| **JFrog Artifactory**                | Universal artifact repository | Stores many artifact types (containers, Maven, npm, etc.) in one place, simplifying enterprise artifact management.              | If you only need a simple container registry.                                        | Large enterprise DevOps platforms   |
| **Sonatype Nexus**                   | Artifact repository           | Similar to Artifactory but often used in organizations managing many software packages.                                          | If you only need container images and not other artifact types.                      | Enterprise CI/CD pipelines          |
| **GitHub Container Registry (GHCR)** | Developer registry            | Integrated directly with GitHub repositories and CI pipelines, making publishing container images simple for developers.         | If you need advanced enterprise registry features.                                   | GitHub-based development workflows  |
| **GitLab Container Registry**        | GitLab-integrated registry    | Built into GitLab CI/CD pipelines, so images are automatically stored during builds.                                             | If your development platform is not GitLab.                                          | GitLab DevOps environments          |
| **Quay**                             | Enterprise container registry | Advanced security scanning and policy enforcement designed for enterprise Kubernetes platforms.                                  | If you need a lightweight or free registry.                                          | OpenShift and enterprise Kubernetes |



Kubernetes Platform vs Cluster Components (Why Each Exists)

| Layer                           | What it is                                                  | What it manages                                  | Example technologies                                                      | Example workload                                                               | Why this layer exists (why not simpler)                                                                                                                                            |
| ------------------------------- | ----------------------------------------------------------- | ------------------------------------------------ | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Managed Kubernetes Platform** | Managed service providing Kubernetes cluster infrastructure | Cluster lifecycle, networking, scaling, upgrades | AWS **EKS**, Azure **AKS**, Google **GKE**, **OpenShift**, Oracle **OKE** | EKS cluster hosting microservices                                              | Running Kubernetes manually is complex. Managed platforms automate cluster setup, upgrades, and control plane management so teams focus on applications instead of infrastructure. |
| **Cluster Node**                | Machine that runs container workloads                       | Pods scheduled by Kubernetes                     | EC2 VM, Azure VM, GCP VM, Bare-metal server                               | Node hosting multiple application pods                                         | Containers still need CPU, memory, disk, and networking. Nodes provide the physical or virtual compute resources where workloads run.                                              |
| **Pod**                         | Smallest deployable unit in Kubernetes                      | One or more containers that run together         | Kubernetes Pod object                                                     | `web-service pod` running an nginx container and a logging sidecar             | Kubernetes schedules Pods instead of containers because Pods provide shared networking, shared storage, and coordinated lifecycle for containers that work together.               |
| **Container Runtime**           | Software that runs containers on the node                   | Container lifecycle (start, stop, isolate)       | **containerd**, **CRI-O**, **Podman**                                     | containerd starting a Python API container                                     | Kubernetes itself does not run containers. The runtime communicates with the Linux kernel to create and manage containers.                                                         |
| **Container**                   | Packaged application environment                            | Application process and dependencies             | Docker/OCI container image                                                | **nginx container**, **Python API container**, **Java microservice container** | Containers package application code, libraries, and dependencies so the application runs the same way on any node.                                                                 |
| **Application**                 | Actual business logic or service                            | End-user functionality                           | Web service, API server, microservice                                     | nginx web server, Python REST API, Java payment service                        | Applications are what users interact with. Containers simply provide a consistent environment to run them reliably.                                                                |


What Exists Inside a Container Image

| Part inside the container image                   | Example inside the image                           | Real examples (Python / Java / Web server)                    | What it means in simple terms                                                        | Why it must be inside the image                                                                               |                                                                                                |
| ------------------------------------------------- | -------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| **Base Operating System**                         | Minimal Linux filesystem                           | Alpine Linux, Ubuntu, Debian                                  | Python API container uses Alpine Linux                                               | A small Linux environment that provides system folders, processes, networking stack, and file system          | Applications expect to run inside a Linux environment                                          |
| **System Libraries (OS packages)**                | Core OS libraries                                  | SSL library, networking library, compression library          | `libssl`, `glibc`, `zlib`                                                            | System-level tools that programs use for encryption, networking, or file operations                           | Many applications rely on these libraries to communicate securely or perform system operations |
| **Programming Runtime**                           | Software that executes a programming language      | Python interpreter, Java JVM, Node.js runtime                 | Python → Python interpreter<br>Java → Java Virtual Machine<br>Node.js → Node runtime | The environment that understands and executes the program written in that language                            | Without the runtime, the application code cannot run                                           |
| **External Application Libraries (Dependencies)** | Pre-built software modules used by the application | Web frameworks, database connectors, authentication libraries | Python → Flask or Django<br>Java → Spring framework<br>Node.js → Express             | These libraries provide ready-made features like handling web requests, database access, authentication, etc. | Developers use these instead of writing complex functionality from scratch                     |
| **Application Code**                              | Developer-written program                          | API service or backend logic                                  | `payment_api.py` (Python)<br>`payment-service.jar` (Java)<br>`server.js` (Node.js)   | This is the actual program implementing business logic                                                        | The container exists to run this application                                                   |
| **Configuration Files**                           | Application settings                               | Environment variables, config files                           | API port, database address, service credentials                                      | Defines how the application behaves in different environments                                                 | Allows the same image to run in development, staging, or production                            |
| **Container Startup Metadata**                    | Default program to start when container runs       | Startup command for application                               | Start nginx server, start Python API, run Java service                               | Instructions telling the container which program to launch                                                    | Ensures the container automatically starts the application                                     |

What Image Scanners Actually Inspect

| Component inside image | Scanned?    | What is detected        |
| ---------------------- | ----------- | ----------------------- |
| Base OS                | ✅ Yes       | OS CVEs                 |
| OS packages            | ✅ Yes       | Package vulnerabilities |
| Language runtime       | ✅ Yes       | Runtime vulnerabilities |
| Application libraries  | ✅ Yes       | Library CVEs            |
| Application code logic | ❌ No        | Handled by SAST         |



FortiCNAPP Container Image Vulnerability Scanning Methods


| Integration Type                                | Stage              | Image State                               | What it scans                                   | Where it runs                                         | Main use case                                                     | Key technical point                                                                                    |
| ----------------------------------------------- | ------------------ | ----------------------------------------- | ----------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Public Registry Scanning (Platform Scanner)** | Pre-deployment     | **Non-active images**                     | Images stored in internet-accessible registries | FortiCNAPP platform                                   | Scan images already stored in public registries                   | Integrate internet-accessible registries so the platform scanner can assess images for vulnerabilities |
| **Private Registry Scanning (Proxy Scanner)**   | Pre-deployment     | **Non-active images**                     | Images stored in private registries             | Proxy scanner deployed inside environment             | Scan images stored in registries that are not internet accessible | Proxy scanner pulls images from internal registries for vulnerability assessment                       |
| **CI / Inline Scanner**                         | Build pipeline     | **Non-active images** (image being built) | Newly built container images                    | CI systems (Jenkins, GitHub Actions, Travis CI, etc.) | Scan images during CI before pushing to registry                  | Inline scanner integrates into CI pipelines to assess images during build                              |
| **Local Scanning / Inline Scanner**             | Developer stage    | **Non-active images** (local build)       | Container images built locally                  | Developer machine                                     | Allow developers to test images before pushing them               | Inline scanner can run locally or via Lacework CLI without requiring console access                    |
| **CD / Kubernetes Admission Controller**        | Deployment control | **Non-active images** (about to run)      | Images referenced in Kubernetes deployment      | Kubernetes cluster                                    | Prevent vulnerable images from being deployed                     | Admission controller webhook and proxy scanner inspect images prior to deployment                      |
| **Agentless Workload Scanning (AWLS)**          | Running phase      | **Active containers / hosts**             | Running container workloads and hosts           | Cloud platform scan                                   | Detect vulnerabilities in running environments                    | Agentless scanning identifies containers and images running on hosts                                   |
| **Agent Scan**                                  | Running phase      | **Active containers / hosts**             | Containers and hosts running workloads          | Host agent                                            | Continuous vulnerability visibility at runtime                    | Agents installed on hosts collect container and host vulnerability data                                |



./lw-scanner image evaluate ubuntu 18.04  

docker run lacework/lacework-inline-scanner image evaluate nginx latest


// auth        configure Lacework platform authentication settings
./lw-scanner configure auth 

or ./lw-scanner image evaluate ubuntu 18.04   -n tenant-id -t inline-auh-token

Scanner Command Differences:
The difference is not “different scan engine” — it is how you launch the scanner.

| Aspect                | `lw-scanner image evaluate` (Binary)                                              | `docker run lacework/lacework-inline-scanner`                           |
| --------------------- | --------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| What runs the scanner | Scanner installed **as a program on the machine**                                 | Scanner **packaged inside a container image**                           |
| Where it can run      | Local machine **or CI runner**                                                    | Local machine **or CI runner**                                          |
| Authentication        | Can reuse **local saved config** (e.g., `~/.lacework`) → **easier for local use** | Cannot see local config unless mounted → usually pass **env variables** |
| Ease of use locally   | ✅ **Simpler** because local config already exists                                 | Slightly more complex                                                   |
| Ease of use in CI/CD  | Works but CI must **install the scanner binary first**                            | ✅ **Preferred in CI** because scanner is already inside the container   |
| Docker runtime usage  | Required to **handle container image format and layers**                          | Required to **run the scanner container and handle image layers**       |
| Scanner engine        | Same FortiCNAPP inline scanner                                                    | Same FortiCNAPP inline scanner                                          |





we need to continue and confirm the methods of integration for these methods focusing on container registries: platform-scanner scan image at the backend, while Proxy scanning happens on customer's side  and inline scanner scan at customer side  / The inline scanner is triggered on an on-demand basis / for integration it requires "Authorization Token" from the Inline-scanner integration



> **Note**
> Agentless Workload Scanning (AWLS) and FortiCNAPP Agents are explained in a separate folder.  
> This document focuses only on container registries vulnerability scanning only.



FortiCNAPP provides the ability to assess, identify, and report vulnerabilities found on hosts, containers, and pods within your environment. 
This means you can identify and take action on software vulnerabilities in your environment and manage that risk proactively.

FortiCNAPP continuously assesses vulnerability risks, identifies OS packages, and correlates them with publicly known vulnerabilities 
with risk ratings by severity and CVSS scores

Host vulnerability scanning with FortiCNAPP can be performed using two different methods:

FortiCNAPP Agent for vulnerability scanning on:
Linux hosts, pods, and containers
Windows Server hosts
Agentless Workload Scanning for vulnerability scanning on Linux hosts, **WindowsServers**, pods, and containers.


- FortiCNAPP uses the following CVE Sources for language libraries when using **agentless workload scanning:**

Risk Based Security (RBS) - VulnDB
GitHub Security Advisory (GHSA)
GitLab Advisory Community
FortiCNAPP uses  National Vulnerability Database (NVD) for the severity and CVSS score associated with the CVEs. 
When an NVD CVSS score is not available for a given GitHub Security Advisory (GHSA) package, 
FortiCNAPP uses the CVSS score directly from GHSA for that package.


- FortiCNAPP uses the following CVE sources for Windows OS and applications:
Risk Based Security (RBS) - VulnDB
Microsoft Security Response Center (MSRC)
FortiCNAPP uses multiple CVE / vulnerability sources and will determine the best source for new and existing vulnerabilities.

When a CVSS score is not available, FortiCNAPP reports the value as N/A in the Console, and 0 in the CLI.
FortiCNAPP assigns severities to CVEs based on the following criteria in the following order of preference:

The operating system distribution vendor (such as CentOS, Ubuntu, Alpine, etc.) provides a severity.
Unlike operating system vendors, language library projects do not directly provide vulnerability data. As such, there is no equivalent "vendor" severity.


The FortiCNAPP platform ingests new CVEs daily from OS vendors and the NIST National Vulnerability Database (NVD).




the platform-scanner pulls the entire image to our backend for analysis. The Proxy and inline scanner will also pull the entire image and analyze it, 
but only send the manifest to the Lacework backend


For the on-demand button click
press the button the UI will send a message to our backend to pull and scan the image from the registry that is the origin from the container you select


for proxy-scanner
scanning happens on customer's side and results are sent to us, and evaluation happens on our side.




















https://docs.fortinet.com/document/forticnapp/latest/administration-guide/182307
AWLS - Host Vulnerability - Scanning of Language Libraries and Package Managers


Host OS and language library support for vulnerability assessment:
https://docs.fortinet.com/document/forticnapp/latest/administration-guide/999307
