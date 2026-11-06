terraform {
  required_version = ">= 1.5.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

locals {
  # Key each VM by "<resource_group>/<vm_name>" so the same VM name can exist in different RGs
  vms = { for vm in var.vms : "${vm.resource_group_name}/${vm.name}" => vm }

  defender_flag = var.exclude_from_defender ? " -Defender" : ""

  # Install - command from Fortinet doc "Installing Windows Agent with Azure Resource Manager"
  install_command = join("", [
    "powershell -ExecutionPolicy Unrestricted -File Install-LWDataCollector.ps1",
    " -MSIURL ${var.agent_msi_url}",
    " -AccessToken ${var.agent_access_token}",
    " -ServerURL ${var.agent_server_url}",
    local.defender_flag,
  ])

  # Uninstall - script from Fortinet doc "Uninstalling the Windows agent",
  # with a guard so the extension succeeds when the agent is already absent
  uninstall_script = <<-EOT
    $apps = Get-WmiObject -Class Win32_Product -Filter "Name like '%Lacework%'"
    if (-not $apps) { Write-Output 'FortiCNAPP agent not installed - nothing to do'; exit 0 }
    foreach ($app in $apps) {
      $result = $app.Uninstall()
      if ($result.ReturnValue -ne 0) { Write-Error "Uninstall of $($app.Name) failed: $($result.ReturnValue)"; exit 1 }
    }
    Write-Output 'FortiCNAPP agent uninstalled'
  EOT

  # EncodedCommand avoids nested-quote escaping inside commandToExecute
  uninstall_command = "powershell -ExecutionPolicy Unrestricted -NoProfile -EncodedCommand ${textencodebase64(local.uninstall_script, "UTF-16LE")}"
}

data "azurerm_virtual_machine" "target" {
  for_each = local.vms

  name                = each.value.name
  resource_group_name = each.value.resource_group_name
}

# One Custom Script Extension per VM. Flipping install_agent changes its settings,
# which makes Azure re-run the extension with the install or uninstall command.
resource "azurerm_virtual_machine_extension" "forticnapp_agent" {
  for_each = local.vms

  name                       = var.extension_name
  virtual_machine_id         = data.azurerm_virtual_machine.target[each.key].id
  publisher                  = "Microsoft.Compute"
  type                       = "CustomScriptExtension"
  type_handler_version       = "1.10"
  auto_upgrade_minor_version = true

  # protected_settings is encrypted by Azure, so the access token is never shown in the portal
  protected_settings = var.install_agent ? jsonencode({
    fileUris         = [var.install_script_url]
    commandToExecute = local.install_command
    }) : jsonencode({
    commandToExecute = local.uninstall_command
  })

  tags = var.tags

  lifecycle {
    precondition {
      condition     = !var.install_agent || length(var.agent_access_token) > 0
      error_message = "agent_access_token is required when install_agent = true (export TF_VAR_agent_access_token)."
    }
  }
}
