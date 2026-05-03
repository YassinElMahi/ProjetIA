import socket 
import json
import copy
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


Name = "MrCalvitie"
team = None

def get_my_team(message):
    if message['players'][0] == Name:  
        return 'light'
    else:
        return 'dark'

def get_directions(team):
    if team == 'light':
        return [(1, 0), (1, -1), (1, 1)]
    else:
        return [(-1, 0), (-1, -1), (-1, 1)]

def find_piece(board, color, team):   
    for row in range(8):
        for col in range(8):
            piece = board[row][col][1]     # [1] = la pièce (ou null si case vide)
            if piece is not None and piece[0] == color and piece[1] == team:   
                return (row, col)
    return None

def get_valid_moves(board, row, col, team):
    moves = []
    for dr,dc in get_directions(team):
        r,c = row + dr, col + dc        
        while 0 <= r < 8 and 0 <= c < 8:
            if board[r][c][1] is not None :   # si une pièce occupe la case
                break
            moves.append((r,c))         # sinon c'est un coup valide
            r += dr                    # on continue dans la même direction
            c += dc
    return moves

def choix_de_move(board,color,team):
    pos = find_piece(board, color, team)
    if pos is None:
        return None               # pièce pas trouvée, abandon
    row,col = pos                 # décompresse la position (ex: row=0, col=3)
    moves = get_valid_moves(board,row,col,team)  # calcule les coups possibles
    if not moves:
        return None
    if team == 'light':
        best = max(moves, key=lambda m: m[0])   #moves c'est une liste de tuples comme [(2,3), (3,3), (4,3)]. On cherche le maximum par m[0]
    else:                                       #moves contient des tuples (rangée, colonne), lambda sert à dire à max sur quoi comparer
        best = min(moves, key=lambda m: m[0])   
    return[[row,col],[best[0],best[1]]]


def evaluate(board, my_team):
    score = 0
    enemy_team = 'dark' if my_team == 'light' else 'light'
    for row in range(8):
        for col in range(8):
            piece = board[row][col][1]
            if piece is None:
                continue
            if piece[1] == my_team:
                if my_team == 'light':
                    score += row * 10
                    if row == 7:
                        score += 1000
                else:
                    score += (7 - row) * 10
                    if row == 0:
                        score += 1000
            else:
                if enemy_team == 'light':
                    score -= row * 10
                    if row == 7:
                        score -= 1000
                else:
                    score -= (7 - row) * 10
                    if row == 0:
                        score -= 1000
    return score

def apply_move(board, src, dst):
    new_board = copy.deepcopy(board)
    piece = new_board[src[0]][src[1]][1]
    new_board[src[0]][src[1]][1] = None
    new_board[dst[0]][dst[1]][1] = piece
    return new_board

def get_all_moves(board, team):
    all_moves = []
    for row in range(8):
        for col in range(8):
            piece = board[row][col][1]
            if piece is not None and piece[1] == team:
                destinations = get_valid_moves(board, row, col, team)
                for dst in destinations:
                    all_moves.append(([row, col], [dst[0], dst[1]]))
    return all_moves

def minimax(board, depth, alpha, beta, is_maximizing, my_team):
    enemy_team = 'dark' if my_team == 'light' else 'light'
    score = evaluate(board, my_team)
    if depth == 0 or abs(score) >= 1000:
        return score
    if is_maximizing:
        best_score = float('-inf')   # on part du pire score possible
        for src, dst in get_all_moves(board, my_team):
            new_board = apply_move(board, src, dst)  # on simule le coup
            s = minimax(new_board, depth - 1, alpha, beta, False, my_team) #on rappelle minimax avec is_maximizing=False (tour adverse)
            best_score = max(best_score, s)
            alpha = max(alpha, s)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = float('inf')
        for src, dst in get_all_moves(board, enemy_team):
            new_board = apply_move(board, src, dst)
            s = minimax(new_board, depth - 1, alpha, beta, True, my_team)
            best_score = min(best_score, s)
            beta = min(beta, s)
            if beta <= alpha:
                break
        return best_score

def choix_de_move_minimax(board, color, my_team, depth=3):
    pos = find_piece(board, color, my_team)
    if pos is None:
        return None
    row, col = pos
    destinations = get_valid_moves(board, row, col, my_team)
    if not destinations:
        return None
    best_move = None
    best_score = float('-inf')
    for dst in destinations:
        new_board = apply_move(board, [row, col], [dst[0], dst[1]])
        score = minimax(new_board, depth - 1, float('-inf'), float('inf'), False, my_team)
        if score > best_score:
            best_score = score
            best_move = [[row, col], [dst[0], dst[1]]]
    return best_move



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
        board = message['board']
        color = message['color']

        if team is None:
            team = get_my_team(message)

        move = choix_de_move_minimax(board, color, team)

        send_message(conn, {
            'response': 'move',
            'move': move  
        })
