import copy


class GameState:
    def __init__(self):
        # Board represented as 8x8 2D list, uppercase = white, lowercase = black
        self.board = [
            list("rnbqkbnr"),
            list("pppppppp"),
            list("........"),
            list("........"),
            list("........"),
            list("........"),
            list("PPPPPPPP"),
            list("RNBQKBNR"),
        ]
        self.white_to_move = True

    def make_move(self, move):
        (sr, sc), (er, ec) = move
        piece = self.board[sr][sc]
        # move the piece
        self.board[sr][sc] = '.'
        # handle pawn promotion
        if piece == 'P' and er == 0:
            piece = 'Q'
        elif piece == 'p' and er == 7:
            piece = 'q'
        self.board[er][ec] = piece
        self.white_to_move = not self.white_to_move

    def get_all_moves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece == '.':
                    continue
                if (piece.isupper() and self.white_to_move) or (piece.islower() and not self.white_to_move):
                    moves.extend(self.get_piece_moves(r, c, piece))
        return moves

    def get_piece_moves(self, r, c, piece):
        moves = []
        if piece.upper() == 'P':
            moves.extend(self._pawn_moves(r, c, piece))
        elif piece.upper() == 'R':
            moves.extend(self._sliding_moves(r, c, piece, [(1,0),(-1,0),(0,1),(0,-1)]))
        elif piece.upper() == 'N':
            moves.extend(self._knight_moves(r, c, piece))
        elif piece.upper() == 'B':
            moves.extend(self._sliding_moves(r, c, piece, [(1,1),(1,-1),(-1,1),(-1,-1)]))
        elif piece.upper() == 'Q':
            moves.extend(self._sliding_moves(r, c, piece, [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]))
        elif piece.upper() == 'K':
            moves.extend(self._king_moves(r, c, piece))
        return moves

    def get_valid_moves(self):
        valid = []
        for move in self.get_all_moves():
            state_copy = copy.deepcopy(self)
            state_copy.make_move(move)
            if not state_copy.in_check(not state_copy.white_to_move):
                valid.append(move)
        return valid

    def in_check(self, white):
        king = 'K' if white else 'k'
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == king:
                    return self._square_under_attack(r, c, not white)
        return False

    def _square_under_attack(self, r, c, by_white):
        enemy_pawn = 'P' if by_white else 'p'
        enemy_knight = 'N' if by_white else 'n'
        enemy_bishop = 'B' if by_white else 'b'
        enemy_rook = 'R' if by_white else 'r'
        enemy_queen = 'Q' if by_white else 'q'
        enemy_king = 'K' if by_white else 'k'
        # pawn attacks
        directions = [(-1, -1), (-1, 1)] if by_white else [(1, -1), (1, 1)]
        for dr, dc in directions:
            rr, cc = r + dr, c + dc
            if 0 <= rr < 8 and 0 <= cc < 8 and self.board[rr][cc] == enemy_pawn:
                return True
        # knight attacks
        for dr, dc in [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]:
            rr, cc = r + dr, c + dc
            if 0 <= rr < 8 and 0 <= cc < 8 and self.board[rr][cc] == enemy_knight:
                return True
        # sliding attacks (rook/queen)
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            rr, cc = r + dr, c + dc
            while 0 <= rr < 8 and 0 <= cc < 8:
                piece = self.board[rr][cc]
                if piece != '.':
                    if piece == enemy_rook or piece == enemy_queen:
                        return True
                    break
                rr += dr; cc += dc
        # sliding attacks (bishop/queen)
        for dr, dc in [(1,1),(1,-1),(-1,1),(-1,-1)]:
            rr, cc = r + dr, c + dc
            while 0 <= rr < 8 and 0 <= cc < 8:
                piece = self.board[rr][cc]
                if piece != '.':
                    if piece == enemy_bishop or piece == enemy_queen:
                        return True
                    break
                rr += dr; cc += dc
        # king attacks
        for dr in (-1,0,1):
            for dc in (-1,0,1):
                if dr == 0 and dc == 0:
                    continue
                rr, cc = r + dr, c + dc
                if 0 <= rr < 8 and 0 <= cc < 8 and self.board[rr][cc] == enemy_king:
                    return True
        return False

    def _pawn_moves(self, r, c, piece):
        moves = []
        direction = -1 if piece.isupper() else 1
        start_row = 6 if piece.isupper() else 1
        # forward move
        if 0 <= r + direction < 8 and self.board[r+direction][c] == '.':
            moves.append(((r, c), (r+direction, c)))
            # double move
            if r == start_row and self.board[r+2*direction][c] == '.':
                moves.append(((r, c), (r+2*direction, c)))
        # captures
        for dc in (-1, 1):
            rr, cc = r+direction, c+dc
            if 0 <= rr < 8 and 0 <= cc < 8:
                target = self.board[rr][cc]
                if target != '.' and target.isupper() != piece.isupper():
                    moves.append(((r, c), (rr, cc)))
        return moves

    def _knight_moves(self, r, c, piece):
        moves = []
        for dr, dc in [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]:
            rr, cc = r+dr, c+dc
            if 0 <= rr < 8 and 0 <= cc < 8:
                target = self.board[rr][cc]
                if target == '.' or target.isupper() != piece.isupper():
                    moves.append(((r, c), (rr, cc)))
        return moves

    def _sliding_moves(self, r, c, piece, directions):
        moves = []
        for dr, dc in directions:
            rr, cc = r+dr, c+dc
            while 0 <= rr < 8 and 0 <= cc < 8:
                target = self.board[rr][cc]
                if target == '.':
                    moves.append(((r, c), (rr, cc)))
                else:
                    if target.isupper() != piece.isupper():
                        moves.append(((r, c), (rr, cc)))
                    break
                rr += dr; cc += dc
        return moves

    def _king_moves(self, r, c, piece):
        moves = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                rr, cc = r+dr, c+dc
                if 0 <= rr < 8 and 0 <= cc < 8:
                    target = self.board[rr][cc]
                    if target == '.' or target.isupper() != piece.isupper():
                        moves.append(((r, c), (rr, cc)))
        return moves

    def ai_move(self, depth=3):
        """
        Choose best move for current player using negamax with alpha-beta pruning.
        """
        import math
        best_score = -math.inf
        best_move = None
        for move in self.get_valid_moves():
            state_copy = copy.deepcopy(self)
            state_copy.make_move(move)
            score = -self._negamax(state_copy, depth-1, -math.inf, math.inf)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def _negamax(self, state, depth, alpha, beta):
        import math
        if depth == 0:
            return self.evaluate(state)
        valid_moves = state.get_valid_moves()
        if not valid_moves:
            # checkmate or stalemate
            if state.in_check(state.white_to_move):
                return -math.inf  # checkmate is worst
            return 0  # stalemate
        value = -math.inf
        for move in valid_moves:
            next_state = copy.deepcopy(state)
            next_state.make_move(move)
            score = -self._negamax(next_state, depth-1, -beta, -alpha)
            value = max(value, score)
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        return value

    def evaluate(self, state):
        """Simple material evaluation: positive if white is ahead."""
        values = {'K':0, 'Q':9, 'R':5, 'B':3, 'N':3, 'P':1,
                  'k':0, 'q':-9, 'r':-5, 'b':-3, 'n':-3, 'p':-1}
        score = 0
        for row in state.board:
            for piece in row:
                if piece in values:
                    score += values[piece]
        return score
