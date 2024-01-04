resource "netbox_device" "demoserver" {
  name           = "flemming"
  device_type_id = netbox_device_type.nuc.id
  role_id        = netbox_device_role.workstation.id
  site_id        = netbox_site.demosite.id
}


