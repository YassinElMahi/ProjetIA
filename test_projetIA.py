from projetIA import get_directions, find_piece, get_valid_moves, evaluate, apply_move, get_all_moves

def make_empty_board():
    board = []
    for row in range(8):
        board.append([["color", None] for col in range(8)])
    return board

def test_get_directions_light():
    assert get_directions("light") == [(1, 0), (1, -1), (1, 1)]
    print("test_get_directions_light: OK")

def test_find_piece():
    board = make_empty_board()
    board[0][0][1] = ["orange", "light"]
    assert find_piece(board, "orange", "light") == (0, 0)
    print("test_find_piece: OK")

def test_get_valid_moves():
    board = make_empty_board()
    board[0][3][1] = ["pink", "light"]
    moves = get_valid_moves(board, 0, 3, "light")
    assert (1, 3) in moves
    print("test_get_valid_moves: OK")

def test_apply_move():
    board = make_empty_board()
    board[0][3][1] = ["pink", "light"]
    new_board = apply_move(board, [0, 3], [3, 3])
    assert new_board[3][3][1] == ["pink", "light"]
    assert new_board[0][3][1] is None
    print("test_apply_move: OK")

def test_evaluate_victoire():
    board = make_empty_board()
    board[7][3][1] = ["pink", "light"]
    assert evaluate(board, "light") >= 10000
    print("test_evaluate_victoire: OK")

def test_get_all_moves():
    board = make_empty_board()
    board[0][0][1] = ["orange", "light"]
    moves = get_all_moves(board, "light")
    assert len(moves) > 0
    print("test_get_all_moves: OK")

if __name__ == "__main__":
    test_get_directions_light()
    test_find_piece()
    test_get_valid_moves()
    test_apply_move()
    test_evaluate_victoire()
    test_get_all_moves()
    print("\n Tous les tests passent !")
