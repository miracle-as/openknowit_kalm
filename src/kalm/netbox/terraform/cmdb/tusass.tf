resource "netbox_virtual_machine" "tusassrancher" {
  count = 3
  cluster_id   = netbox_cluster.openstack[1].id
  name         = "tusassrancher${format("%02d", count.index + 1)}"
  tags         = [ "os_redhat",  "role_backup" ]
  disk_size_gb = 10
  memory_mb    = 3500
  vcpus        = "1"
  role_id      = netbox_device_role.server.id
  tenant_id    = netbox_tenant.knowit.id
  local_context_data = jsonencode(
        {
        "os": {
                "activation_key": "Faceted-Oil-Scion6",
                "operating_system": "rhel-9.2",
                "rhel_org": "6207854A"
        },
        "wireguard": {
                "network": "wgdemo",
                "public_key": "",
                "role": "client"
                }
        }
  )
}

resource "netbox_virtual_machine" "tusassrancherctl" {
  count = 1
  cluster_id   = netbox_cluster.openstack[1].id
  name         = "tusassrancherctl${format("%02d", count.index + 1)}"
  tags         = [ "os_redhat",  "role_backup" ]
  disk_size_gb = 10
  memory_mb    = 3500
  vcpus        = "1"
  role_id      = netbox_device_role.server.id
  tenant_id    = netbox_tenant.knowit.id
  local_context_data = jsonencode(
        {
        "os": {
                "activation_key": "Faceted-Oil-Scion6",
                "operating_system": "rhel-9.2",
                "rhel_org": "6207854A"
        },
        "wireguard": {
                "network": "wgdemo",
                "public_key": "",
                "role": "client"
                }
        }
  )
}

