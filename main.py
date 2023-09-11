import pygame
import button
import random

pygame.init()
pygame.font.init()
cell_color = (0,0,0)
selected_color = (0, 128, 0)
remove_number = 30
running = True
input_mode = False
my_font = pygame.font.SysFont('Comic Sans MS', 30)
grid_size = 9
square_size = 60
grid_width = 2 
screen_length = 1350
screen_width = 720
screen = pygame.display.set_mode((screen_length, screen_width))

#title
pygame.display.set_caption("Sudoku")
icon = pygame.image.load('D:\Code\C++\Projects\Sudoku game\images\sudoku_icon.png')
pygame.display.set_icon(icon)

#background
background = pygame.image.load('D:\Code\C++\Projects\Sudoku game\images\menu.png')

#player
player_img = pygame.image.load('D:\Code\C++\Projects\Sudoku game\images\pencil_mouse.png')
#pygame.mouse.set_visible(False)
def player(x):
    screen.blit(player_img, (x)) 

#button
start_button = button.Button('NEW GAME', 31, 221, (552, 305), 6)
exit_button = button.Button('EXIT', 31, 221, (552,445), 6 )

#new game
def play():
    #check whether the number will be legal to assign to the given row, col
    def issafe(board, row, col, num):
        for x in range (9):
            if board[row][x] == num :
                return False
        for x in range(9):
            if board[x][col] == num :
                return False
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num :
                    return False
        return True 
    
    def solve_board(board, row, col):
        if (row == 8 and col == 9):
            return True
        if col == 9 :
            row += 1 
            col = 0 
        if board[row][col] > 0 : 
            return solve_board(board, row, col + 1) 
        for num in range(1, 10):
            if issafe(board, row, col, num) :
                board[row][col] = num 
                if solve_board(board, row, col + 1) :
                    return True
                board[row][col] = 0
        return False
   
    def remove_numbers(board, num_removed) :
        cells = [(row, col) for row in range(grid_size) for col in range(grid_size)]
        random.shuffle(cells) 

        for row, col in cells:
            temp = board[row][col]
            board[row][col] = 0

            board_copy = [row[:] for row in board]
            #check if the current board is still solveable
            if not (solve_board(board_copy, 0, 0)):
                board[row][col] = temp
            num_removed -= 1 
            if(num_removed == 0):
                break

    #generate sudoku board
    def generate_board():
        board = [[0] * grid_size for _ in range(grid_size)] 
        initial_cells = [[False] * grid_size for _ in range(grid_size)]
        solve_board(board,0,0)
        remove_numbers(board, remove_number)

        for row in range (grid_size):
            for col in range (grid_size) :
                if board[row][col] != 0 :
                    initial_cells[row][col] = True
        return board, initial_cells
    
    #draw numbers to sudoku board
    def  draw_board(board,initial_cells, selected_cell):
        for i in range(0, 10) :
            if(i % 3 == 0):
                pygame.draw.line(screen, (0,0,0), (440 + 60 * i, 100), (440 + 60*i, 640), 4)
                pygame.draw.line(screen, (0,0,0), (440, 100 + 60 * i), (980, 100 + 60 * i), 4)
            else:
                pygame.draw.line(screen, (0,0,0), (440 + 60 * i, 100), (440 + 60*i, 640), 2)
                pygame.draw.line(screen, (0,0,0), (440, 100 + 60 * i), (980, 100 + 60 * i), 2)
        for row in range(grid_size):
            for col in range(grid_size):
                x = col * square_size + 440
                y = row * square_size + 100
                if(row, col) == selected_cell:
                    pygame.draw.rect(screen, selected_color, (x,y , square_size, square_size), grid_width) #(x, y, width, height)
                if board[row][col] != 0 and initial_cells[row][col]:
                    number_text = my_font.render(str(board[row][col]), True, (0,0,0))
                    number_rect = number_text.get_rect(center = (col * square_size + 470 , row * square_size + 130))
                    screen.blit(number_text, number_rect)
                elif board[row][col] != 0 and initial_cells[row][col] == False:                   
                    number_text = my_font.render(str(board[row][col]), True, (255,0,0))
                    number_rect = number_text.get_rect(center = (col * square_size + 470 , row * square_size + 130))
                    screen.blit(number_text, number_rect)
                
    
    #handle user input    
    def handle_mouse_click(x,y):
        global selected_cell, input_mode
        if(x < 440 or x > 980 or y < 100 or y > 640) :
            selected_cell = None
            return 
        row = (y - 100) // 60
        col = (x - 440) // 60
        selected_cell = (row, col)
        input_mode = True

    def handle_key_press(key) :
        global input_mode,undefined_num 
        if (pygame.K_1 <= key <= pygame.K_9) and input_mode == True:
            number = int(pygame.key.name(key))
            if(selected_cell[0] >= 0 and selected_cell[1] >= 0 and selected_cell[0] < 9 and selected_cell[1] < 9):
                row,col = selected_cell
                if(row < 9 and col < 9 and initial_cells[row][col] == False):               
                    board[row][col] = number
                input_mode = False 
                undefined_num = 0
                for row in range (grid_size):
                    for col in range (grid_size) :
                        if board[row][col] == 0 :
                            undefined_num += 1
                if(undefined_num  == 0 and solve_board(board, 0, 0)):
                    print("Finish")


    #main game funtion
    board, initial_cells = generate_board() 
   
    playing = True

    while playing:
        screen.fill((255,255,255))
        draw_board(board, initial_cells, None)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #handle mouse click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                handle_mouse_click(mouse_x, mouse_y)
                draw_board(board, initial_cells, selected_cell,)
                pygame.display.update() 
            elif event.type == pygame.KEYDOWN:
                handle_key_press(event.key)
                draw_board(board, initial_cells, None)
                pygame.display.update()
        if input_mode == False:
            pygame.display.update()
        
#game loop


while running:
    screen.fill((255,255,255))
    screen.blit(background,(0,0))
    mouse_pos = pygame.mouse.get_pos() 
    start_button.draw(screen, mouse_pos)
    exit_button.draw(screen, mouse_pos)

    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exit_button.top_rect.collidepoint(mouse_pos):
                running = False
            if start_button.top_rect.collidepoint(mouse_pos):
                play()
                running = False 

            
    #player(mouse_pos)
    pygame.display.update()

pygame.quit()