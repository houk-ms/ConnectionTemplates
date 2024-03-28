variable "resource_group_location" {
  default     = "eastus"
  description = "Location of the resource group."
}

variable "resource_prefix" {
  type        = string
  default     = "code2cloud"
  description = "Prefix of the resource names"
}

variable "env_var_prefix" {
  type        = string
  default     = "AZURE"
  description = "Prefix of the environment variables"
}