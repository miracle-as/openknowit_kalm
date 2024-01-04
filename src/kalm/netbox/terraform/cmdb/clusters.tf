variable "openstackcluster_names" {
  description = "Create clusters with theese names"
  type        = list(string)
  default     = ["openstack01.openknowit.com", "openstack02.openknowit.com", "openstack03.openknowit.com"]
}

resource "netbox_cluster" "openstack" {
  count = 3
  cluster_type_id  = netbox_cluster_type.kvm.id
  name             = var.openstackcluster_names[count.index]
  cluster_group_id = netbox_cluster_group.openstackclusters.id
}

variable "vmwarecluster_names" {
  description = "Create clusters with theese names"
  type        = list(string)
  default     = ["vmware01.openknowit.com", "vmware02.openknowit.com", "vmware03.openknowit.com"]
}

resource "netbox_cluster" "linuxclusters" {
  count = 3
  cluster_type_id  = netbox_cluster_type.vmware.id
  name             = var.vmwarecluster_names[count.index]
  cluster_group_id = netbox_cluster_group.linuxclusters.id
}