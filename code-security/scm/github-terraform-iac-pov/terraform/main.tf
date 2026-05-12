terraform {
  required_version = ">= 1.5.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.100"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-forticnapp-gap1"
  location = "West Europe"
}

resource "azurerm_storage_account" "forticnappstorage" {
  name                     = "yaforticnappstorage"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  # Intentional misconfiguration
  # Set public_network_access_enabled to "false" to fix the violation

  public_network_access_enabled = true

  # Add network rules to fix other violations related to Storage access

  #  network_rules {
  #    default_action            = "Deny"
  #    bypass                    = ["Metrics", "AzureServices"]
  #    }
  tags = {
    environment = "demo"
    owner       = "security-lab"
  }
}