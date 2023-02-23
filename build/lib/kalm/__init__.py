from kalm import kalm
import os
import redis


def main():
    r = redis.Redis()
    r.flushdb()
    ansibletoken = os.getenv("ANSIBLE_TOKEN")
    print("Running ansible automation daemonm")
    kalm.kalm(ansibletoken, r)



