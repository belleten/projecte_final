import zmq
import random
import time


def sensor():

    reads=["20","22","25","30","10"]
    new_read=random.choice(reads)
    return new_read

if __name__=="__main__":

    context = zmq.Context()

    sock = context.socket(zmq.REQ)
    sock.connect("tcp://127.0.0.1:5678")

    while True:
        sock.send(sensor())
        time.sleep(1)
        print sock.recv()
