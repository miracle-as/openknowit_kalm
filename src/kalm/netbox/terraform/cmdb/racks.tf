resource "netbox_rack" "demo_rack1" {
  count  =  6
  name         = "demo${format("%02d", count.index + 1)}_rack1"
  site_id  = netbox_site.demosite[count.index].id
  status   = "reserved"
  width    = 19
  u_height = 48
}
