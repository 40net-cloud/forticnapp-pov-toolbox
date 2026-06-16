
Note: Never delete terraform.tfstate if you may need to run terraform destroy later. Only .terraform/ is considered disposable cache.


| **Step**                                                    | **Action / Command**                                                                                                  | **Purpose / Notes**                                                                                                                                               |
| ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 🧩 **1. Check CloudShell storage**                          | `df -h`                                                                                                               | Verify the limited persistent CloudShell storage. Example: `/dev/loop0 974M 146M 761M 17% /home/cloudshell-user`.                                                 |
| 📁 **2. Go to the Terraform project directory**             | `cd /home/cloudshell-user/lacework/aws-xxxx`                                                                          | Run all Terraform commands from the directory that contains `main.tf`.                                                                                            |
| 📊 **3. Check current folder sizes**                        | `du -sh .[!.]* * 2>/dev/null \| sort -hr`                                                                             | Shows all visible and hidden files/folders with sizes. Useful to detect if `.terraform/` is consuming large space, for example `742M .terraform`.                 |
| 🧹 **4. Create temporary Terraform cache before init**      | `mkdir -p /tmp/terraform-cache`                                                                                       | Creates a temporary cache location outside the limited `/home/cloudshell-user` storage.                                                                           |
| 🔗 **5. Create `.terraform` symlink if it does not exist**  | `ln -s /tmp/terraform-cache .terraform`                                                                               | Redirects Terraform's `.terraform/` directory to `/tmp/terraform-cache`. This must be done before `terraform init` if `.terraform` does not already exist.        |
| ✅ **6. Verify the symlink**                                 | `ls -la`                                                                                                              | Confirm expected output: `.terraform -> /tmp/terraform-cache`.                                                                                                    |
| 📦 **7. Initialize and deploy Terraform**                   | `terraform init`<br>`terraform apply`                                                                                 | Terraform uses `.terraform`, which now points to `/tmp/terraform-cache`.                                                                                          |
| 📊 **8. Check Terraform cache size after init**             | `du -sh .[!.]* * 2>/dev/null \| sort -hr`                                                                             | Confirms whether `.terraform` is a large local directory or a symlink to `/tmp`.                                                                                  |
| 🗑️ **9. If `.terraform` already exists as a large folder** | `rm -rf .terraform`<br>`mkdir -p /tmp/terraform-cache`<br>`ln -s /tmp/terraform-cache .terraform`<br>`terraform init` | `.terraform/` is disposable cache. You can delete it and recreate it with `terraform init`.                                                                       |
| ⚠️ **10. Session restart behavior**                         | `mkdir -p /tmp/terraform-cache`                                                                                       | `/tmp` is temporary. After CloudShell restart, the symlink may still exist but the target may be gone. Recreate the target folder before running Terraform again. |
| 🔗 **10.5 Verify or recreate `.terraform` symlink**         | `ls -la`<br>`ln -s /tmp/terraform-cache .terraform`                                                                   | Verify that `.terraform -> /tmp/terraform-cache` exists. If the symlink is missing, recreate it before running `terraform init`.                                  |
| 📁 **11. Keep essential Terraform files**                   | Keep: `main.tf`, `terraform.tfstate`, `terraform.tfstate.backup`, `.terraform.lock.hcl`, `tfplan.json` if needed      | Do **not** delete `terraform.tfstate` if you may need future `terraform destroy`, `plan`, `apply`, or updates. Only `.terraform/` is disposable cache.            |

````
Example:

```bash
$ cd /home/cloudshell-user/lacework/aws-997159613128

$ du -sh .[!.]* * 2>/dev/null | sort -hr
742M    .terraform
288K    terraform.tfstate
60K     tfplan.json
8.0K    .terraform.lock.hcl
4.0K    main.tf

$ mkdir -p /tmp/terraform-cache
$ ln -s /tmp/terraform-cache .terraform

$ ls -la
lrwxrwxrwx. 1 cloudshell-user cloudshell-user 20 Jun 10 11:55 .terraform -> /tmp/terraform-cache
````
