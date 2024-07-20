import pygame
import random
import sys
from pygame.locals import *

def pattern(r, c): return (3*(r % 3) + r // 3 + c) % 9
def shuffle(s): return random.sample(s, len(s))

def generate_board():
    rBase = range(3)
    rows  = [ g*3 + r for g in shuffle(rBase) for r in shuffle(rBase) ]
    cols  = [ g*3 + c for g in shuffle(rBase) for c in shuffle(rBase) ]
    nums  = shuffle(range(1, 10))

    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    squares = 9 * 9
    empties = squares * 3 // 4
    for p in random.sample(range(squares), empties):
        board[p // 9][p % 9] = 0

    return board

def solve(board):
    def is_valid(board, r, c, num):
        for i in range(9):
            if board[i][c] == num or board[r][i] == num:
                return False
        startRow, startCol = 3 * (r // 3), 3 * (c // 3)
        for i in range(3):
            for j in range(3):
                if board[i + startRow][j + startCol] == num:
                    return False
        return True

    def solve_board(board):
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    for num in range(1, 10):
                        if is_valid(board, r, c, num):
                            board[r][c] = num
                            if solve_board(board):
                                return True
                            board[r][c] = 0
                    return False
        return True

    board_copy = [row[:] for row in board]
    solve_board(board_copy)
    return board_copy

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

WINDOW_SIZE = 540
GRID_SIZE = 9
CELL_SIZE = WINDOW_SIZE // GRID_SIZE

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Sudoku')

font = pygame.font.SysFont("comicsans", 40)

board = generate_board()
solved_board = solve(board)
user_entries = [[False] * 9 for _ in range(9)]

def draw_board():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = board[row][col]
            if value != 0:
                text = font.render(str(value), True, BLACK)
                screen.blit(text, (col * CELL_SIZE + 20, row * CELL_SIZE + 10))
            elif user_entries[row][col]:
                text = font.render(str(value), True, RED)
                screen.blit(text, (col * CELL_SIZE + 20, row * CELL_SIZE + 10))

    for i in range(GRID_SIZE + 1):
        if i % 3 == 0:
            thickness = 4
        else:
            thickness = 1
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE), thickness)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE), thickness)

def draw_selected_cell(row, col):
    pygame.draw.rect(screen, BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

def get_cell(pos):
    x, y = pos
    return y // CELL_SIZE, x // CELL_SIZE

selected = None

while True:
    screen.fill(WHITE)
    draw_board()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            selected = get_cell(pos)
        if event.type == KEYDOWN:
            if selected and event.key == K_s:  #Solutions are shown by pressing the s key
                board = solved_board
            if selected and event.unicode.isdigit():
                row, col = selected
                if board[row][col] == 0 or user_entries[row][col]:
                    value = int(event.unicode)
                    if solved_board[row][col] == value:
                        board[row][col] = value
                        user_entries[row][col] = True
                    else:
                        print("Incorrect value.")

    if selected:
        draw_selected_cell(*selected)

    pygame.display.update()
