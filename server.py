import socket
import threading
import re

IP = socket.gethostbyname(socket.gethostname())
TCP = 20000
ADDR = (IP, TCP)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "/bye"
LIST_USERS_CONNECTED_MSG = "/list"
SEND_FILE_MSG = '/file'
GET_FILE_MSG = '/get'



usernameByAddress = dict()
activeUsers = []
udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


def handle_client():
    udp.bind(ADDR)

    # tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # tcp.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    # tcp.bind(ADDR)
    # tcp.listen(1)
    connected = True
    while connected:
        msg, client  = udp.recvfrom(SIZE)
        msg = msg.decode(FORMAT)

        if msg == DISCONNECT_MSG:
            disconectUser(client)

        elif 'USER:' in msg:
            getClientName(msg, client)
        
        elif msg == LIST_USERS_CONNECTED_MSG:
            listActiveUsers(client)
        
        elif SEND_FILE_MSG in msg:
            sendFileMessage(msg, client)
        
        else:
            sendTextMessage(msg, client)


    # getNameByClientAddress(ADDR, udp.recv(SIZE).decode(FORMAT))
    # activeUsers.append(udp)


def getClientName(msg, client):
    regexp = re.compile('USER:(.*)$')
    name = regexp.search(msg).group(1)
    activeUsers.append(name)
    usernameByAddress[client] = name
    msg = name + ' entrou'
    print('INFO:' + name + ' entrou')
    sendMensageToAll(msg, client)

def disconectUser(client):
    msg = usernameByAddress[client] + ' saiu'
    print('INFO:' + usernameByAddress[client] + ' saiu')
    sendMensageToAll(msg, client)
    activeUsers.remove(usernameByAddress[client])
    del usernameByAddress[client]

def listActiveUsers(client):
    msg = 'Clientes conectados:\n'
    for user in activeUsers:
        msg += user
        msg += ', '
    msg = msg[:-2]
    sendMessageToClient(msg, client)

def sendTextMessage(msg, client):
    print('MSG:' + usernameByAddress[client] + ':' + msg)
    clientMsg = 'MSG:' + msg
    msg = usernameByAddress[client] + ' disse: ' + msg
    sendMessageToClient(clientMsg, client)
    sendMensageToAll(msg, client)

def sendFileMessage(msg, client):
    pass

def sendMessageToClient(msg, client):
    msg = msg.encode(FORMAT)
    udp.sendto(msg, client)
    return

def sendMensageToAll(msg, client):
    for user in usernameByAddress:
        if user != client:
            sendMessageToClient(msg, user)

def main():
    print(f"[NEW CONNECTION] {ADDR} connected")
    thread = threading.Thread(target=handle_client)
    thread.start()

main()
