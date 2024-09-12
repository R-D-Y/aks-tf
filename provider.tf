terraform {
  backend "azurerm" {
    resource_group_name   = "aks-prod-resource-group"   # Groupe de ressources Azure contenant le compte de stockage
    storage_account_name  = "tfstateaccount"            # Nom du compte de stockage Azure
    container_name        = "terraform-state"           # Nom du conteneur Blob où stocker l'état
    key                   = "terraform.tfstate"         # Nom du fichier tfstate dans le conteneur
  }
}

provider "azurerm" {
  features {}

  client_id       = var.client_id
  client_secret   = var.client_secret
  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
}

variable "client_id" {
  description = "Azure Client ID for authentication"
  type        = string
}

variable "client_secret" {
  description = "Azure Client Secret for authentication"
  type        = string
  sensitive   = true
}

variable "subscription_id" {
  description = "Azure Subscription ID"
  type        = string
}

variable "tenant_id" {
  description = "Azure Tenant ID"
  type        = string
}
