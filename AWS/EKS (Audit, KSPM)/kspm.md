# 🧩 AWS-EKS Security Posture Management (KSPM)  Integration  


## ⚙️Configuration

#!/usr/bin/env bash
set -euo pipefail

################################################################################
# 🧿 FortiCNAPP / Lacework KSPM + Agent Deployment for EKS
#
# This script deploys:
#   ✅ Lacework Agent DaemonSet  → Node Collector + Runtime Agent (CWPP)
#   ✅ Lacework Cluster Collector Deployment → Cluster-level KSPM
#
# It also:
#   - Configures API connection to your regional Lacework tenant
#   - Registers the EKS cluster for Kubernetes Security Posture Management (KSPM)
#   - Enables IMDS (Instance Metadata Service) access for collectors
#   - Applies tolerations for high-priority scheduling
################################################################################

echo "🚀 Deploying Lacework Agent + KSPM components..."

# ------------------------------------------------------------------------------
# 1) Helm install or upgrade
# ------------------------------------------------------------------------------

helm upgrade --install lacework-agent lacework-agent \
  --create-namespace \
  --namespace lacework \
  --repo https://lacework.github.io/helm-charts/ \
  \
  # --- Lacework API & Authentication ---
  --set laceworkConfig.serverUrl=https://api.fra.lacework.net \
  --set laceworkConfig.accessToken=0f28b6681ff56c9e51856f2871e126a5d30a2ad985e699bcbe1f4ea1 \
  \
  # --- Cluster Metadata ---
  --set laceworkConfig.kubernetesCluster=hkeksfrankfurt \
  --set laceworkConfig.env=Production \
  \
  # --- Cluster Collector Configuration (KSPM) ---
  --set clusterAgent.enable=true \
  --set clusterAgent.clusterType=eks \
  --set clusterAgent.clusterRegion=eu-central-1 \
  --set clusterAgent.image.repository=lacework/k8scollector \
  \
  # --- Node Collector / Runtime Agent (CWPP) ---
  --set image.repository=lacework/datacollector \
  \
  # --- Pod Scheduling Tolerations ---
  --set "tolerations[0].key=CriticalAddonsOnly" \
  --set "tolerations[0].operator=Exists" \
  --set "tolerations[0].effect=NoSchedule"

# ------------------------------------------------------------------------------
# 2) IMDS Fix — Enable host network access for Cluster Collector
# ------------------------------------------------------------------------------
# This ensures the Cluster Collector can access AWS Instance Metadata Service
# (IMDS) to retrieve node and cluster metadata for full KSPM visibility.
# Without this, you might see “Partial collection available” in the console.
# ------------------------------------------------------------------------------

echo "🔧 Enabling IMDS access for Cluster Collector..."
kubectl -n lacework patch deploy lacework-agent-cluster --type=json -p='[
  {"op":"add","path":"/spec/template/spec/hostNetwork","value":true},
  {"op":"add","path":"/spec/template/spec/dnsPolicy","value":"ClusterFirstWithHostNet"}
]'

# ------------------------------------------------------------------------------
# 3) Restart Cluster Collector to apply IMDS changes
# ------------------------------------------------------------------------------
echo "♻️ Restarting Cluster Collector deployment..."
kubectl -n lacework rollout restart deploy/lacework-agent-cluster

# ------------------------------------------------------------------------------
# ✅ Completion Message
# ------------------------------------------------------------------------------
echo "✅ Lacework Agent + KSPM deployment complete!"
echo "   - DaemonSet: lacework-agent (Node Collector + Agent)"
echo "   - Deployment: lacework-agent-cluster (Cluster Collector)"
echo "   - Verify pods with: kubectl get pods -n lacework -o wide"
echo "   - Full Collection should appear in the Lacework console within ~1 hour."






**Uninstall any Helm releases in the Lacework namespace:**
```bash
helm ls -n lacework -q | xargs -r -I{} helm uninstall {} -n lacework
```

## ⚙️ Resources Required for EKS KSPM  Integration

| **KSPM Components**         | **Purpose / Function**                                                                                         | **Deployment Method**                                                 | **Privileges / Network Access**                                                                              | **Collection Frequency**        | **Data Sent to FortiCNAPP**             | **Key Requirements / Notes**                                                                                |
| --------------------- | -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------- | --------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Cloud Collector**   | Enumerates and assesses EKS clusters using existing **CSPM (Cloud Configuration Integration)** for compliance. | Automatically available once AWS Configuration Integration is set up. | Runs as part of the cloud integration (no pod deployment required).                                          | Daily (based on CSPM schedule). | Within 24 hours of configuration setup. | Requires AWS  Configuration Integration. No additional setup for EKS.                                 |
| **Node Collector**    | Collects **node-level data** (configurations, workloads, metadata) from each node in the EKS cluster.          | **Helm or Terraform** (not DaemonSet).                                | Runs as a **privileged pod** using the **host network namespace**.                                           | Every hour.                     | Within 2 hours of installation.         | Requires access to the **Instance Metadata Service (IMDS)**. Must be deployed on each cluster.              |
| **Cluster Collector** | Collects **cluster-wide configuration and API data** (RBAC, resources, policies).                              | **Helm or Terraform**                                                 | Runs as a **non-privileged pod** using the **pod network namespace** (can use host network if IMDS blocked). | Every 24 hours.                 | Within 2 hours of installation.         | Requires access to both the **Kubernetes API Server** and **IMDS**. If IMDS blocked → *Partial Collection*. |  

------
------

## 🛠️ FortiCNAPP EKS KSPM Troubleshooting


| **Notes**           | **Description**                                                                                                                                                                                                                                                                                                                                                                                               |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Full Collection**    | All three collectors (**Cloud**, **Node**, **Cluster**) are installed and actively sending data — complete Kubernetes compliance visibility.                                                                                                                                                                                                                                                                  |
| **Partial Collection** | One or more collectors (usually Node or Cluster) are missing or misconfigured — limited compliance visibility in FortiCNAPP.                                                                                                                                                                                                                                                                                  |
| **No Collection**      | Cloud Configuration Integration (CSPM) not set up — FortiCNAPP cannot detect or enumerate EKS clusters.                                                                                                                                                                                                                                                                                                       |
| **Common Issue**       | ⚠️ **Error Message:** `Partial collection available. The node collector has not been configured.`<br><br>**Cause:** This occurs when the `lacework-agent-cluster` pod cannot reach the **AWS Instance Metadata Service (IMDS)**.<br><br>**Resolution:** Ensure IMDS access is allowed from pods. Verify that network policies, service meshes, or firewalls are not blocking access to the metadata endpoint. |  

------

**To verify IMDS access, run:**
```bash
kubectl -n lacework exec deploy/lacework-agent-cluster -- sh -lc 'T=$(curl -s --connect-timeout 2 -X PUT http://169.254.169.254/latest/api/token -H "X-aws-ec2-metadata-token-ttl-seconds:60" || true); [ -n "$T" ] && { printf "instance_id: "; curl -s --connect-timeout 2 -H "X-aws-ec2-metadata-token: $T" http://169.254.169.254/latest/meta-data/instance-id || echo ERR; } || echo TOKEN_FAIL'
```
✅ If the output shows something like: instance_id: i-xxxxxxxxxxxx, IMDS access is working correctly.  
⚠️ If you see TOKEN_FAIL or ERR, IMDS is blocked — check NetworkPolicies/CNI rules/firewall settings restricting access to 169.254.169.254.  
   **Enable lacework-agent-cluster Pod IMDS access, run:** This Enables IMDS access for the lacework-agent-cluster pod:

```bash
kubectl -n lacework patch deploy lacework-agent-cluster --type=json -p='[
  {"op":"add","path":"/spec/template/spec/hostNetwork","value":true},
  {"op":"add","path":"/spec/template/spec/dnsPolicy","value":"ClusterFirstWithHostNet"}
]'
kubectl -n lacework rollout restart deploy/lacework-agent-cluster
```
**hostNetwork**: true makes the pod use the node’s network namespace, so calls to 169.254.169.254 (IMDS) go out exactly like they would from the node.

-----
-----

**Check Nodes and Cluster Lacework Pods:**
```bash
kubectl get pods -o wide -n lacework

NAME                                     READY   STATUS    RESTARTS   AGE   IP              NODE                  NOMINATED NODE   READINESS GATES
lacework-agent-9p2cl                     1/1     Running   0          18h   172.31.15.1     i-084f64ad869c04a64   <none>           <none>
lacework-agent-cluster-fcb8d8f7c-59bwv   1/1     Running   0          6s    172.31.15.1     i-084f64ad869c04a64   <none>           <none>
lacework-agent-svtnk                     1/1     Running   0          18h   172.31.34.187   i-0c0fa636d2fbd7808   <none>           <none>
lacework-agent-vlbxm                     1/1     Running   0          18h   172.31.15.62    i-08b86b7b9ee759e7a   <none>           <none>
kobe@HussamElKebbis-MacBook-Pro deploy-kspm-imsd % 
```bash
