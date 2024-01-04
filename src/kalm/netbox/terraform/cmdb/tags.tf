
resource "netbox_tag" "role_wireguard"             { 
name      = "role_wireguard"            
color_hex =  var.color_map["Blue"] 
}
resource "netbox_tag" "role_backup"             { 
name      = "role_backup"            
color_hex =  var.color_map["Cyan"] 
}
resource "netbox_tag" "role_kalm"             { 
name      = "role_kalm"            
color_hex =  var.color_map["Cyan"] 
}
resource "netbox_tag" "role_zabbix"             { 
name      = "role_zabbix"            
color_hex =  var.color_map["Cyan"] 
}
resource "netbox_tag" "service_nfsserver"             { 
name      = "service_nfsserver"            
color_hex =  var.color_map["Blue"] 
}
resource "netbox_tag" "service_openshiftmaster"             { 
name      = "service_openshiftmaster"            
color_hex =  var.color_map["Blue"] 
}
resource "netbox_tag" "service_openshiftworker"             { 
name      = "service_openshiftworker"            
color_hex =  var.color_map["Blue"] 
}
resource "netbox_tag" "service_openstackundercloud"             { 
name      = "service_openstackundercloud"            
color_hex =  var.color_map["Blue"] 
}
resource "netbox_tag" "service_openstackovercloud"             { 
name      = "service_openstackovercloud"            
color_hex =  var.color_map["Blue"] 
}
resource "netbox_tag" "service_satellite"             { 
name      = "service_satellite"            
color_hex =  var.color_map["Blue"] 
}
resource "netbox_tag" "sla_test"             { 
name      = "sla_test"            
color_hex =  var.color_map["Purple"] 
}
resource "netbox_tag" "sla_prerproduction"             { 
name      = "sla_prerproduction"            
color_hex =  var.color_map["Yellow"] 
}
resource "netbox_tag" "sla_production"             { 
name      = "sla_production"            
color_hex =  var.color_map["Red"] 
}
resource "netbox_tag" "sla_qa"             { 
name      = "sla_qa"            
color_hex =  var.color_map["Blue"] 
}
resource "netbox_tag" "os_ubuntu"             { 
name      = "os_ubuntu"            
color_hex =  var.color_map["Orange"] 
}
resource "netbox_tag" "os_win2022"             { 
name      = "os_win2022"            
color_hex =  var.color_map["Blue"] 
}
resource "netbox_tag" "os_redhat"             { 
name      = "os_redhat"            
color_hex =  var.color_map["OrangeRed"] 
}
resource "netbox_tag" "os_debian"             { 
name      = "os_debian"            
color_hex =  var.color_map["PowderBlue"] 
}
resource "netbox_tag" "os_linux"             { 
name      = "os_linux"            
color_hex =  var.color_map["LightSkyBlue"] 
}
resource "netbox_tag" "os_windows"             { 
name      = "os_windows"            
color_hex =  var.color_map["LightGreen"] 
}
resource "netbox_tag" "openshiftmaster"      { 
name      = "openshiftmaster"
color_hex =  var.color_map["LightGreen"] 
}
resource "netbox_tag" "workstation"      { 
name      = "workstation"
color_hex =  var.color_map["Green"] 
}
