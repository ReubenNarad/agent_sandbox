import pygame

class PygameGUI:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.square_size = screen.get_width() // 8
        self.selected_sq = None
        self.moves = []
        self.font = pygame.font.SysFont(None, self.square_size // 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row = y // self.square_size
            col = x // self.square_size
            if self.selected_sq:
                move = (self.selected_sq, (row, col))
                if move in self.game_state.get_valid_moves():
                    # player's move
                    self.game_state.make_move(move)
                    # AI move
                    ai_move = self.game_state.ai_move()
                    if ai_move:
                        self.game_state.make_move(ai_move)
                self.selected_sq = None
            else:
                piece = self.game_state.board[row][col]
                if piece != '.' and ((piece.isupper() and self.game_state.white_to_move)
                                      or (piece.islower() and not self.game_state.white_to_move)):
                    self.selected_sq = (row, col)

    def draw(self):
        colors = [pygame.Color("white"), pygame.Color("gray")]
        for r in range(8):
            for c in range(8):
                color = colors[(r + c) % 2]
                rect = pygame.Rect(c*self.square_size, r*self.square_size,
                                   self.square_size, self.square_size)
                pygame.draw.rect(self.screen, color, rect)
                # highlight selected square
                if self.selected_sq == (r, c):
                    s = pygame.Surface((self.square_size, self.square_size), flags=pygame.SRCALPHA)
                    s.fill((255, 255, 0, 100))
                    self.screen.blit(s, rect.topleft)
                # draw piece
                piece = self.game_state.board[r][c]
                if piece != '.':
                    text = self.font.render(piece, True, pygame.Color("black"))
                    text_rect = text.get_rect(center=(c*self.square_size + self.square_size//2,
                                                      r*self.square_size + self.square_size//2))
                    self.screen.blit(text, text_rect)
