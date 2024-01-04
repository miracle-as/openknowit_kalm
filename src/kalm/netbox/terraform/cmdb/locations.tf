resource "netbox_location" "falkenstein" {
  count = 6
  name        = "falkenstein"
  description = "my description"
  site_id     = netbox_site.fsn1[count.index].id
  tenant_id   = netbox_tenant.knowit.id
}
