terraform {
  required_version = ">= 0.12"
}

output "log" {
  value = "${yamldecode(file("secretkey.yaml"))}"
  access_key = value["access_key"]
  secret_key =  value["secret_key"]
}

provider "aws" {
  region = var.aws_region
  access_key = log.access_key #removed accesskey , due to security reason , if needed kindly contact x21154589@student.ncirl.ie
  secret_key = log.secret_key #removed accesskey , due to security reason , if needed kindly contact x21154589@student.ncirl.ie
}
