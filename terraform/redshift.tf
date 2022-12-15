
## creating s3 full access policy

resource "aws_iam_role_policy" "s3_full_access_policy" {
  name = "redshift_s3_policy"
  role = "${aws_iam_role.redshift_role.id}"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": "*"
        }
    ]
}
EOF
}

## assigning the role

resource "aws_iam_role" "redshift_role" {
  name = "redshift_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "redshift.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF

  tags = {
    tag-key = "redshift-role"
  }
}


resource "aws_subnet" "redshift_subnet_2" {
            vpc_id     = aws_vpc.prod-vpc.id
            cidr_block = "10.0.2.0/24"
            availability_zone = "us-east-1b"
            tags = {
                Name = "redshift-subnet-2"
            }
            }

resource "aws_redshift_subnet_group" "redshift_subnet_group" {
  name       = "redshift-subnet-group"
  subnet_ids = [aws_subnet.subnet-1.id,
                  aws_subnet.redshift_subnet_2.id]
        tags = {
            environment = "dev"
            Name = "redshift-subnet-group"       
        }
        }

resource "aws_redshift_cluster" "default" {
  cluster_identifier = "x21154589-sample-cluster"
  database_name      = "x21154589_sample_cluster_db"
  master_username    = "x21154589_sample_cluster_db_user"
  master_password    = "x21154589_sample_cluster_db_Pwd"
  node_type          = "dc2.large"
  cluster_type       = "single-node"
  cluster_subnet_group_name = aws_redshift_subnet_group.redshift_subnet_group.id
  skip_final_snapshot = true
  iam_roles = ["${aws_iam_role.redshift_role.arn}"]

}
