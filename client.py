import json
import socket
import optparse


parser = optparse.OptionParser('usage %prog -u <key> -f <flag>  --host <serverIP> -p <port>')


parser.add_option('-u', dest='userkey', help='The user key associated with your user. No username required.')
parser.add_option('-f', dest='flag', help='The flag. May require "" if on UNIX.')
parser.add_option('--host', dest='host', help='Server hostname or IP address where flag server is running.')
parser.add_option('-p', dest='port', help='Specifies port that server is listening on.')
parser.add_option('--points', dest='points', help='Optional parameter. Retrieves points for specified user. Flag (-f) is ignored.', action="store_true", default=False)

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
