# Resource Group
resource "azurerm_resource_group" "gpteasers" {
  name     = var.resource_group_name
  location = var.location
}

# Container App Environment
resource "azurerm_container_app_environment" "gpteasers" {
  name                       = var.container_app_environment_name
  location                   = azurerm_resource_group.gpteasers.location
  resource_group_name        = azurerm_resource_group.gpteasers.name
  # Remove log_analytics_workspace_id - the existing environment doesn't have one
}

# Container App
resource "azurerm_container_app" "gpteasers" {
  name                         = var.container_app_name
  container_app_environment_id = azurerm_container_app_environment.gpteasers.id
  resource_group_name          = azurerm_resource_group.gpteasers.name
  revision_mode                = "Single"

  template {
    container {
      name   = "gpteasers"
      image  = "ghcr.io/djsaunders1997/gpteasers:7aa9ecacb7f655e25c149d704108690263ec26b4"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name        = "OPENAI_API_KEY"
        secret_name = "openai-api-key-secret"
      }
      env {
        name        = "AZURE_AI_API_KEY"
        secret_name = "azure-ai-api-key-secret"
      }
      env {
        name        = "GEMINI_API_KEY"
        secret_name = "gemini-api-key-secret"
      }
      env {
        name        = "DEEPSEEK_API_KEY"
        secret_name = "deepseek-api-key-secret"
      }
      env {
        name        = "AZURE_AI_API_BASE"
        secret_name = "azure-ai-api-base-secret"
      }
    }

    min_replicas = 0
    max_replicas = 1
  }

  ingress {
    external_enabled = true
    target_port      = 8000
    transport        = "auto"  # Changed from "Auto" to "auto" to match existing
    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  registry {
    server               = "ghcr.io"
    username             = "DJSaunders1997"
    password_secret_name = "ghcrio-djsaunders1997"
  }

  # Secrets are managed externally - these placeholders prevent Terraform from removing them
  secret {
    name  = "openai-api-key-secret"
    value = var.openai_api_key
  }

  secret {
    name  = "azure-ai-api-key-secret"
    value = var.azure_ai_api_key
  }

  secret {
    name  = "gemini-api-key-secret"
    value = var.gemini_api_key
  }

  secret {
    name  = "deepseek-api-key-secret"
    value = var.deepseek_api_key
  }

  secret {
    name  = "azure-ai-api-base-secret"
    value = var.azure_ai_api_base
  }

  secret {
    name  = "ghcrio-djsaunders1997"
    value = var.ghcr_token
  }

  lifecycle {
    ignore_changes = [
      secret,  # Don't update secrets - they're managed by CI/CD or manually
      template[0].container[0].image,  # Allow image updates from CI/CD
    ]
  }
}