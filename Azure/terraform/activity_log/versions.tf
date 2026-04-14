terraform {
  required_version = ">= 0.14"

  required_providers {
    random  = ">= 2.1"
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 3.0"
    }
    lacework = {
      source  = "lacework/lacework"
      version = "~> 2.0"
    }
  }
}