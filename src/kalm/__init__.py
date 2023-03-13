from kalm import kalm
import os
import redis

def setupkalm():
    setup = False
    print("We need to setup kalm - Do you with to continue (y/N)? ")
    answer = input()
    if answer.upper == "Y":
        os.makedirs("/etc/kalm")
    return setup

def etcready():
    if os.path.isdir("/etc/kalm"):
        print("Ready to proceed, /etc/kalm is a directory")
        return True
    else:
        print("We need to setup kalm")
        return setupkalm()

def main():
    ready = False
    setup = False
    ready  = etcready()

    if ready:
        r = redis.Redis()
        r.flushdb()
        ansibletoken = os.getenv("ANSIBLE_TOKEN")
        print("Running ansible automation daemonm")
        kalm.kalm(ansibletoken, r)



