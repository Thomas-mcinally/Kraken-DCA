resource "aws_vpc" "vpc" {
  cidr_block = "10.100.0.0/16"
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

resource "aws_internet_gateway" "ig" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name = "Kraken DCA internet gateway"
  }
}