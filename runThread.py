import threading
import time


def a():
   # print("Function a is running at time : " + str(int(time.time()))) + " seconds."
   print("Function a is running at time ")


def b():
    #print("Function a is running at time : " + str(int(time.time()))) + " seconds."
    print("Function a is running at time : ")

threading.Thread(target=a).start()

threading.Thread(target=b).start()