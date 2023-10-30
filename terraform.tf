provider "aws" {
  region     = "us-east-2"
  access_key = "AKIARBT534H7I57XYHG7"
  secret_key = "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"
}

resource "aws_instance" "webapp" {
  ami           = "ami-0430580de6244e02e"
  instance_type = "t2.micro"
  vpc_security_group_ids = [
    "sg-05fab7c3d57ce50b8"
  ]
  user_data = <<-EOF
            #!/bin/bash
            sudo apt-get update
            sudo apt-get install git python3 python3-pip -y
            pip3 install --upgrade pip
            git clone https://github.com/IvanPdrk/webapp.git /home/ubuntu/app
            cd /home/ubuntu/app
            sudo apt-get install python3-venv -y
            python3 -m venv venv
            source venv/bin/activate
            pip install -r requirements.txt
            cd src/
            chmod +x crud.py
            python3 crud.py
            EOF
    // This attaches a public IP to the instance
  associate_public_ip_address = true
  tags = {
    Name = "Terraform_instance"
  }
}


output "public_ip" {
  value = aws_instance.webapp.public_ip
}
