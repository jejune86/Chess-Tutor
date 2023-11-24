import pygame

board_size = 640
square_size = 80
top_bottom_space = 40

  # 이전 체스 보드 상태를 저장하는 리스트

board_image = pygame.image.load("assets/images/chessboard.png")
piece_images = {
    'P': pygame.image.load("assets/images/white_pawn.png"),  # 흰색 폰
    'R': pygame.image.load("assets/images/white_rook.png"),  # 흰색 룩
    'N': pygame.image.load("assets/images/white_knight.png"),  # 흰색 나이트
    'B': pygame.image.load("assets/images/white_bishop.png"),  # 흰색 비숍
    'Q': pygame.image.load("assets/images/white_queen.png"),  # 흰색 퀸
    'K': pygame.image.load("assets/images/white_king.png"),  # 흰색 킹
    'p': pygame.image.load("assets/images/black_pawn.png"),  # 검은색 폰
    'r': pygame.image.load("assets/images/black_rook.png"),  # 검은색 룩
    'n': pygame.image.load("assets/images/black_knight.png"),  # 검은색 나이트
    'b': pygame.image.load("assets/images/black_bishop.png"),  # 검은색 비숍
    'q': pygame.image.load("assets/images/black_queen.png"),  # 검은색 퀸
    'k': pygame.image.load("assets/images/black_king.png"),  # 검은색 킹
}

screen_width, screen_height = 960, 720 