# Deploy with OCI Cloud Shell

Deploy the FortiCNAPP OCI integration directly from [OCI Cloud Shell](https://cloud.oracle.com/) — no local tooling required. Cloud Shell comes with Terraform, Git, and the OCI CLI pre-installed.

## What gets deployed

This Terraform uses the [`lacework/config/oci`](https://registry.terraform.io/modules/lacework/config/oci/latest) module to integrate your OCI tenancy with FortiCNAPP for cloud resource configuration assessment (CSPM). It creates:

**In OCI (tenancy level):**
- An IAM user dedicated to the integration, with an API signing key (named `lw_cspm_user` by default)
- An IAM group containing that user (`lw_cspm_group`)
- An IAM policy granting the group read-only access to tenancy resources (`lw_cspm_policy`)

**In FortiCNAPP:**
- An OCI CSPM cloud account integration (labeled `OCI CSPM Integration` by default), configured with the credentials of the IAM user above

Resource names can be customized via `name_prefix` or the individual `user_name`, `group_name`, and `policy_name` variables. No compute, network, or agent resources are deployed — this is an agentless, API-based integration.

## Prerequisites

- OCI user with permissions to create IAM resources (policies, groups, users)
- An OCI API key pair — [generate one](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm) under **Identity → My Profile → API Keys** and download the private key (`.pem`)
- FortiCNAPP API credentials (account, API key, API secret)

## 1. Open Cloud Shell

Log in to the OCI Console and click the **Cloud Shell** icon (`>_`) in the top-right toolbar.

## 2. Clone the Terraform example

Clone only the `OCI/terraform` directory using sparse checkout:

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/40net-cloud/forticnapp-pov-toolbox.git
cd forticnapp-pov-toolbox
git sparse-checkout set OCI/terraform
cd OCI/terraform
```

## 3. Upload your API private key

Use the Cloud Shell menu (**⋮ → Upload**) to upload your `.pem` private key. Uploaded files land in your home directory — locate it if needed:

```bash
find ~ -name "*.pem" 2>/dev/null
```

Secure the key:

```bash
chmod 600 ~/oci-key.pem
```


## 4. Configure variables

```bash
cp terraform.tfvars.example terraform.tfvars
nano terraform.tfvars
```

Cloud Shell exposes several values you need as environment variables:

```bash
echo $OCI_TENANCY   # tenancy_id
echo $OCI_REGION    # region — use your tenancy HOME region for IAM writes
```

For direct API-key auth, set `config_file_profile = ""` and fill in `oci_user_ocid`, `oci_fingerprint`, and `oci_private_key_path` (absolute path, e.g. `/home/your_user/oci-key.pem`). Also set `tenancy_id`, `region`, `user_email`, and your FortiCNAPP credentials (`lw_account`, `lw_api_key`, `lw_api_secret` — or leave them empty to fall back to `~/.lacework.toml` or `LW_*` environment variables).

## 5. Deploy

```bash
terraform init
terraform plan
terraform apply
```

Type `yes` when prompted. The integration appears in the FortiCNAPP console under **Settings → Cloud accounts** within a few minutes.

## Cleanup

To remove all resources created by this example:

```bash
terraform destroy
```
