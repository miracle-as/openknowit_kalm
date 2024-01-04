resource "netbox_cluster_type" "kvm" {
  name = "Native linux libvirt kvm"
}

resource "netbox_cluster_type" "vmware" {
  name = "Native vmware"
}
resource "netbox_cluster_type" "openstack" {
  name = "Native openstack"
}

