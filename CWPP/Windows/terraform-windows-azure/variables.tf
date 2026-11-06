variable "subscription_id" {
  description = "Azure subscription ID that holds the target VMs."
  type        = string
}

variable "install_agent" {
  description = "true = install the FortiCNAPP Windows agent, false = uninstall it."
  type        = bool
  default     = true
}

variable "vms" {
  description = "Existing Windows VMs to manage."
  type = list(object({
    name                = string
    resource_group_name = string
  }))

  validation {
    condition     = length(var.vms) > 0
    error_message = "Provide at least one VM."
  }
}

variable "install_script_url" {
  description = "URL of Install-LWDataCollector.ps1 for the chosen release (FortiCNAPP Windows agent releases page)."
  type        = string

  validation {
    condition     = startswith(var.install_script_url, "https://")
    error_message = "install_script_url must be an https URL."
  }
}

variable "agent_msi_url" {
  description = "URL of LWDataCollector.msi for the chosen release (FortiCNAPP Windows agent releases page)."
  type        = string

  validation {
    condition     = startswith(var.agent_msi_url, "https://")
    error_message = "agent_msi_url must be an https URL."
  }
}

variable "agent_access_token" {
  description = "FortiCNAPP agent access token. Required for install only. Pass via TF_VAR_agent_access_token."
  type        = string
  default     = ""
  sensitive   = true
}

variable "agent_server_url" {
  description = "FortiCNAPP agent server URL for your region."
  type        = string
  default     = "https://api.lacework.net"

  validation {
    condition     = startswith(var.agent_server_url, "https://")
    error_message = "agent_server_url must be an https URL."
  }
}

variable "exclude_from_defender" {
  description = "Pass -Defender to exclude the agent from Microsoft Defender scanning."
  type        = bool
  default     = true
}

variable "extension_name" {
  description = "Name of the Custom Script Extension on each VM."
  type        = string
  default     = "forticnapp-agent"
}

variable "tags" {
  description = "Tags applied to the VM extensions."
  type        = map(string)
  default     = {}
}
