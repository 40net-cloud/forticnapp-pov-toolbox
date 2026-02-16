terraform {
  required_providers {
    lacework = {
      source = "lacework/lacework"
    }
  }
}

provider "lacework" {}

provider "aws" {}

module "lacework_ecr" {
  source  = "lacework/ecr/aws"
  version = "~> 0.9"

  iam_role_arn = var.iam_role_arn
  iam_role_external_id = var.iam_role_external_id
  iam_role_name = var.iam_role_name 
  lacework_aws_account_id = var.lacework_aws_account_id
  lacework_integration_name = var.lacework_integration_name
  limit_by_labels = var.limit_by_labels
  limit_by_repositories = var.limit_by_repositories
  limit_by_tags         = var.limit_by_tags
  limit_num_imgs = var.limit_num_imgs
  non_os_package_support = var.non_os_package_support
  registry_domain = var.registry_domain
  tags = var.tags
  use_existing_iam_role = var.use_existing_iam_role
  wait_time = var.wait_time

}