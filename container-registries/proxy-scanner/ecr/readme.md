:wave: [Introduction](#introduction) • [Amazon ECR](#amazon-elastic-container-registry-ecr) • [ECR Integration with FortiCNAPP](#ecr-integration-with-forticnapp) • [Deploy the Proxy Scanner](#deploy-the-proxy-scanner) • [Validate the Integration](#validate-the-integration)

# Proxy Scanner Integration with Amazon Elastic Container Registry (ECR) 

## Introduction

The FortiCNAPP Proxy Scanner integration enables vulnerability assessments of Docker image registries without exposing them to external networks. It runs as a Docker container or Kubernetes workload within your environment and continuously scans new images. The scanner extracts required image metadata locally and sends it securely to FortiCNAPP using an integration token. FortiCNAPP analyzes the metadata and provides risk assessments in the Vulnerability Assessment page of the Console. This approach optimizes bandwidth by avoiding full image transfers.

## Deployment

### Amazon Elastic Container Registry (ECR)

- Create a private repository from aws cli using command [Link](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html)

```bash
aws ecr create-repository --repository-name <name> --region <region>
```

![Private Repository AWS](images/AWS-ECR.png)

- Authenticate your Docker client to the Amazon ECR registry to which you intend to push your image.

```bash
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com
```

- List available images

```bash
docker images
```
- Tag image 

```bash
docker tag e9ae3c220b23 <aws_account_id>.dkr.ecr.<region>.amazonaws.com/my-repository:tag
```

- Push image to repository

```bash
docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/<prefix/my-new-repository:tag>
```
More information can be found from [link.](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html)

## ECR Integration with FortiCNAPP 

**AWS**

- In the navigation pane of the console, choose Roles and then choose Create role

- Select trusted entitiy type "AWS Service" and Use Case "EC2".

- Add permission "AmazonEC2ContainerRegistryReadOnly" 

![IAM Roles Permission Policy](images/AWS-Roles-Policies.png)

- Enter a role name and then create role.

- Create a proxy scanner linux machine and attache the created role to it.

![AWS Trusted Entities](images/AWS-Roles-Trustrelations.png)

**FortiCNAPP**

- Navigate to: Setting -> Containers registries 

- Select Proxy Scanner.

- Enter a Name for the integration 

- Download credentials.json or Copy the authorization token and keep it to paste it later in config.yml file in proxy scanner VM.

![FortiCNAPP Token](images/FortiCNAPP-Token.png)

For more information, refer to the official documentation at the following [link](https://docs.fortinet.com/document/forticnapp/latest/administration-guide/321350/integrate-proxy-scanner)

## Deploy the Proxy Scanner

- Before you deploy the proxy scanner, ensure that you set up a host machine with Docker installed.

- Pull the latest FortiCNAPP proxy scanner image:
```bash
docker pull lacework/lacework-proxy-scanner:latest
```
- Create a persistent storage location for the FortiCNAPP proxy scanner cache and change the ownership:
```bash
mkdir cache
chown -R 1000:65533 cache
```
- Create config.yml and add the content to it:

```json 
static_cache_location: /opt/lacework
default_registry:
lacework:
  account_name: <account_name>
  integration_access_token: <integration_access_token>
registries:
  - domain: <aws_account_id>.dkr.ecr.<region>.amazonaws.com
    name: my-proxy-ecr-integration
    auth_type: ecr
    is_public: false
    ssl: true
    auto_poll: true
    credentials:
      use_local_credentials: true
    disable_non_os_package_scanning: false
    go_binary_scanning:
      enable: true
```
account_name: Lacework account name from your Lacework FortiCNAPP URL <account_name>.lacework.net
integration_access_token: The integration's access token from the Lacework Console


- Start the FortiCNAPP proxy scanner:

```bash
docker run -d --mount type=bind,source="$(pwd)"/cache,target=/opt/lacework/cache -v "$(pwd)"/config.yml:/opt/lacework/config/config.yml -p 8080:8080 lacework/lacework-proxy-scanner
```
- For debugging purposes, add -e LOG_LEVEL=debug:
```bash
docker run -e LOG_LEVEL=debug -d --mount ...
```

## Validate the Integration

Navigate to : Vulnerabilities -> Containers

![FortiCNAPP-ECR-vulnerabilities-containers](images/FortiCNAPP-ECR-vulnerabilities-containers.png)

- The following command requests an on-demand container vulnerability scan and waits for the scan to completeon-demand
```bash
curl --location --request POST 'YourHost:8080/v1/scan' \
--header 'Content-Type: application/json' \
--data-raw '{
    "registry": "YourRegistry",
    "image_name": "YourRepository/YourImage",
    "tag": "YourValue"
}'
```
- To view all container vulnerability assessments for your Lacework FortiCNAPP account for the last 24 hours (default):
```bash
lacework vulnerability container list-assessments
```
- To view a specific container vulnerability assessment use the command.
```bash
lacework vulnerability container show-assessment <sha256:hash>
```
Additional details are available in the official documentation [link](https://docs.fortinet.com/document/forticnapp/latest/cli-reference/861350/container-vulnerability)





