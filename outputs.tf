output "nodejs-ip" {
  value       = module.compute.nodejs-ip
  sensitive   = false
  description = "public ip of the nodejs"
}

output "react-ip" {
  value       = module.compute.react-ip
  sensitive   = false
  description = "public ip of the react"
}

output "postgress-ip" {
  value       = module.compute.postgress-ip
  sensitive   = false
  description = "public ip of the postgress"
}