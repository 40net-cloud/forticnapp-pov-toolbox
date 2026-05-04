| **Step** | **Action / Command** | **Purpose / Notes** |
|---------|----------------------|---------------------|
| 🧩 **1. Understand the limitation** | `/home/cloudshell-user/` has only ~1 GB persistent storage | AWS CloudShell keeps this directory between sessions, but it is very limited. Terraform provider caches (`.terraform/`) can quickly consume all space. |
| 📦 **2. Deploy your Terraform** | `terraform init`<br>`terraform apply` | Run Terraform normally inside `/home/cloudshell-user/...` project directory. This will create `.terraform/` locally (large size). |
| 📊 **3. Check disk usage** | `du -sh .terraform` | Verify how much space `.terraform/` is consuming (often hundreds of MB). |
| 🧹 **4. Move heavy cache to /tmp (ephemeral)** | `mv .terraform /tmp/terraform-cache` | `/tmp` has much larger space (~20+ GB) but is **not persistent**. This avoids filling CloudShell storage. |
| 🔗 **5. Create symlink back** | `ln -s /tmp/terraform-cache .terraform` | Terraform still expects `.terraform/` in project directory, so we link it back. |
| 🔁 **6. Reuse in same session** | `ls -la` | Confirms `.terraform -> /tmp/terraform-cache` symlink is active. Works fine during current session. |
| ⚠️ **7. Session restart behavior** | *(No command)* | `/tmp` is wiped when CloudShell restarts → `.terraform` will be broken and must be recreated. |
| 🔄 **8. Reinitialize if needed** | `rm -f .terraform`<br>`terraform init` | If symlink breaks after restart, remove it and re-run init to rebuild providers. |
| 🧹 **9. Optional cleanup after deploy** | `rm -rf .terraform` | Safe to delete after successful deployment if no further Terraform actions are needed immediately. |
| 📁 **10. Keep only essential files** | Keep: `main.tf`, `terraform.tfstate`, `.terraform.lock.hcl` | These are small and required for future `terraform destroy` or updates. |
