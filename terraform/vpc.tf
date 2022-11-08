resource "aws_vpc" "vpc" {
  cidr_block = "10.100.0.0/16"
  tags = {
    Name = "Kraken DCA VPC"
  }
}
/* Public and private subnets */
resource "aws_subnet" "private_subnet" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = "10.100.0.0/24"
  map_public_ip_on_launch = false

  tags = {
    Name = "Kraken DCA private Subnet"
  }
}

resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = "10.100.1.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "Kraken DCA public Subnet"
  }
}
/* Internet gateway for public subnet */
resource "aws_internet_gateway" "ig" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name = "Kraken DCA internet gateway"
  }
}

/* Routing table for private subnet */
resource "aws_route_table" "private_subnet_route_table" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name = "Kraken-DCA-private-subnet-route-table"
  }
}
/* Routing table for public subnet */
resource "aws_route_table" "public_subnet_route_table" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name = "Kraken-DCA-public-subnet-route-table"
  }
}
resource "aws_route" "public_internet_gateway" {
  route_table_id         = aws_route_table.public_subnet_route_table.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.ig.id
}
resource "aws_route" "private_nat_instance" {
  route_table_id         = aws_route_table.private_subnet_route_table.id
  destination_cidr_block = "0.0.0.0/0"
  network_interface_id   = aws_instance.ec2_nat_instance.id
}
/* Route table associations */
resource "aws_route_table_association" "public_route_table_association" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_subnet_route_table.id
}
resource "aws_route_table_association" "private_route_table_association" {
  subnet_id      = aws_subnet.private_subnet.id
  route_table_id = aws_route_table.private_subnet_route_table.id
}
/* Security Group */
resource "aws_default_security_group" "default_security_group" {
  vpc_id = aws_vpc.vpc.id

  ingress {
    protocol  = -1
    self      = true
    from_port = 0
    to_port   = 0
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Kraken-DCA-default-security-group"
  }
}