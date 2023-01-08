
# ### passing list of buckets

# variable "s3_folders" {
#   type        = list(string)
#   description = "The list of S3 folders to create"
#   default     = ["x21154589_input", "x21154589_output","x21154589_scripts"]
# }

# resource "aws_s3_bucket" "x21154589_bucket_v2" {
#   bucket = "emrbuckettestsumitv2"
# }

# resource "aws_s3_bucket_object" "folders" {
#     count   = "${length(var.s3_folders)}"
#     bucket = aws_s3_bucket.x21154589_bucket_v2.id
#     acl    = "private"
#     key    = "${var.s3_folders[count.index]}/"
#     source = "/dev/null"
# }