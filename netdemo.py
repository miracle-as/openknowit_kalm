import netifaces

interfaces = netifaces.interfaces()

for interface in interfaces:
    if interface == "lo":
        continue


    addrs = netifaces.ifaddresses(interface)
    
    if netifaces.AF_INET in addrs:
        ipv4_info = addrs[netifaces.AF_INET]
        for addr in ipv4_info:
            print(f"Interface: {interface}")
            print(f"  IPv4 Address: {addr['addr']}")
    


