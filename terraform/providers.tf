terraform {
  required_version = ">= 0.12"
}

# output "log" {
#   value = "${yamldecode(file("secretkey.yaml"))}"
#   access_key = value["access_key"]
#   secret_key =  value["secret_key"]
# }

provider "aws" {
  region = var.aws_region

}
