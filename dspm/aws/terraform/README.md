# Terraform for Integrating Single Region AWS Data Security Posture Management (DSPM) with FortiCNAPP

## Overview

This Code creates the necessary AWS resources for DSPM scanning, including:

- Lacework cloud account integration
- ECS Cluster on AWS Fargate for scanner tasks
- EventBridge Rule for scheduled scanning
- S3 bucket for scan results
- Secret Manager secret for Lacework credentials
- DynamoDB table for scanner cache
- VPC and networking configuration
- Required IAM roles and policies

## Instructions

Follow these steps to deploy:

1. Rename the file `terraform.tfvars.txt` to `terraform.tfvars`.
2. Fill in the required variables in `terraform.tfvars` file:
    - scanning_account_id: AWS account ID where DSPM scanner will be deployed
    - regions : Regions where DSPM scanners is deployed
3. (Optional) Use the global_region variable to define the region for global resources (such as S3 buckets) when deploying DSPM in a multi-region setup. By default, it is set to the first region listed in regions variable. Leave this value empty when deploying in a single-region configuration.
4. (Optional) Customize your deployment: Default values are provided for all optional variables, but you may want to customize some of them:
    - lacework_integration_name
    - resource_prefix
    - tags 

You can also adjust scanning setting or ecs task sizing.
Only modify other variables if necessary. Refer to variables.tf for variable types and descriptions.

5. Run the following commands:
<code><pre>
   terraform init
   terraform plan
   terraform apply
</code></pre>

You can delete the integration and remove all created resources using the following command:
<code><pre>
   terraform destroy
</code></pre>