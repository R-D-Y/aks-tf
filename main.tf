provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "aks_rg" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_kubernetes_cluster" "aks" {
  name                = var.cluster_name
  location            = azurerm_resource_group.aks_rg.location
  resource_group_name = azurerm_resource_group.aks_rg.name
  dns_prefix          = var.dns_prefix

  default_node_pool {
    name       = "default"
    node_count = var.node_count
    vm_size    = var.vm_size
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin = "azure"
    load_balancer_sku = "standard"
  }

  tags = {
    environment = var.environment
  }
}

resource "azurerm_kubernetes_cluster_node_pool" "additional_nodes" {
  count               = var.additional_node_pools_count
  kubernetes_cluster_id = azurerm_kubernetes_cluster.aks.id
  name                = format("nodepool%d", count.index + 1)
  vm_size             = var.additional_vm_size
  node_count          = var.additional_node_count
}

output "kube_config" {
  value = azurerm_kubernetes_cluster.aks.kube_config_raw
  sensitive = true
}

output "aks_fqdn" {
  value = azurerm_kubernetes_cluster.aks.fqdn
}

output "resource_group_name" {
  value = azurerm_resource_group.aks_rg.name
}
