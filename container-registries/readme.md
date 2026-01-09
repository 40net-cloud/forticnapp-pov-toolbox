# Platform Scanner Overview

The **Lacework FortiCNAPP Platform Scanner** provides automated vulnerability scanning for container images stored in **public and internet-accessible container registries**. Images are scanned as they are added to the registry once an integration is configured.

> ⚠️ **Note**  
> You must integrate the registry that hosts the repositories containing the images you want to scan, including public registries.

---

## Image Scanning Methods

Depending on the registry type, Lacework FortiCNAPP supports:

- **Registry Notification** – Triggers a scan when the registry sends an event for a newly uploaded image.
- **Auto-Polling** – Discovers and scans new images every **15 minutes**, including some existing images.
- **On-Demand Scans** – Manually trigger scans via the Console or CLI.

---

## Supported Container Registries

Supports **Docker image manifest V2, schema 2** registries.

| Registry | Scan Types |
|--------|-----------|
| Amazon ECR | Auto-polling, On-demand |
| Azure Container Registry (Docker V2) | Registry notification, On-demand |
| Docker Hub | Auto-polling, On-demand |
| Docker V2 Registry / Auth Registries | Registry notification, On-demand |
| GitHub Container Registry | Registry notification, On-demand |
| GitLab (Docker V2) | Registry notification, On-demand |
| Google Artifact Registry / GCR | Auto-polling, On-demand |
| JFrog (Docker V2) | Auto-polling (limited), Registry notification, On-demand |

---

## Multi-Architecture Support

Multi-architecture images are supported. The scanner evaluates the first available architecture in this order:

1. AMD64  
2. ARM64  
3. ARM32  

---

## Auto-Polling vs. Registry Notification

- **Registry Notification**: Scans images immediately after upload.
- **Auto-Polling**: Scans new images every 15 minutes and may include existing images.

Both methods publish results to the Lacework FortiCNAPP Console. On-demand scans can always be used for existing images.

---

## Docker API v2

Lacework FortiCNAPP uses **Docker API v2** to pull images. Registry integrations must support Docker v2 authentication and APIs to enable auto-polling or notifications.

---

## Default Scanning Limits

- **Max repositories per integration**: 2000  
  - Amazon ECR: 1000
- **Per-repository scan rate**: 100 images/hour
- **Account-wide limit**: 1200 images/hour





Example On-Demand: CLI Command   ( lacework vulnerability container scan repo/image)

 lacework vulnerability container scan quay.io quay/busybox latest  
 lacework vulnerability container scan index.docker.io dockerfabric/hello-app latest 
