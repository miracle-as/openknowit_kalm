from kalm import kalm
import os
import sys
import redis
import subprocess

def runme(command):
  subprocess.Popen(command , shell=True,stdout=subprocess.PIPE)

def setupkalm():
    setup = False
    print("We need to setup kalm - Do you with to continue (y/N)? ")
    answer = input()
    if answer == "Y" or answer == "y" or answer == "Yes" or answer == "yes":
        print("Initializing")
        runme("sudo mkdir /etc/kalm")

        setup  = True
    return setup

def etcready():
    if os.path.isdir("/etc/kalm"):
        print("Ready to proceed, /etc/kalm is a directory")
        return True
    else:
        print("We need to setup kalm")
        return setupkalm()

def main():
    print( "This is the name of the script: ", sys.argv[0])
    print( "Number of arguments: ", len(sys.argv))
    print( "The arguments are: " , str(sys.argv))
    ready = False
    setup = False
    ready  = etcready()

    if ready:

        r = redis.Redis()
        r.flushdb()
        ansibletoken = os.getenv("ANSIBLE_TOKEN")
        loop = False
        first = True
        if str(sys.argv[1]) == '-d': 
            loop = True 
        print("loop %s " % str(loop))
        while first == True or loop == True:
            print("Running ansible automation daemon")
            kalm.kalm(ansibletoken, r)
            first = False
            if loop:
               runme("sleep 30")




