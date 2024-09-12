output "kube_config" {
  description = "Raw Kubernetes config to interact with the AKS cluster"
  value       = azurerm_kubernetes_cluster.aks.kube_config_raw
  sensitive   = true
}

output "aks_fqdn" {
  description = "Fully Qualified Domain Name of the AKS cluster"
  value       = azurerm_kubernetes_cluster.aks.fqdn
}

output "resource_group_name" {
  description = "The name of the resource group in which the AKS cluster is created"
  value       = azurerm_resource_group.aks_rg.name
}

output "node_count" {
  description = "Number of nodes in the default node pool"
  value       = azurerm_kubernetes_cluster.aks.agent_pool_profile[0].count
}

output "node_vm_size" {
  description = "VM size of the default node pool"
  value       = azurerm_kubernetes_cluster.aks.agent_pool_profile[0].vm_size
}
