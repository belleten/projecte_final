import zmq
import random
import time
import ORM

class service():

    def

if __name__=="__main__":

    context = zmq.Context()

    sock = context.socket(zmq.REP)
    sock.bind("tcp://127.0.0.1:5678")

    while True:
        message = sock.recv()
        sock.send("correct")
        print message
