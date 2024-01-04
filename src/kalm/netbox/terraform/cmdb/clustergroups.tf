resource "netbox_cluster_group" "linuxclusters" {
  description = "Servers running native linuxclusters"
  name        = "linuxclusters"
}

resource "netbox_cluster_group" "vmwareclusters" {
  description = "Servers  running on vmware"
  name        = "vmwareclusters"
}
