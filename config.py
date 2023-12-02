import pygame
pygame.init()
pygame.mixer.init()
font = pygame.font.SysFont("sans-serif", 30)
screen_width, screen_height = 1000, 720 
board_size = 640
square_size = 80
top_bottom_space = 40

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Chess Tutor")



board_image = pygame.image.load("assets/images/chessboard.png")
piece_images = {
    'P': pygame.image.load("assets/images/white_pawn.png"),  
    'R': pygame.image.load("assets/images/white_rook.png"), 
    'N': pygame.image.load("assets/images/white_knight.png"),  
    'B': pygame.image.load("assets/images/white_bishop.png"),  
    'Q': pygame.image.load("assets/images/white_queen.png"), 
    'K': pygame.image.load("assets/images/white_king.png"),  
    'p': pygame.image.load("assets/images/black_pawn.png"),  
    'r': pygame.image.load("assets/images/black_rook.png"),  
    'n': pygame.image.load("assets/images/black_knight.png"),  
    'b': pygame.image.load("assets/images/black_bishop.png"),  
    'q': pygame.image.load("assets/images/black_queen.png"),  
    'k': pygame.image.load("assets/images/black_king.png"),  
}
tooltip_image = pygame.image.load("assets/images/tooltip.png")
dr_image = pygame.image.load("assets/images/DrCat.png")


move_sound = pygame.mixer.Sound('assets/sound/move.wav')