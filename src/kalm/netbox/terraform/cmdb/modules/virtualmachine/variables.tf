variable "cluster_id" {
  description = "Cluster ID"
}

variable "name" {
  description = "Name of the virtual machine"
}

variable "tags" {
  description = "List of tags for the virtual machine"
  type        = list(string)
  default     = ["RedHat", "undercloud", "Backup"]
}

variable "disk_size_gb" {
  description = "Disk size in gigabytes"
  default     = 40
}

variable "memory_mb" {
  description = "Memory size in megabytes"
  default     = 8192
}

variable "vcpus" {
  description = "Number of virtual CPUs"
  default     = 2
}

variable "role_id" {
  description = "Role ID"
}

variable "tenant_id" {
  description = "Tenant ID"
}

variable "local_context_data" {
  description = "Local context data as JSON"
}
