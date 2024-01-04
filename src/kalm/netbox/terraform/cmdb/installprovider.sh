export NETBOX_PROVIDER_VERSION=3.5.3
mkdir -p ~/.terraform.d/plugins/registry.terraform.io/e-breuninger/netbox/${NETBOX_PROVIDER_VERSION}/linux_amd64
wget -O /tmp/e-breuninger_netbox_${NETBOS_PROVIDER_VERSION}  https://artifacts.openknowit.com/openknowit/netbox/${NETBOX_PROVIDER_VERSION}/terraform-provider-netbox

cp  /tmp/e-breuninger_netbox_${NETBOS_PROVIDER_VERSION} ~/.terraform.d/plugins/registry.terraform.io/e-breuninger/netbox/${NETBOX_PROVIDER_VERSION}/linux_amd64/terraform-provider-netbox_v${NETBOX_PROVIDER_VERSION}

rm /tmp/e-breuninger_netbox_${NETBOS_PROVIDER_VERSION}
