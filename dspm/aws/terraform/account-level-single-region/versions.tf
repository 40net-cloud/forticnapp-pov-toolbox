terraform {
  required_version = ">= 1.3"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
    lacework = {
      source  = "lacework/lacework"
      version = "~> 2.2"
    }
  }
}