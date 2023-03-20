#!/usr/bin/env python 
import pynetbox
nb = pynetbox.api(
    'https://netbox.openknowit.com',
    token='1b29e94362e31c84431524be05100a6c916641f6'
)


ipranges = nb.ipam.ip_ranges.all()
ipaddresses = nb.ipam.ip_addresses.all()
sites = nb.dcim.sites.all()
regions = nb.dcim.regions.all()
locations = nb.dcim.locations.all()
tenants = nb.tenancy.tenants.all()
tenantgroups = nb.tenancy.tenant_groups.all()
contacts = nb.dcim.contacts.all()
contactgroups = nb.dcim.contact_groups.all()
contactroles = nb.dcim.contact_roles.all()
sitegroups = nb.dcim.site_groups.all()
devices = nb.dcim.devices.all()
devicetypes = nb.dcim.device_types.all()
deviceroles = nb.dcim.device_roles.all()



#nb.dcim.devices.delete(devices)
#nb.dcim.sites.delete(sites)
#nb.dcim.site_groups.delete(sitegroups)
#nb.dcim.regions.delete(regions)
nb.ipam.ip_addresses.delete(ipaddresses)
nb.ipam.ip_ranges.delete(ipranges)
nb.tenancy.tenants.delete(tenants)
nb.tenancy.tenant_groups.delete(tenantgroups)



#nb.dcim.site_groups.create({"name": "demo", "slug": "demo", "groups": ""})
#nb.dcim.sites.create({"name": "demosite1", "slug": "demo1"})

#nb.dcim.devices.create({"name": "demo", "device_role": 2, "site": 4, "device_type": 1})
#nb.dcim.devices.create({"name": "demo", "device_role": 2, "site": 4, "device_type": 1})

