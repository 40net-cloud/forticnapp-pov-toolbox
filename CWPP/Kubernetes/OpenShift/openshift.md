## 🧩 FortiCNAPP (Lacework) Agent Guide on OpenShift (RHCOS)

Follow these steps to completely deploy Lacework (FortiCNAPP) Linux agent on OpenShift RHCOS Cluster.
Each step includes a brief explanation and ready-to-copy command.

#### Example Result:

<img width="1456" height="588" alt="Screenshot 2025-11-07 at 2 47 16 PM" src="https://github.com/user-attachments/assets/3a0d8953-31f7-43a3-a58a-6cfbe6086bce" />


<img width="1468" height="344" alt="Screenshot 2025-11-07 at 2 56 45 PM" src="https://github.com/user-attachments/assets/55ab2b3b-b595-441c-9aaa-fc8686885128" />

---
---

### ⚙️ FortiCNAPP Agent deployment on OpenShift (RHCOS)

#### 🧱 1️⃣ Create Namespace
Create (or reapply) the `lacework` namespace for the agent deployment.
Why: Ensures the namespace exists and is managed declaratively for future automation.

```bash
oc create namespace lacework --dry-run=client -o yaml | oc apply -f -
```

#### 🔐 2️⃣ Grant privileged SCC to Default Service Account
Grant the Security Context Constraint (SCC) privileged to the default service account in the lacework namespace.
Why: The Lacework agent DaemonSet needs privileged permissions to attach eBPF hooks and collect runtime telemetry on the host kernel.

```bash
oc -n lacework adm policy add-scc-to-user privileged -z default
```

#### 📦 3️⃣ Add and Update the Helm Repository
Add the official Lacework Helm repository and update local chart metadata.
Why: Ensures you have the latest Helm chart version before deployment or upgrade.

```bash
helm repo add lacework https://lacework.github.io/helm-charts/
helm repo update
```

#### 🚀 4️⃣ Deploy (or Upgrade) the Lacework Agent via Helm
Install or upgrade the agent release using your specific configuration values.

```bash

helm upgrade --install lacework-agent lacework/lacework-agent \
  --namespace lacework --create-namespace \
  --set laceworkConfig.accessToken=b8e67defc53aa0...fa2d2 \
  --set laceworkConfig.serverUrl=https://api.lacework.net \
  --set laceworkConfig.kubernetesCluster=rhcos \
  --set laceworkConfig.env=poc \
  --set priorityClassCreate=true \
  --set laceworkConfig.codeaware.enable=experimental \
  --set laceworkConfig.packagescan.enable=true \
  --set laceworkConfig.procscan.enable=true \
  --set tolerations[0].operator=Exists \
  --set resources.requests.memory=256Mi \
  --set resources.limits.memory=512Mi

```
---

### ⚙️ FortiCNAPP Agent Helm Configuration Summary

This table summarizes the Helm parameters used to deploy the FortiCNAPP (Lacework) Linux Agent on **OpenShift (RHCOS)**.  
These values were retrieved from the current Helm release using:  
`helm get values lacework-agent -n lacework`

| Variable / Option | Description | Example / Command |
|--------------------|--------------|--------------------|
| `serverUrl=${LACEWORK_SERVER_URL}` | FortiCNAPP (Lacework) API endpoint URL — region-specific (e.g., `https://api.lacework.net`). | **Current value:** `https://api.lacework.net`<br>**Helm flag:** `--set laceworkConfig.serverUrl=${LACEWORK_SERVER_URL}` |
| `accessToken=${LACEWORK_AGENT_TOKEN}` | Access token for agent authentication (sensitive). | **Current value:** `b8e67defc53aa0...fa2d2` *(truncated)*<br>**Helm flag:** `--set laceworkConfig.accessToken=${LACEWORK_AGENT_TOKEN}` |
| `kubernetesCluster=${KUBERNETES_CLUSTER_NAME}` | Logical cluster name as it appears in FortiCNAPP. | **Current value:** `rhcos`<br>**Helm flag:** `--set laceworkConfig.kubernetesCluster=${KUBERNETES_CLUSTER_NAME}` |
| `laceworkConfig.env=${KUBERNETES_ENVIRONMENT_NAME}` | Environment label for grouping (e.g., POC, Production, Staging). | **Current value:** `poc`<br>**Helm flag:** `--set laceworkConfig.env=${KUBERNETES_ENVIRONMENT_NAME}` |
| `laceworkConfig.packagescan.enable` | Enable package-level vulnerability scanning for hosts and containers. | **Current value:** `true` |
| `laceworkConfig.procscan.enable` | Enable process activity and behavioral scanning. | **Current value:** `true` |
| `laceworkConfig.codeaware.enable` | Enable active package detection on hosts and containers. | **Current value:** `experimental` |
| `resources.limits.memory` | Maximum memory limit per agent pod. | **Current value:** `512Mi` |
| `resources.requests.memory` | Minimum memory requested for scheduling the agent pod. | **Current value:** `256Mi` |
| `priorityClassCreate` | Creates a Kubernetes PriorityClass for agent scheduling preference. | **Current value:** `true` |
| `tolerations` | Allows the agent DaemonSet to run on all node types, including infra and control-plane nodes. | **Current value:**<br>`- operator: Exists`<br>**Helm flag:** `--set 'tolerations[0].operator=Exists'` |



#### 🧠 Notes
- Verified on **OpenShift (RHCOS)** using `helm get values lacework-agent -n lacework`.  
- Token is truncated for security purposes.  
- `packagescan`, `procscan`, and `codeaware` are all **enabled**, ensuring comprehensive host and container coverage.  
- `tolerations` and `priorityClassCreate` guarantee deployment on every node.  


---

#### Example Results:
---

<img width="1456" height="588" alt="Screenshot 2025-11-07 at 2 47 16 PM" src="https://github.com/user-attachments/assets/3a0d8953-31f7-43a3-a58a-6cfbe6086bce" />

---
<img width="1286" height="354" alt="Screenshot 2025-11-07 at 3 14 42 PM" src="https://github.com/user-attachments/assets/f015d143-0143-4560-bcc8-0817a2704c31" />

---
<img width="1213" height="674" alt="Screenshot 2025-11-07 at 3 00 17 PM" src="https://github.com/user-attachments/assets/e1d2fc83-f95b-4f7c-9e48-b128d8cdd5e0" />


---

#### 🧠 Notes For Container Image Vulnerability Scanning 
#####  Add:  Container registries Integration

<img width="1464" height="235" alt="Screenshot 2025-11-07 at 2 52 42 PM" src="https://github.com/user-attachments/assets/a5a82630-7f50-4664-9b27-a64e69658f37" />

---

<img width="1456" height="534" alt="Screenshot 2025-11-07 at 2 51 14 PM" src="https://github.com/user-attachments/assets/b27acb59-ae0c-4519-819a-b660290587bd" />

---
---

## 🧩 Verify Helm  and Agent Deployment
#### Check Helm Deployment for Lacework Agent

Use the following steps to verify which Helm chart, version, and configuration were used to deploy the Lacework (FortiCNAPP) agent on OpenShift.

| Step | Command | Description | Example Output / Meaning |
|------|----------|--------------|--------------------------|
| **1️⃣ List all Helm releases in the `lacework` namespace** | `helm list -n lacework` | Lists every Helm release deployed under the namespace, including the chart name, app version, and deployment status. | **Example:**<br>`NAME: lacework-agent`<br>`NAMESPACE: lacework`<br>`STATUS: deployed`<br>`CHART: lacework-agent-1.4.2`<br>`APP VERSION: 7.10.0` |
| **2️⃣ Check which chart and values were used** | `helm get all lacework-agent -n lacework` | Displays full Helm release information — including chart metadata, manifests, and parameters used during installation. | Confirms the chart version, namespace, and Kubernetes manifests created for the deployment. |
| **3️⃣ View Helm values (custom configuration)** | `helm get values lacework-agent -n lacework` | Shows parameters provided during Helm install, such as account name, API token, cluster name, or proxy settings. | **Example:**<br>`accountName: lacework-demo`<br>`clusterName: ocp-lab`<br>`autoUpdate: true` |
| **4️⃣ Confirm Helm chart metadata** | `helm get manifest lacework-agent -n lacework` | Prints Helm chart details to verify which resources (DaemonSet, ConfigMap, Secrets, etc.) were deployed. | **Example:**<br>`apiVersion: apps/v1`<br>`kind: DaemonSet`<br>`metadata: name: lacework-agent` |
| **5️⃣ Find release across all namespaces (if unsure)** | `helm list --all-namespaces` | Searches for any Helm release containing “lacework” across all namespaces. | **Example:**<br>`lacework-agent  lacework  deployed  lacework-agent-1.4.2  7.10.0` |


#### 🧠 Notes

- The Helm release name is typically **`lacework-agent`**.  
- The namespace is usually **`lacework`**, unless changed during installation.  
- **CHART VERSION** shows the Helm chart version used.  
- **APP VERSION** corresponds to the actual Lacework agent binary version.  
- These commands confirm how the agent was deployed and what configuration was applied.

---

#### 🧱 Check Lacework Agents Deployment

| Step | Command | Expected Output | Meaning / Action |
|------|----------|----------------|------------------|
| **List DaemonSet and pods** | `oc -n lacework get ds,pods -o wide` | All pods show `1/1 Running` and DaemonSet desired = current = ready | ✅ Agents deployed successfully across all nodes |
| **Show pod labels** | `oc -n lacework get pods -o wide --show-labels` | Labels include `name=lacework-agent` | ✅ Confirms label selector used by DaemonSet |
| **Describe one agent pod** | `oc -n lacework describe pod -l name=lacework-agent \| egrep -i 'Service Account\|scc:\|SecurityContext\|Reason'` | Shows service account and SCC in use | 🧩 Confirms correct permissions (privileged / SCC assignment) |


---
---

## 🧩 FortiCNAPP (OpenShift RHCOS) Agent Troubleshooting Guide

---

#### 🧱 1. Check Lacework Agents Deployment

| Step | Command | Expected Output | Meaning / Action |
|------|----------|----------------|------------------|
| **List DaemonSet and pods** | `oc -n lacework get ds,pods -o wide` | All pods show `1/1 Running` and DaemonSet desired = current = ready | ✅ Agents deployed successfully across all nodes |
| **Show pod labels** | `oc -n lacework get pods -o wide --show-labels` | Labels include `name=lacework-agent` | ✅ Confirms label selector used by DaemonSet |
| **Describe one agent pod** | `oc -n lacework describe pod -l name=lacework-agent \| egrep -i 'Service Account\|scc:\|SecurityContext\|Reason'` | Shows service account and SCC in use | 🧩 Confirms correct permissions (privileged / SCC assignment) |

---

#### 🧱 1. Check Agent Pod Status

| Purpose | Command | Expected Output | Meaning |
|----------|----------|----------------|----------|
| **List Lacework pods** | `oc -n lacework get pods -l name=lacework-agent` | All pods show `1/1 Running` and no restarts | ✅ Agent pods deployed and healthy |
| **Confirm labels (optional)** | `oc -n lacework get pods -o wide --show-labels` | Includes label `name=lacework-agent` | 🧩 Confirms correct DaemonSet labels |

---

#### 🌐 2. Verify Connectivity to Backend
##### Change lacework-agent-cpwwt with your pod-name

| Purpose | Command | Example Output | Meaning |
|----------|----------|----------------|----------|
| **Check authentication / controller connection** | `oc -n lacework logs lacework-agent-cpwwt \| grep -E -i 'connected to controller\|authenticated\|registered' \| tail -n 3` | ```time="2025-11-04T07:44:46.897Z" level=info msg="Connected to controller, version 7.10.0.29352"``` | ✅ Agent is authenticated and connected to the Lacework (FortiCNAPP) backend |

---

#### ⚙️ 3. Confirm Runtime Monitoring (eBPF)
##### Change lacework-agent-cpwwt with your pod-name

| Purpose | Command | Example Output | Meaning |
|----------|----------|----------------|----------|
| **Check EventMonitor and eBPF status** | `oc -n lacework logs lacework-agent-cpwwt \| grep -E -i 'EventMonitor\|Loaded eBPF' \| tail -n 3` | ```time="2025-11-04T07:44:27.973Z" level=info msg="Loaded eBPF programs for socket events: V2Btf"``` | ✅ Runtime visibility and container telemetry active |

---

#### 🚨 4. Look for Real Errors
##### Change lacework-agent-cpwwt with your pod-name

| Purpose | Command | Example Output | Meaning |
|----------|----------|----------------|----------|
| **Show only error lines (last few)** | `oc -n lacework logs lacework-agent-cpwwt \| grep -E -i 'level=error' \| tail -n 5` | ```time="2025-11-04T07:44:50.486Z" level=error msg="Failed to stop child ... no such process"``` | ⚙️ Harmless cleanup error — ignore unless repeated |

---

#### 🧠 5. Interpretation Summary

| Result | What It Means | Action |
|---------|----------------|--------|
| `Connected to controller` appears | Agent authenticated and communicating | ✅ Healthy |
| `Starting Container EventMonitor` and `Loaded eBPF` appear | Runtime container monitoring active | ✅ Working |
| Only one or few “no such process” errors | Transient internal cleanup | ⚙️ Normal |
| Repeated `failed to authenticate` or `connection refused` | Network, key, or proxy issue | ❌ Check credentials or outbound access |


---
---

## 🔧 Clean destroy lacwork agent (OpenShift)
### Optional: delete namespace if you want a full reset

```bash
helm uninstall lacework-agent -n lacework
```

---
---


## 📚 Reference Documentation

Use the following official Fortinet FortiCNAPP resources when deploying or troubleshooting the Lacework (FortiCNAPP) Linux agent on OpenShift and related platforms.

| Reference Topic | Description | Official Documentation Link |
|------------------|-------------|------------------------------|
| **Installing on OpenShift / Kubernetes** | Step-by-step installation of the FortiCNAPP (Lacework) Linux agent as a DaemonSet in OpenShift and Kubernetes clusters. Includes YAML examples, RBAC configuration, and verification steps. | [Installing Linux Agent on Kubernetes (FortiCNAPP Admin Guide)](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/663510/installing-linux-agent-on-kubernetes) |
| **October 2025 Linux Agent Releases** | Latest release notes for the FortiCNAPP Linux Agent, including new features, fixes, version numbers, and compatibility information for October 2025. | [October 2025 Linux Agent Release Notes](https://docs.fortinet.com/document/forticnapp/latest/release-notes/412967/october-2025-linux-agent-releases) |
| **Host OS & Language Library Support** | Lists the supported Linux/Windows OS versions, RHCOS compatibility, applications, and language package libraries for vulnerability assessments. | [Host OS and Language Library Support for Vulnerability Assessment (RHCOS)](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/999307/host-os-and-language-library-support-for-vulnerability-assessment#:~:text=8.x-,Red%20Hat%20Core%20OS,-4.x) |

---
---


