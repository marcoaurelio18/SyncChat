import socket
import threading
import sys

IP = socket.gethostbyname(socket.gethostname())
PORT = 20000
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "/bye"
LIST_MSG = "/list"
SEND_FILE_MSG = '/file'
GET_FILE_MSG = '/get'

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def sendNameToServer():
    udp.connect(ADDR)
    nomeDeUsuario = input("Nome de usuario: ")
    msg = ("USER:" + nomeDeUsuario)
    udp.send(msg.encode(FORMAT))

def sendMessage():
    connect = True
    while connect:
        msg = input()
        if msg == DISCONNECT_MSG:
            udp.connect(ADDR)
            udp.send(msg.encode(FORMAT))
            udp.close()            
            connect = False
        
        elif ((SEND_FILE_MSG or GET_FILE_MSG) in msg):
            tcp.connect(ADDR)
            tcp.send(msg)

        else:
            udp.connect(ADDR)
            udp.send(msg.encode(FORMAT))

def receiveMessage():
    connect = True
    while connect:
        msg = udp.recv(SIZE).decode(FORMAT)
        print(msg)

sendNameToServer()

(threading.Thread(target=sendMessage)).start()
(threading.Thread(target=receiveMessage)).start()