import time
import zmq
from flask import Flask

app = Flask(__name__)
ctx = zmq.Context()
pub = ctx.socket(zmq.PUB)

def publish_message(message):
    url = "tcp://10.0.3.124:5555"
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