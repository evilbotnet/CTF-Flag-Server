import json
import socket
import optparse


parser = optparse.OptionParser('usage%prog'+'-user_key <key>'+'-flag <flag> ')


parser.add_option('-u', dest='userkey', help='The user key associated with your user')
parser.add_option('-f', dest='flag', help='The flag')
parser.add_option('--host', dest='host', help='Server IP')
parser.add_option('-p', dest='port', help='Server Port')
parser.add_option('--points', dest='points', action="store_true", default=False)

(options,args) = parser.parse_args()

points = options.points
userkey = options.userkey
flag = options.flag
host = options.host
port = options.port


if points == True:
    data = json.dumps({"points": "True", "user_key": userkey})

elif points == False:
    data = json.dumps({"flag": flag, "user_key": userkey})

#host = '192.168.1.151'
#port = 5000                   # The same port as used by the server

print("Sending " + data + " to " + host + ":" + str(port))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, int(port)))
s.sendall(bytes(data, encoding='utf-8'))
data = s.recv(1024)
s.close()
print(data.decode('utf-8'))