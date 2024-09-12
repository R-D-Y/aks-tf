variable "resource_group_name" {
  description = "The name of the resource group in which the AKS cluster will be created"
  type        = string
  default     = "aks-resource-group"
}

variable "location" {
  description = "The Azure location where the resources will be created"
  type        = string
  default     = "East US"
}

variable "cluster_name" {
  description = "The name of the Kubernetes cluster"
  type        = string
  default     = "myAKSCluster"
}

variable "dns_prefix" {
  description = "DNS prefix for the AKS cluster"
  type        = string
  default     = "aks"
}

variable "node_count" {
  description = "The number of nodes in the default node pool"
  type        = number
  default     = 2
}

variable "vm_size" {
  description = "The size of the virtual machine for the default node pool"
  type        = string
  default     = "Standard_DS2_v2"
}

variable "additional_node_pools_count" {
  description = "Number of additional node pools"
  type        = number
  default     = 1
}

variable "additional_vm_size" {
  description = "The size of the virtual machines in the additional node pools"
  type        = string
  default     = "Standard_DS2_v2"
}

variable "additional_node_count" {
  description = "The number of nodes in the additional node pools"
  type        = number
  default     = 1
}

variable "environment" {
  description = "The environment to which the AKS cluster belongs"
  type        = string
  default     = "dev"
}
