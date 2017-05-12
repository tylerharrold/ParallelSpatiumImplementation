import time
import threading
#from threading import Thread

vals = [ 0 , 0 , 0 , 0 , 0]

def spatium(i):
    vals[i] = i + 1

def main():
    threads = []
    for i in range(5):
        threads.append(threading.Thread(target=spatium , args=(i,)))
        threads[i].start()
    for j in range(5):
        threads[j].join()
    total = 0
    for k in range(5):
        total = total + vals[k]
    print(vals)
    print(total)
    

main()
