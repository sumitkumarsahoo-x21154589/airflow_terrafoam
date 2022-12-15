terraform {
  required_version = ">= 0.12"
}

provider "aws" {
  region = var.aws_region
  access_key = ""#removed accesskey , due to security reason , if needed kindly contact x21154589@student.ncirl.ie
  secret_key = ""#removed accesskey , due to security reason , if needed kindly contact x21154589@student.ncirl.ie
}
