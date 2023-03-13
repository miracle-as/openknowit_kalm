from kalm import kalm
import os
import redis


def main():
    print(os.path.isdir("/etc/kalm"))

    r = redis.Redis()
    r.flushdb()
    ansibletoken = os.getenv("ANSIBLE_TOKEN")
    print("Running ansible automation daemonm")
    kalm.kalm(ansibletoken, r)



