resource "netbox_device_type" "nuc" {
  model           = "nuc"
  part_number     = "123"
  manufacturer_id = netbox_manufacturer.Intel.id
}

resource "netbox_device_type" "P1" {
  model           = "P1"
  part_number     = "123"
  manufacturer_id = netbox_manufacturer.Lenovo.id
}
