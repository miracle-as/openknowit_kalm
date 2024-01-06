resource "netbox_virtual_machine" "gusti" {
  cluster_id   = netbox_cluster.openstack[0].id
  name         = "gusti01"
  tags         = [ "os_win2022", "role_backup" ]
  disk_size_gb = 500
  memory_mb    = 16192
  vcpus        = "8"
  role_id      = netbox_device_role.server.id
  tenant_id    = netbox_tenant.knowit.id
  local_context_data = jsonencode(
        {
        "os": {
                "operating_system": "win2022",
        },
        "wireguard": {
                "network": "wgdemo",
                "public_key": "",
                "role": "client"
                }
        }
  )
}
