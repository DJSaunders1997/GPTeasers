# GPTeasers Terraform Infrastructure

This directory contains the Infrastructure as Code (IaC) configuration for deploying the GPTeasers quiz application to Azure Container Apps.

## 📁 Directory Contents

- `main.tf` - Main infrastructure configuration (Resource Group, Container App Environment, Container App)
- `variables.tf` - Input variables for the infrastructure
- `outputs.tf` - Output values from the deployed infrastructure
- `providers.tf` - Terraform provider configurations
- `terraform.tfvars` - Actual values for sensitive variables (not committed to git)
- `terraform.tfvars.example` - Example file showing required variable structure
- `terraform.tfstate` - Current state of deployed infrastructure (not committed to git)
- `graph.dot` - Infrastructure dependency graph in DOT format
- `infrastructure.png` & `infrastructure.svg` - Visual representations of the infrastructure

## 🚀 Deploying the Infrastructure

### Prerequisites

1. **Azure CLI installed and authenticated**:
   ```bash
   az login
   ```

2. **Terraform installed** (v1.14.3+ recommended)

3. **Configure your secrets**:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your actual API keys and tokens
   ```

### Deployment Commands

1. **Initialize Terraform** (first time only):
   ```bash
   cd backend/terraform
   terraform init
   ```

2. **Review the planned changes**:
   ```bash
   cd backend/terraform
   terraform plan
   ```

3. **Deploy the infrastructure**:
   ```bash
   cd backend/terraform
   terraform apply
   ```

4. **Get the deployed app URL**:
   ```bash
   cd backend/terraform
   terraform output container_app_url
   ```

### Cleanup

To destroy all resources:
```bash
cd backend/terraform
terraform destroy
```

## ⚠️ Important Notes

### Hardcoded Container Image Concern

**I'm a bit confused and concerned that the container image is hardcoded in `main.tf`**:

```terraform
image  = "ghcr.io/djsaunders1997/gpteasers:7aa9ecacb7f655e25c149d704108690263ec26b4"
```

This means:
- The infrastructure is tied to a specific image version/tag
- Updates require manual Terraform changes
- CI/CD pipelines can't automatically update the infrastructure
- Risk of the image being deleted or becoming unavailable

**Future Enhancement Idea**: This would be a cool project to parameterize the image reference:
- Add an `image_tag` variable to `variables.tf`
- Make the image reference dynamic: `"ghcr.io/djsaunders1997/gpteasers:${var.image_tag}"`
- Allow CI/CD to pass the latest image tag during deployment
- Enable blue/green deployments with different image versions

For now, the infrastructure works as-is, but image updates require manual intervention. This could be a fun Terraform parameterization project for the future! 🎯

## 🔧 Configuration Details

### Resources Created

- **Resource Group**: `ContainerApps` (UK West region)
- **Container App Environment**: `container-app-environment`
- **Container App**: `gpteasers` with:
  - 0.25 CPU cores, 0.5Gi memory
  - External ingress on port 8000
  - GitHub Container Registry integration
  - Environment variables for all AI provider API keys

### Secrets Management

The following secrets are managed via Terraform:
- OpenAI API Key
- Azure AI API Key & Base URL
- Gemini API Key
- DeepSeek API Key
- GitHub Container Registry Token

**Security Note**: Secrets are defined in `terraform.tfvars` (gitignored) and managed through Terraform's lifecycle rules to prevent accidental overwrites during CI/CD deployments.

### Network Configuration

- **Ingress**: External enabled, auto transport
- **Traffic**: 100% to latest revision
- **Scaling**: 0-1 replicas (manual scaling)

## 📊 Infrastructure Visualization

View the infrastructure dependencies:
```bash
# Generate DOT graph
cd backend/terraform
terraform graph > graph.dot

# Convert to PNG (requires GraphViz)
dot -Tpng graph.dot -o infrastructure.png
```

## 🔍 Troubleshooting

- **State issues**: `terraform refresh` to sync with Azure
- **Import existing resources**: `terraform import <resource_type>.<name> <azure_resource_id>`
- **Debug mode**: `TF_LOG=DEBUG terraform apply`

## 📝 Development Workflow

1. Make changes to `.tf` files
2. Run `terraform plan` to preview
3. Run `terraform apply` to deploy
4. Use `terraform output` to get URLs/endpoints
5. Commit changes (excluding `.tfstate` and `.tfvars`)