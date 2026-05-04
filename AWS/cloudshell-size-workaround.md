| **Step** | **Action / Command** | **Purpose / Notes** |
|---------|----------------------|---------------------|
| 🧩 **1. Understand the limitation** | `/home/cloudshell-user` has only ~1 GB persistent storage | AWS CloudShell keeps this directory between sessions, but it is very limited. Terraform provider caches (`.terraform/`) can quickly consume all space. |
| 📦 **2. Deploy your Terraform** | `cd /home/cloudshell-user/lacework/aws-xxxx`<br>`terraform init`<br>`terraform apply` | Run Terraform inside your project directory. This creates a large `.terraform/` folder locally. |
| 📊 **3. Check disk usage** | `du -sh .terraform` | Verify how much space `.terraform/` is consuming (often hundreds of MB). |
| 🧹 **4. Move heavy cache to /tmp (ephemeral)** | `mv .terraform /tmp/terraform-cache` | `/tmp` has much larger space (~20+ GB) but is **not persistent**. This prevents CloudShell storage from filling up. |
| 🔗 **5. Create symlink back** | `ln -s /tmp/terraform-cache .terraform` | Terraform expects `.terraform/` in the project directory, so we link it back. |
| 🔁 **6. Reuse in same session** | `ls -la` | Confirms `.terraform -> /tmp/terraform-cache` symlink is active and usable during the session. |
| ⚠️ **7. Session restart behavior** | *(No command)* | `/tmp` is wiped when CloudShell restarts → symlink breaks and `.terraform` must be recreated. |
| 🔄 **8. Reinitialize if needed** | `rm -f .terraform`<br>`terraform init` | After restart, remove broken symlink and reinitialize providers. |
| 🧹 **9. Optional cleanup after deploy** | `rm -rf .terraform` | Safe to delete after successful deployment if no further Terraform actions are needed immediately. |
| 📁 **10. Keep only essential files** | Keep: `main.tf`, `terraform.tfstate`, `.terraform.lock.hcl` | These are lightweight and required for future `terraform destroy` or updates. |
