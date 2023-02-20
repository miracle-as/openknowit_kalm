from kalm import kalm
import os
import redis


def main():
    r = redis.Redis()
    r.flushdb()
    ansibletoken = os.getenv("ANSIBLE_TOKEN")
    print(ansibletoken)
    print("Running ansible automation daemonm")
    print(kalm.kalm(ansibletoken, r))



