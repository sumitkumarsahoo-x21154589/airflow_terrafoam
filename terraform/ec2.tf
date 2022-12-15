# 9. Create Ubuntu server and install/enable apache2

resource "aws_instance" "web-server-instance" {
  ami               = "ami-085925f297f89fce1"
  instance_type     = "c3.large"
  availability_zone = "us-east-1a"
  key_name          = "test_ec2_key_pair"
  iam_instance_profile = aws_iam_instance_profile.ec2_test_profile.name

  network_interface {
    device_index         = 0
    network_interface_id = aws_network_interface.web-server-nic.id
  }

  user_data = <<-EOF
                #!/bin/bash
                sudo apt update -y
                sudo apt install git
                sudo apt-get remove docker docker-engine docker.io
                sudo apt-get update
                sudo apt install docker.io -y
                sudo snap install docker
                sudo apt install docker-compose -y
                sudo git clone https://github.com/sumitkumarsahoo-x21154589/airflow_terrafoam.git
                cd /airflow_terrafoam
                sudo docker-compose build
                sudo docker-compose up airflow-init
                sudo docker-compose up
                EOF
  tags = {
    Name = "web-server"
  }
}