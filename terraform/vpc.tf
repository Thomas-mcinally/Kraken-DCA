resource "aws_vpc" "vpc" {
  cidr_block = "10.100.0.0/16"
  tags = {
    Name = "Kraken DCA VPC"
  }
}

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

/* Elastic IP for NAT */
resource "aws_eip" "nat_eip" {
  vpc        = true
  depends_on = [aws_internet_gateway.ig]
}
/* NAT gateway*/
resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.public_subnet.id
  depends_on    = [aws_internet_gateway.ig]
  tags = {
    Name = "Kraken DCA NAT"
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
resource "aws_route" "private_nat_gateway" {
  route_table_id         = aws_route_table.private_subnet_route_table.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.nat.id
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