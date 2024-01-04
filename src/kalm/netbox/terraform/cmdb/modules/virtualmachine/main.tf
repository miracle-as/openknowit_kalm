resource "netbox_virtual_machine" "example" {
  cluster_id   = var.cluster_id
  name         = var.name
  tags         = var.tags
  disk_size_gb = var.disk_size_gb
  memory_mb    = var.memory_mb
  vcpus        = var.vcpus
  role_id      = var.role_id
  tenant_id    = var.tenant_id
  local_context_data = var.local_context_data
}

