// outputs already defined in main.tf but kept here for clarity
output "instance_id" {
  description = "ID of the created instance"
  value       = aws_instance.web.id
}
