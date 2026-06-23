terraform {
  required_version = ">= 0.14"

  required_providers {
    oci = {
      source  = "oracle/oci"
      version = ">= 5.2.0"
    }
    lacework = {
      source  = "lacework/lacework"
      version = "~> 2.0"
    }
    time = {
      source  = "hashicorp/time"
      version = "~> 0.9"
    }
  }
}
