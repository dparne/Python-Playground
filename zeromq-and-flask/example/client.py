import sys
import zmq

context = zmq.Context()

subscriber = context.socket (zmq.SUB)
subscriber.connect ("tcp://10.0.3.124:5555")
subscriber.setsockopt (zmq.SUBSCRIBE,b"number")

while True:
    message = subscriber.recv()
    print(message)