resource "aws_eip" "nat_eip" {
  vpc        = true
  depends_on = [aws_internet_gateway.ig]
  instance   = aws_instance.ec2_nat_instance.id
}
resource "aws_instance" "ec2_nat_instance" {
  ami           = "ami-0bbb886f29931c526"
  instance_type = "t3.nano"
  network_interface {
    network_interface_id = aws_network_interface.nat_ec2_network_interface.id
    device_index = 0
  }
  user_data = <<EOT
#!/bin/bash
sudo /usr/bin/apt update
sudo /usr/bin/apt install ifupdown
/bin/echo '#!/bin/bash
if [[ $(sudo /usr/sbin/iptables -t nat -L) != *"MASQUERADE"* ]]; then
  /bin/echo 1 > /proc/sys/net/ipv4/ip_forward
  /usr/sbin/iptables -t nat -A POSTROUTING -s ${aws_vpc.vpc.cidr_block} -j MASQUERADE
fi
' | sudo /usr/bin/tee /etc/network/if-pre-up.d/nat-setup
sudo chmod +x /etc/network/if-pre-up.d/nat-setup
sudo /etc/network/if-pre-up.d/nat-setup 
  EOT

  tags = {
    Name = "nat_instance"
    Role = "nat"
  }
}
resource "aws_network_interface" "nat_ec2_network_interface" {
  subnet_id = aws_subnet.public_subnet.id
  security_groups = [aws_security_group.security_group.id]
  source_dest_check = false
}
resource "aws_security_group" "security_group" {
  name = "nat_instance_security_group"
  description = "Security group for NAT instance"
  vpc_id = aws_vpc.vpc.id
  
  ingress = [
    {
      description = "Ingress CIDR"
      from_port = 0
      to_port = 0
      protocol = "-1"
      cidr_blocks = [aws_vpc.vpc.cidr_block]
      ipv6_cidr_blocks = []
      prefix_list_ids = []
      security_groups = []
      self = true
    }
  ]
  
  egress = [
    {
      description = "Default egress"
      from_port = 0
      to_port = 0
      protocol = "-1"
      cidr_blocks = ["0.0.0.0/0"]
      ipv6_cidr_blocks = []
      prefix_list_ids = []
      security_groups = []
      self = true
    }
  ]
}