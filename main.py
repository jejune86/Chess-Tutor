import pygame
import chess
import config
import copy
from chess_engine import get_best_move, STOCKFISH_PATH
from chess_logic import get_game_state
from chess_ui import draw_captured_pieces

# Pygame 초기화
pygame.init()
font = pygame.font.SysFont("sans-serif", 15)


# 화면 설정
 # 추가된 공간을 포함한 너비

screen = pygame.display.set_mode((config.screen_width, config.screen_height))
pygame.display.set_caption("Chess Game")

# 승리 확률 정보를 표시할 폰트 설정
def set_engine_difficulty(engine, level):
    try:
        engine.configure({"Skill Level": level})
    except chess.engine.EngineTerminatedError :
        # 엔진이 종료된 경우, 다시 시작합니다.
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        engine.configure({"Skill Level": level})
    return engine

win_probability_text = "Game in Progress"

ai_difficulty = 10
chess_running = True
selected_square = None  # 선택한 말의 위치를 저장하는 변수
current_state_index = 0 # 현재 보드 상태의 인덱스
best_move = None
last_move = None
last_moves = [] 


# 메인 게임 루프에서 잡은 기물을 관리하는 딕셔너리를 초기화합니다.
captured_pieces = {
    'white': [],
    'black': []
}

# 체스 보드 생성
board = chess.Board()
captured_pieces_history = [copy.deepcopy(captured_pieces)]
previous_board_states = [board.copy()]

with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
    engine.configure({"Skill Level": ai_difficulty})
    while chess_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                chess_running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 마우스 클릭 위치를 체스 보드 좌표로 변환
                x, y = pygame.mouse.get_pos()
                if x < config.board_size and y >= 40 and y < config.board_size + 40:
                    file = x // config.square_size
                    rank = 7 - (y - 40) // config.square_size  # 좌표를 체스 보드에 맞게 반전

                    clicked_square = chess.square(file, rank)
                    piece = board.piece_at(clicked_square)
                    if piece is not None and piece.color == board.turn:
                        if selected_square != clicked_square:
                            # 다른 기물 선택 시 색상 업데이트
                            selected_square = clicked_square
                            selected_rect = pygame.Rect((file * config.square_size),
                                                        ((7 - rank) * config.square_size) + 40,
                                                        config.square_size,
                                                        config.square_size)
                        else:
                            selected_square = None  # 같은 말을 다시 클릭한 경우 선택 해제
                            
                    elif selected_square is not None:
                        move = chess.Move(selected_square, clicked_square)
                        if move in board.legal_moves:
                            captured_piece = board.piece_at(move.to_square)
                            board.push(move)  # 보드 업데이트

                            if captured_piece:
                                if captured_piece.color == chess.WHITE:
                                    captured_pieces['black'].append(captured_piece)
                                else:
                                    captured_pieces['white'].append(captured_piece)
                            
                        selected_square = None  # 선택 해제

# ...

                        
                    else:
                        piece = board.piece_at(clicked_square)
                        if piece is not None and piece.color == board.turn:
                            selected_square = clicked_square
                            selected_rect = pygame.Rect((file * config.square_size),
                                                        ((7 - rank) * config.square_size) + 40,
                                                        config.square_size,
                                                        config.square_size)
                        
            elif event.type == pygame.KEYDOWN:
                # 'r' 키를 눌렀을 때 체스 보드 초기화
                if event.key == pygame.K_r:
                    current_state_index = 0
                    board.reset()
                    selected_square = None
                    previous_board_states = [board.copy()]  # 이전 상태 리스트 초기화
                    last_moves.clear()
                    last_move = None
                    captured_pieces = {'white': [], 'black': []}
                    captured_pieces_history = [copy.deepcopy(captured_pieces)]

                # 왼쪽 화살표를 눌렀을 때 이전 수로 되돌리기
                elif event.key == pygame.K_LEFT:
                    if current_state_index > 0:
                        current_state_index -= 1
                        board = previous_board_states[current_state_index].copy()
                        captured_pieces = captured_pieces_history[current_state_index].copy()
                        last_move = last_moves[current_state_index - 1] if current_state_index > 0 else None

                # 오른쪽 화살표 키를 눌렀을 때 다시 앞으로 진행
                elif event.key == pygame.K_RIGHT:
                    if current_state_index < len(previous_board_states) - 1:
                        current_state_index += 1
                        board = previous_board_states[current_state_index].copy()
                        captured_pieces = captured_pieces_history[current_state_index].copy()
                        last_move = last_moves[current_state_index - 1] if current_state_index > 0 else None


# ...

                    
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
                    best_move = get_best_move(engine, board, ai_difficulty)
                    
                    
                    
        # 화면 지우기
        screen.fill((255, 255, 255))

        # 체스 보드 그리기
        screen.blit(config.board_image, (0, 40))
        pygame.draw.rect(screen, (24,73,33), (0, 0, config.board_size, 40))
        pygame.draw.rect(screen, (24,73,33), (0, config.screen_height - 40, config.board_size, 40))
        # 마지막 움직임을 하늘색으로 표시합니다.
        if last_move:
            highlight_color = (135, 206, 250)  # 하늘색
            start_square = last_move.from_square
            end_square = last_move.to_square
            start_rect = pygame.Rect((start_square % 8) * config.square_size,
                                     (7 - start_square // 8) * config.square_size+40,
                                     config.square_size, config.square_size)
            end_rect = pygame.Rect((end_square % 8) * config.square_size, 
                                   (7 - end_square // 8) * config.square_size+40,
                                   config.square_size, config.square_size)
            pygame.draw.rect(screen, highlight_color, start_rect)
            pygame.draw.rect(screen, highlight_color, end_rect)
        
        if best_move:
            # 시작 위치와 목적지를 다른 색으로 강조합니다.
            start_square = best_move.from_square
            end_square = best_move.to_square
            start_rect = pygame.Rect((start_square % 8) * config.square_size,
                                     (7 - start_square // 8) * config.square_size+40,
                                     config.square_size, config.square_size)
            end_rect = pygame.Rect((end_square % 8) * config.square_size,
                                   (7 - end_square // 8) * config.square_size+40,
                                   config.square_size, config.square_size)
            pygame.draw.rect(screen, (0, 255, 0), start_rect)  # 시작 위치를 녹색으로 표시
            pygame.draw.rect(screen, (255, 0, 0), end_rect)  # 목적지를 빨간색으로 표시
        
        if selected_square:
            pygame.draw.rect(screen, (255,238,138), selected_rect)
            
        # 체스 기물 그리기
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                x = chess.square_file(square) * config.square_size
                y = (7 - chess.square_rank(square)) * config.square_size + 40
                screen.blit(config.piece_images[piece.symbol()], (x, y))

        # 승리 확률 정보 표시
        
        
        text_surface = font.render(win_probability_text, True, (0, 0, 0))
        text_surface_rect = text_surface.get_rect()
        text_surface_rect.topleft = (config.board_size + 10, 50)  # 승리 확률 정보를 추가 공간에 표시하는 위치 설정
        screen.blit(text_surface, text_surface_rect)
        
        difficulty_text = f"AI Difficulty: {ai_difficulty}"
        difficulty_surface = font.render(difficulty_text, True, (0, 0, 0))
        difficulty_surface_rect = difficulty_surface.get_rect()
        difficulty_surface_rect.topleft = (config.board_size + 10, 10)  # 승리 확률 정보 위에 난이도를 표시합니다.
        screen.blit(difficulty_surface, difficulty_surface_rect)
        
        draw_captured_pieces(screen, captured_pieces, config.top_bottom_space, config.square_size)
        
        pygame.display.flip()

        # AI 움직임 계산 및 수행
        if not board.is_game_over() and board.turn == chess.BLACK:
            if current_state_index < len(last_moves):
                # 이전 상태에서의 AI 움직임 재현
                move_to_replay = last_moves[current_state_index]
                board.push(move_to_replay)
                last_move = move_to_replay
                win_probability_text = get_game_state(board, engine, ai_difficulty)
                previous_board_states[current_state_index] = board.copy()
                captured_pieces_history[current_state_index] = copy.deepcopy(captured_pieces)
            else :
                result = engine.play(board, chess.engine.Limit(time=0.1))
                captured_piece = board.piece_at(result.move.to_square)
                board.push(result.move)
                last_move = result.move
                win_probability_text = get_game_state(board,engine,ai_difficulty)
                last_moves.append(last_move)
                if captured_piece:
                # 잡힌 기물의 색깔에 따라 리스트에 추가합니다.
                    if captured_piece.color == chess.WHITE:
                        captured_pieces['black'].append(captured_piece)
                    else:
                        captured_pieces['white'].append(captured_piece)
                        
                previous_board_states.append(board.copy())
                captured_pieces_history.append(copy.deepcopy(captured_pieces))
            current_state_index += 1
            
            

                
# Pygame 종료
pygame.quit()
