import pygame
import sys

pygame.init()

SIZE = 400
SQUARE_SIZE = SIZE // 8

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("Chess Game")

pieces = {}
for colour in ['w', 'b']:
    for piece in ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']:
        image = pygame.image.load(f'images/{colour}_{piece}.png')
        image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
        pieces[f'{colour}_{piece}'] = image

board = [
    ['b_rook', 'b_knight', 'b_bishop', 'b_queen', 'b_king', 'b_bishop', 'b_knight', 'b_rook'],
    ['b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn'],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ['w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn'],
    ['w_rook', 'w_knight', 'w_bishop', 'w_queen', 'w_king', 'w_bishop', 'w_knight', 'w_rook'],
]

selected_square = None
current_turn = 'w'

def draw_board():
    for row in range(8):
        for col in range(8):
            colour = WHITE if (row + col) % 2 == 0 else BLUE
            pygame.draw.rect(screen, colour, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = board[row][col]
            if piece:
                screen.blit(pieces[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def get_valid_moves(piece, row, col):
    moves = []
    piece_type = piece[2:]
    colour = piece[0]

    if piece_type == 'pawn':
        direction = -1 if colour == 'w' else 1
        if 0 <= row + direction < 8 and board[row + direction][col] is None:
            moves.append((row + direction, col))
            if (colour == 'w' and row == 6) or (colour == 'b' and row == 1):
                if board[row + 2 * direction][col] is None:
                    moves.append((row + 2 * direction, col))
        if col > 0 and 0 <= row + direction < 8 and board[row + direction][col - 1] and board[row + direction][col - 1][0] != colour:
            moves.append((row + direction, col - 1))
        if col < 7 and 0 <= row + direction < 8 and board[row + direction][col + 1] and board[row + direction][col + 1][0] != colour:
            moves.append((row + direction, col + 1))

    elif piece_type == 'rook':
        for d in [1, -1]:
            for r in range(1, 8):
                if 0 <= row + d * r < 8:
                    if board[row + d * r][col] is None:
                        moves.append((row + d * r, col))
                    elif board[row + d * r][col][0] != colour:
                        moves.append((row + d * r, col))
                        break
                    else:
                        break
        for d in [1, -1]:
            for c in range(1, 8):
                if 0 <= col + d * c < 8:
                    if board[row][col + d * c] is None:
                        moves.append((row, col + d * c))
                    elif board[row][col + d * c][0] != colour:
                        moves.append((row, col + d * c))
                        break
                    else:
                        break

    elif piece_type == 'knight':
        knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for move in knight_moves:
            new_row, new_col = row + move[0], col + move[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] is None or board[new_row][new_col][0] != colour:
                    moves.append((new_row, new_col))

    elif piece_type == 'bishop':
        for d_row, d_col in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for i in range(1, 8):
                new_row = row + d_row * i
                new_col = col + d_col * i
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if board[new_row][new_col] is None:
                        moves.append((new_row, new_col))
                    elif board[new_row][new_col][0] != colour:
                        moves.append((new_row, new_col))
                        break
                    else:
                        break

    elif piece_type == 'queen':
        for d in [1, -1]:
            for r in range(1, 8):
                if 0 <= row + d * r < 8:
                    if board[row + d * r][col] is None:
                        moves.append((row + d * r, col))
                    elif board[row + d * r][col][0] != colour:
                        moves.append((row + d * r, col))
                        break
                    else:
                        break
        for d in [1, -1]:
            for c in range(1, 8):
                if 0 <= col + d * c < 8:
                    if board[row][col + d * c] is None:
                        moves.append((row, col + d * c))
                    elif board[row][col + d * c][0] != colour:
                        moves.append((row, col + d * c))
                        break
                    else:
                        break
        for d_row, d_col in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for i in range(1, 8):
                new_row = row + d_row * i
                new_col = col + d_col * i
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if board[new_row][new_col] is None:
                        moves.append((new_row, new_col))
                    elif board[new_row][new_col][0] != colour:
                        moves.append((new_row, new_col))
                        break
                    else:
                        break

    elif piece_type == 'king':
        for d_row, d_col in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            new_row = row + d_row
            new_col = col + d_col
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] is None or board[new_row][new_col][0] != colour:
                    moves.append((new_row, new_col))

    return moves

def highlight_valid_moves(valid_moves):
    for move in valid_moves:
        pygame.draw.rect(screen, GREEN, (move[1] * SQUARE_SIZE, move[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

def main():
    global selected_square, current_turn
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
                if selected_square is None:
                    piece = board[row][col]
                    if piece and piece[0] == current_turn:
                        selected_square = (row, col)
                else:
                    piece = board[selected_square[0]][selected_square[1]]
                    valid_moves = get_valid_moves(piece, selected_square[0], selected_square[1])
                    if (row, col) in valid_moves:
                        board[row][col] = piece
                        board[selected_square[0]][selected_square[1]] = None
                        current_turn = 'b' if current_turn == 'w' else 'w'
                    selected_square = None

        draw_board()
        if selected_square:
            piece = board[selected_square[0]][selected_square[1]]
            valid_moves = get_valid_moves(piece, selected_square[0], selected_square[1])
            highlight_valid_moves(valid_moves)
        pygame.display.update()

main()

