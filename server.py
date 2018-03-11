import socket, select
from threading import Thread
import json


database = json.load(open('flags.json'))

class ClientThread(Thread):

    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print("[+] New thread started for "+ip+":"+str(port))
        run(self)

def run(self):
    while True:
        print("Listening...")
        data = conn.recv(2048)
        if not data: break

        try:
            jsondata = json.loads(data.decode('utf-8'))
            print("received data:", data.decode('utf-8'))
            user_key = jsondata['user_key']
            if 'points' in jsondata:
                for user in database['users']:
                    if user['user_key'] == user_key:
                        points = user['score']
                        conn.send(
                            bytes("<Server> " + str(points) + " points! \n", encoding='utf-8'))
                        break
            if 'points' not in jsondata:

                print(user_key)
                flag = jsondata['flag']
                print(flag)

                for challenge in database['challenges']:
                    if challenge['flag'] == flag:
                        challenge_title = challenge['name']
                        points = challenge['points']
                        print(challenge_title)

                for user in database['users']:
                    if user['user_key'] == user_key:
                        username = user['name']
                        print(username)
                        if challenge_title in user['completed']:
                            conn.send(bytes("<Server> " + "Already Completed! Thanks " + username + "\n",
                                            encoding='utf-8'))
                        else:
                            print('writing value to json file')
                            user['completed'].append(challenge_title)
                            user['score'] = user['score'] + points
                            with open('data.txt', 'w') as outfile:
                                json.dump(database, outfile)

                conn.send(bytes("<Server> " + str(points) + " points! Thanks " + username + "\n", encoding='utf-8'))
                break
        except Exception as e:
            print(e)
            conn.send(bytes("<Server> Got your data. But something went wrong..\n", encoding='utf-8'))
            break



BUFFER_SIZE = 1024  # Normally 1024
threads = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("0.0.0.0", 5000))
server_socket.listen(10)

read_sockets, write_sockets, error_sockets = select.select([server_socket], [], [])

while True:
    print("Waiting for incoming connections...")
    for sock in read_sockets:
        (conn, (ip,port)) = server_socket.accept()
        newthread = ClientThread(ip,port)