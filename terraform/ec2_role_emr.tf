## create IAM role
resource "aws_iam_role" "ec2_test_role" {
  name = "ec2_test_role"

  assume_role_policy = <<EOF
    {
    "Version": "2012-10-17",
    "Statement": [
        {
        "Action": "sts:AssumeRole",
        "Principal": {
            "Service": "ec2.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
        }
    ]
    }
    EOF

    tags = {
        tag-key = "tag-value"
    }
    }

#Create EC2 Instance Profile
resource "aws_iam_instance_profile" "ec2_test_profile" {
  name = "ec2_test_profile"
  role = aws_iam_role.ec2_test_role.name
}

#Adding IAM Policies
#To give full access to S3 bucket
resource "aws_iam_role_policy" "ec2_test_policy" {
  name = "ec2_test_policy"
  role = aws_iam_role.ec2_test_role.id

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "elasticmapreduce:DescribeStep",
                "iam:PassRole",
                "elasticmapreduce:AddJobFlowSteps"
            ],
            "Resource": [
                "arn:aws:elasticmapreduce:*:505316317378:cluster/*",
                "arn:aws:iam::505316317378:role/EMR_EC2_DefaultRole",
                "arn:aws:iam::505316317378:role/EMR_DefaultRole"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "elasticmapreduce:RunJobFlow",
            "Resource": "*"
        },
        { "Effect": "Allow",
            "Resource": "*",
            "Action": [
                "s3:CreateBucket",
                "s3:Get*",
                "s3:List*"
               
            ]
        }
    ]
}
EOF
}

#Attach this role to EC2 instance
# resource "aws_instance" "role-test" {
#   ami = "ami-0bbe6b35405ecebdb"
#   instance_type = "t2.micro"
#   iam_instance_profile = "${aws_iam_instance_profile.test_profile.name}"
#   key_name = "mytestpubkey"
# }