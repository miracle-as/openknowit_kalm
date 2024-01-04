resource "netbox_cluster" "openstack" {
  cluster_type_id  = netbox_cluster_type.openstack.id
  name             = "openstackcluster01"
  cluster_group_id = netbox_cluster_group.openstackclusters.id
}

resource "netbox_cluster" "vmwareclusters" {
  cluster_type_id  = netbox_cluster_type.vmware.id
  name             = "vmwarecluster01"
  cluster_group_id = netbox_cluster_group.vmwarelusters.id
}

resource "netbox_cluster" "linuxclusters" {
  cluster_type_id  = netbox_cluster_type.vmware.id
  name             = "linuxcluster01"
  cluster_group_id = netbox_cluster_group.linuxclusters.id
}