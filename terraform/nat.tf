resource "aws_eip" "nat_eip" {
  vpc        = true
  depends_on = [aws_internet_gateway.ig]
  instance   = aws_instance.ec2_nat_instance.id
}
resource "aws_instance" "ec2_nat_instance" {
  ami           = "ami-0bbb886f29931c526"
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.public_subnet.id
}