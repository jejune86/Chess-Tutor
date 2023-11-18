import pygame
import chess
import chess.svg
import chess.engine

# Pygame 초기화
pygame.init()

# 화면 설정
screen_width, screen_height = 640, 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Chess Game")

# 체스 보드 이미지 로드 (체스 보드 이미지 파일을 필요에 따라 바꿉니다)
board_image = pygame.image.load("assets/images/imgs-80px/chessboard.png")

piece_images = {
    'P': pygame.image.load("assets/images/imgs-80px/white_pawn.png"),  # 흰색 폰
    'R': pygame.image.load("assets/images/imgs-80px/white_rook.png"),  # 흰색 룩
    'N': pygame.image.load("assets/images/imgs-80px/white_knight.png"),  # 흰색 나이트
    'B': pygame.image.load("assets/images/imgs-80px/white_bishop.png"),  # 흰색 비숍
    'Q': pygame.image.load("assets/images/imgs-80px/white_queen.png"),  # 흰색 퀸
    'K': pygame.image.load("assets/images/imgs-80px/white_king.png"),  # 흰색 킹
    'p': pygame.image.load("assets/images/imgs-80px/black_pawn.png"),  # 검은색 폰
    'r': pygame.image.load("assets/images/imgs-80px/black_rook.png"),  # 검은색 룩
    'n': pygame.image.load("assets/images/imgs-80px/black_knight.png"),  # 검은색 나이트
    'b': pygame.image.load("assets/images/imgs-80px/black_bishop.png"),  # 검은색 비숍
    'q': pygame.image.load("assets/images/imgs-80px/black_queen.png"),  # 검은색 퀸
    'k': pygame.image.load("assets/images/imgs-80px/black_king.png"),  # 검은색 킹
}


# Stockfish 엔진 경로 설정
STOCKFISH_PATH = "stockfish/stockfish-windows-x86-64-avx2.exe"  # Stockfish 엔진 실행 파일의 경로를 설정하세요.

# 체스 보드 초기화
board = chess.Board()

# 체스 보드와 기물 이미지 크기 설정
board_size = min(screen_width, screen_height)
square_size = board_size // 8

running = True
selected_square = None  # 선택한 말의 위치를 저장하는 변수
previous_board_states = []  # 이전 체스 보드 상태를 저장하는 리스트

with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 마우스 클릭 위치를 체스 보드 좌표로 변환
                x, y = pygame.mouse.get_pos()
                file = x // square_size
                rank = 7 - y // square_size  # 좌표를 체스 보드에 맞게 반전

                # 클릭한 위치의 말을 선택하거나 이동 처리
                clicked_square = chess.square(file, rank)
                if selected_square is None:
                    # 선택한 말이 없는 경우, 클릭한 위치의 말을 선택
                    piece = board.piece_at(clicked_square)
                    if piece is not None and piece.color == board.turn:
                        selected_square = clicked_square
                else:
                    # 선택한 말이 있는 경우, 클릭한 위치로 움직임 수행
                    move = chess.Move(selected_square, clicked_square)
                    if move in board.legal_moves:
                        # 현재 보드 상태를 이전 상태 리스트에 저장
                        previous_board_states.append(board.copy())

                        board.push(move)  # 보드 업데이트
                    selected_square = None  # 선택 해제
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # 'r' 키를 눌렀을 때 체스 보드 초기화
                    board.reset()
                    selected_square = None
                    previous_board_states.clear()  # 이전 상태 리스트 초기화
                elif event.key == pygame.K_u:
                    # 'u' 키를 눌렀을 때 이전 수로 되돌리기
                    if previous_board_states:
                        board = previous_board_states.pop()
                        selected_square = None

        # 화면 지우기
        screen.fill((255, 255, 255))

        # 체스 보드 그리기
        screen.blit(board_image, (0, 0))

        # 체스 기물 그리기
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                x = chess.square_file(square) * square_size
                y = (7 - chess.square_rank(square)) * square_size
                screen.blit(piece_images[piece.symbol()], (x, y))

        pygame.display.flip()



        # AI 움직임 계산 및 수행
        if not board.is_game_over() and board.turn == chess.BLACK:
            result = engine.play(board, chess.engine.Limit(time=1.0))
            board.push(result.move)

# Pygame 종료
pygame.quit()
