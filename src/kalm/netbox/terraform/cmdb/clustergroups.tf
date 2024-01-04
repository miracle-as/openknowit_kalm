resource "netbox_cluster_group" "linuxclusters" {
  description = "Servers running native linuxclusters"
  name        = "linuxclusters"
}

resource "netbox_cluster_group" "vmwareclusters" {
  description = "Servers  running on vmware"
  name        = "vmwareclusters"
}

resource "netbox_cluster_group" "openstackclusters" {
  description = "Servers  running on openstack"
  name        = "openstackclusters"
}