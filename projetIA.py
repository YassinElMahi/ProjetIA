import socket 
import json
import struct


def send_message(sock, message):
    data = json.dumps(message).encode('utf-8') # transforme en bytes
    size = struct.pack('I', len(data))        # taille en binaire
    sock.send(size + data)                     # envoie taille + message
    print("sent")

def receive_message(sock):
    raw_size = b''                   # on commence avec rien (b'' = bytes vide)
    while len(raw_size) < 4:         # Lire exactement 4 bytes
        raw_size += sock.recv(4 - len(raw_size))
    size = struct.unpack('I', raw_size)[0]  # convertit en nombre
    data = b'' 
    while len(data) < size:
        data += sock.recv(size - len(data))        # lit exactement 'size' bytes
    return json.loads(data.decode('utf-8'))  # transforme en dictionnaire python

Ping_port = 3000

ping_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ping_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ping_sock.bind(('0.0.0.0', 3000))
ping_sock.listen(1)


client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('172.17.10.46', 3000))

message = {
  "request": "subscribe",
  "port": 3000,
  "name": "MrCalvitie",
  "matricules": ["24115"]
}

send_message(client, message)
response = receive_message(client)
print(response)



while True:
    print("Serveur connécté")
    ping_sock.settimeout(10)
    while 1:
        try:
            conn, addr = ping_sock.accept()
            break
        except socket.timeout:
            print("waiting for request")
    message = receive_message(conn)
    print(message)

    if message['request'] == 'ping':
        send_message(conn, {'response': 'pong'})

    if message['request'] == 'play':
        send_message(conn, {
            'response': 'move',
            'move': 0  
        })
