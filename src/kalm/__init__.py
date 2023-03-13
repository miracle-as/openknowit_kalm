from kalm import kalm
import os
import redis


def main():
    ready = False
    if os.path.isdir("/etc/kalm"):
        print("Ready to proceed, /etc/kalm is a directory")
    else:
        print("We need to setup kalm")
        exit

    if ready:
        r = redis.Redis()
        r.flushdb()
        ansibletoken = os.getenv("ANSIBLE_TOKEN")
        print("Running ansible automation daemonm")
        kalm.kalm(ansibletoken, r)



