import os

def check_netbox_environment_variables():
    if os.getenv("KALM_NETBOX_URL") is None:
        return False
    if os.getenv("KALM_NETBOX_TOKEN") is None:
        return False
    return True

def check_netbox_connectivity():
    if check_netbox_environment_variables() == False:
        return False
    return True

