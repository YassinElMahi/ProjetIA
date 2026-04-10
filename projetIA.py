import socket 
import json
import struct

def send_message(sock, message):
    data = json.dumps(message).encode('utf-8') # transforme en bytes
    size = struct.pack('!I', len(data))        # taille en binaire
    sock.send(size + data)                     # envoie taille + message

def receive_message(sock):
    raw_size = b''                   # on commence avec rien (b'' = bytes vide)
    while len(raw_size) < 4:         # Lire exactement 4 bytes
        raw_size += sock.recv(4 - len(raw_size))
    size = struct.unpack('!I', raw_size)[0]  # convertit en nombre
    data = b'' 
    while len(data) < size:
        data += sock.recv(size - len(data))        # lit exactement 'size' bytes
    return json.loads(data.decode('utf-8'))  # transforme en dictionnaire python

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(('192.168.0.103', 3000))

message = {
  "request": "subscribe",
  "port": 3000,
  "name": "MrCalvitie",
  "matricules": ["24115"]
}

send_message(client, message)
response = receive_message(client)
print(response)