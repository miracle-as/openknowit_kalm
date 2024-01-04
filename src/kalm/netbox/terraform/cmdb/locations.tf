resource "netbox_location" "demolocation" {
  name        = "demolocation"
  description = "my demolocation"
  site_id     = netbox_site.demosite.id
  tenant_id   = netbox_tenant.knowit.id
}
