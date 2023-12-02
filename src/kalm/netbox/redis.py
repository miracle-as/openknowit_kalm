import redis

def refresh_netbox_from_redis(myenv):
    r = redis.Redis(host='localhost', port=6379, db=0)
    data = {}
    details = {}
    mykey = "netbox"
    knownservers = r.keys("kalm:vmware:*:known")
    detailedservers = r.keys("kalm:vmware:*:details")
    for server in knownservers:
        key = server.decode("utf-8")
        value = r.get(key)
        data[key] = value.decode("utf-8")
    for server in detailedservers:
        key = server.decode("utf-8")
        value = r.get(key)
        details[key] = value.decode("utf-8")
    print(data)
    return data
