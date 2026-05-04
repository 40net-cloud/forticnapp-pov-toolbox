## ⚙️ Terraform Deployment in CloudShell (1 GB Limit Workaround)

| **Step**                                   | **Action / Command**                                                                                                                      | **Purpose / Notes**                                                                                                   |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| 🧩 **1. Understand the limitation**        | `/home/cloudshell-user/lacework/aws-xxxxx` has only **~1 GB** of persistent space.                                                                           | Large `.terraform/` directories (provider cache) quickly fill this up.                                                |
| 🧹 **2. After deployment**                 | `du -hs .*` → shows `.terraform` size.<br>`rm -rf .terraform`                                                                              | Safe to delete `.terraform/` after a successful deploy. It can always be re-initialized.                              |
| 📦 **3. Keep only essential files**        | Keep `main.tf`, `terraform.tfstate`, and `.terraform.lock.hcl` in `/home/cloudshell-user`.                                                | These are lightweight and needed for later destruction or updates.                                                    |
| 🚚 **4. Before destroying infrastructure** | 1️⃣ Create a temp folder with more space:<br>`mkdir -p /tmp/forti`<br>2️⃣ Move the project:<br>`mv /home/cloudshell-user/awls /tmp/forti` | `/tmp`, `/root`, or `/aws/mde/mde` usually have tens of GB free. `-p` ensures the folder path exists even if missing. |
| 🔄 **5. Re-initialize Terraform**          | `terraform init`                                                                                                                          | Re-downloads providers and recreates the `.terraform/` folder.                                                        |
| 💣 **6. Destroy resources**                | `terraform destroy`                                                                                                                       | Cleanly removes deployed cloud resources.                                                                             |
| ✅ **Result**                               | Efficient use of CloudShell’s limited storage while maintaining full deploy/destroy capability.                                           | Keeps environment lightweight and reproducible.                                                                       |


The command is "ls -laih"
"du -sh *
