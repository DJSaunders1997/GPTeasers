variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
  default     = "ContainerApps"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "UK West"
}

variable "container_app_name" {
  description = "Name of the container app"
  type        = string
  default     = "gpteasers"
}

variable "container_app_environment_name" {
  description = "Name of the container app environment"
  type        = string
  default     = "container-app-environment"
}

# Secret variables - values loaded from terraform.tfvars (not committed)
variable "openai_api_key" {
  description = "OpenAI API key"
  type        = string
  sensitive   = true
}

variable "gemini_api_key" {
  description = "Gemini API key"
  type        = string
  sensitive   = true
}

variable "azure_ai_api_key" {
  description = "Azure AI API key"
  type        = string
  sensitive   = true
}

variable "azure_ai_api_base" {
  description = "Azure AI API base URL"
  type        = string
  sensitive   = true
}

variable "deepseek_api_key" {
  description = "DeepSeek API key"
  type        = string
  sensitive   = true
}

variable "ghcr_token" {
  description = "GitHub Container Registry token"
  type        = string
  sensitive   = true
}