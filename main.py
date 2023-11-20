import pygame
import chess
import chess.engine

# Pygame 초기화
pygame.init()

# 화면 설정
screen_width, screen_height = 960, 640  # 추가된 공간을 포함한 너비
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Chess Game")

# 승리 확률 정보를 표시할 폰트 설정
font = pygame.font.SysFont("arial", 15)

# Stockfish 엔진 경로 설정
STOCKFISH_PATH = "stockfish/stockfish-windows-x86-64-avx2.exe"  # Stockfish 엔진 실행 파일의 경로를 설정하세요.

# 현재 보드 상태를 기반으로 승리 확률 계산
def calculate_win_probability(board):
    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        result = engine.analyse(board, chess.engine.Limit(time=0.1))  # 시간 제한을 설정하세요.
        if "score" in result:
            score = result["score"].relative.score()
            if score is not None:
                if score > 0:
                    return f"White is Winning (+{score/100:.2f})"
                elif score < 0:
                    return f"Black is Winning ({score/100:.2f})"
        return "Game in progress"

def get_game_state(board):
    if board.is_checkmate():
        # 체크메이트인 경우, 현재 턴의 반대 색깔이 이긴 것입니다.
        if board.turn:
            return "Black checkmate"
        else:
            return "White checkmate"
    elif board.is_stalemate():
        return "Stalemate"
    elif board.is_insufficient_material():
        return "Draw due to insufficient material"
    elif board.is_seventyfive_moves():
        return "Draw due to 75-move rule"
    elif board.is_fivefold_repetition():
        return "Draw due to five-fold repetition"
    elif board.can_claim_draw():
        return "Draw claimable"
    # 이외의 게임 진행 중인 상태에서는 승리 확률을 계산합니다.
    return calculate_win_probability(board)

# 난이도 조절 버튼을 눌렀을 때 호출될 함수를 정의합니다.
def set_engine_difficulty(engine, level):
    try:
        # 엔진 설정을 변경합니다.
        engine.configure({"Skill Level": level})
    except chess.engine.EngineTerminatedError:
        # 엔진이 종료된 경우, 다시 시작합니다.
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        engine.configure({"Skill Level": level})
    return engine

def get_best_move(engine, board):
    # 최적의 수 계산을 위해 임시로 엔진의 난이도를 최대로 설정합니다.
    engine.configure({"Skill Level": 20})
    result = engine.play(board, chess.engine.Limit(time=0.1))
    best_move = result.move
    # 계산이 끝난 후 원래 난이도로 되돌립니다.
    engine.configure({"Skill Level": ai_difficulty})
    return best_move


# 체스 보드 이미지 로드 (체스 보드 이미지 파일을 필요에 따라 바꿉니다)
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

# 체스 보드 생성
board = chess.Board()

# 체스 보드와 기물 이미지 크기 설정
board_size = 640
square_size = 80

chess_running = True
selected_square = None  # 선택한 말의 위치를 저장하는 변수
previous_board_states = []  # 이전 체스 보드 상태를 저장하는 리스트

win_probability_text = "Game in Progress"

ai_difficulty = 10

best_move = None
last_move = None

with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
    engine.configure({"Skill Level": ai_difficulty})
    while chess_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                chess_running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 마우스 클릭 위치를 체스 보드 좌표로 변환
                x, y = pygame.mouse.get_pos()
                if x < board_size:
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
                            win_probability_text = get_game_state(board)
                            best_move = None
                            last_move = None
                        selected_square = None
                        
                    
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
                    win_probability_text = get_game_state(board)
                elif event.key == pygame.K_UP:
                # 위 화살표를 누르면 난이도를 증가시킵니다.
                    ai_difficulty = min(ai_difficulty + 1, 20)
                    engine = set_engine_difficulty(engine, ai_difficulty)
                elif event.key == pygame.K_DOWN:
                    # 아래 화살표를 누르면 난이도를 감소시킵니다.
                    ai_difficulty = max(ai_difficulty - 1, 0)
                    engine = set_engine_difficulty(engine, ai_difficulty)
                elif event.key == pygame.K_SPACE:
                    # 스페이스바를 눌렀을 때 최적의 수를 계산합니다.
                    result = engine.play(board, chess.engine.Limit(time=0.1))
                    best_move = get_best_move(engine, board)
                    
                    
                    
        # 화면 지우기
        screen.fill((255, 255, 255))

        # 체스 보드 그리기
        screen.blit(board_image, (0, 0))
        
        # 마지막 움직임을 하늘색으로 표시합니다.
        if last_move:
            highlight_color = (135, 206, 250)  # 하늘색
            start_square = last_move.from_square
            end_square = last_move.to_square
            start_rect = pygame.Rect((start_square % 8) * square_size, (7 - start_square // 8) * square_size, square_size, square_size)
            end_rect = pygame.Rect((end_square % 8) * square_size, (7 - end_square // 8) * square_size, square_size, square_size)
            pygame.draw.rect(screen, highlight_color, start_rect)
            pygame.draw.rect(screen, highlight_color, end_rect)
        
        if best_move:
            # 시작 위치와 목적지를 다른 색으로 강조합니다.
            start_square = best_move.from_square
            end_square = best_move.to_square
            start_rect = pygame.Rect((start_square % 8) * square_size, (7 - start_square // 8) * square_size, square_size, square_size)
            end_rect = pygame.Rect((end_square % 8) * square_size, (7 - end_square // 8) * square_size, square_size, square_size)
            pygame.draw.rect(screen, (0, 255, 0), start_rect)  # 시작 위치를 녹색으로 표시
            pygame.draw.rect(screen, (255, 0, 0), end_rect)  # 목적지를 빨간색으로 표시

        # 체스 기물 그리기
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                x = chess.square_file(square) * square_size
                y = (7 - chess.square_rank(square)) * square_size
                screen.blit(piece_images[piece.symbol()], (x, y))

        # 승리 확률 정보 표시
        
        
        text_surface = font.render(win_probability_text, True, (0, 0, 0))
        text_surface_rect = text_surface.get_rect()
        text_surface_rect.topleft = (board_size + 10, 50)  # 승리 확률 정보를 추가 공간에 표시하는 위치 설정
        screen.blit(text_surface, text_surface_rect)
        
        difficulty_text = f"AI Difficulty: {ai_difficulty}"
        difficulty_surface = font.render(difficulty_text, True, (0, 0, 0))
        difficulty_surface_rect = difficulty_surface.get_rect()
        difficulty_surface_rect.topleft = (board_size + 10, 10)  # 승리 확률 정보 위에 난이도를 표시합니다.
        screen.blit(difficulty_surface, difficulty_surface_rect)
        
        pygame.display.flip()

        # AI 움직임 계산 및 수행
        if not board.is_game_over() and board.turn == chess.BLACK:
            result = engine.play(board, chess.engine.Limit(time=1.0))
            board.push(result.move)
            last_move = result.move
            win_probability_text = get_game_state(board)
            
# Pygame 종료
pygame.quit()
