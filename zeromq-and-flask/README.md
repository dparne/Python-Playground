## zeromq and flask

I was working on this experimental project where I needed to find out and do something whenever a HTTP request is being made to an application running in Python using flask.

I have decided that using a Publisher-Subscriber pattern would be better since whenever a request is made I can publish a message and then in turn use a client which subscribes to the publisher and use the message published to do any custom implementation based on the message.

I have explored a couple of other things that I could use but they did not work out for various reasons or simply me being lazy enough to explore them in detail.

[PubNub](https://www.pubnub.com/) - Required subscription

[PyPubSub](http://pubsub.sourceforge.net/) - Promising! but not enough documentation for my laziness I guess

[Flask-SocketIO](https://flask-socketio.readthedocs.org/en/latest/) - Good documentation but could not find implementations of python clients that I can refer to. Being a python newbie I guess it scared me away.

Based on your requirements please explore these and more before deciding on an approach.

I myself tried [ZeroMQ](http://zeromq.org/) first and could not make it work and tried all of the above before coming back to it again and making it work.

So coming to the implementation. I was working on two unix flavored machines with both already having python installed. we need to install "pyzmq" and "flask" packages for python. You could do this using the regular "pip install" command. You might have to install "autoconf", "g++", "python-dev" before you could install "pyzmq". You can use either "apt-get" or "yum" package managers to install these three based on the type of linux you are using.

This is the code in my server.py file. Let's say this script is running on a machine with ip address "192.168.10.10". I wanna publish the message over tcp on port 5555.

```
## server.py

import time
import zmq
from flask import Flask

app = Flask(__name__)
ctx = zmq.Context()
pub = ctx.socket(zmq.PUB)

def publish_message(message):
    url = "tcp://192.168.10.10:5555"
    try:
        pub.bind(url)
        time.sleep(1)
        print("sending message : {0}".format(message, pub))
        pub.send(message)
    except Exception as e:
        print("error {0}".format(e))
    finally:
        '''You wanna unbind the publisher to keep receiving the published messages Otherwise you would get a -- Adress already in use -- error'''
        pub.unbind(url)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/print/<int:number>/", methods = ['GET'])
def printNumber(number):
    ''' This is an endpoint which prints the number we want to print in response and also publishes a message containing the number '''
    response = 'Number %d' % number
    publish_message('number%d' % number)
    return response

''' In python __name__ will be "__main__" whenever the script file itself is called instead of being used as a library '''
if __name__ == '__main__':
    ''' The default port it will run on here is 5000 '''
    app.run(host='0.0.0.0', debug=True)

```

- Run this script by running the command "pyhton server.py". 
- Now you can make requests to http://192.168.10.10:5000/print/1 which will respond with message "Number 1". But it also publishes a message "number1" to the subscribers.

Now let's look at the implementation of client.

In this client I am gonna just keep listening to the server and print whatever I get.

```
## client.py

import zmq

context = zmq.Context()

subscriber = context.socket (zmq.SUB)
subscriber.connect ("tcp://192.168.10.10:5555")
subscriber.setsockopt (zmq.SUBSCRIBE,b"number")

while True:
    message = subscriber.recv()
    print(message)
```

I can run the client on any machine and be able to receive the messages as long as I am on the same network as the server.

After making a series of HTTP requests like this

- http://192.168.10.10:5000/print/1

- http://192.168.10.10:5000/print/2

- http://192.168.10.10:5000/print/3

My client received the following messages

```
number1
number2
number3
```