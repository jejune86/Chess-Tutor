import copy
import config
import pygame
import chess
from chess_engine import set_engine_difficulty, get_best_move, get_game_state, move_analysis

class ChessGame:
    def __init__(self, board, engine):
        self.chess_running = True
        self.ai_difficulty = 10
        self.engine = engine
        self.current_state_index = 0
        self.selected_square = None
        self.selected_rect = None
        self.board = board
        self.previous_board_states = [board.copy()]
        self.last_moves = []
        self.last_move = None
        self.best_move = None
        self.captured_pieces = {'white': [], 'black': []}
        self.captured_pieces_history = [copy.deepcopy(self.captured_pieces)]
        self.win_probability_text = "Game in Progress"
        self.baord_win_rate = [[0,0]]
        self.move_analysis_text = "Game Start"
    
    def event_handle(self, event) :
        if event.type == pygame.QUIT:
            self.chess_running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 마우스 클릭 위치를 체스 보드 좌표로 변환
            self.click()
                    
        elif event.type == pygame.KEYDOWN:
            # 'r' 키를 눌렀을 때 체스 보드 초기화
            if event.key == pygame.K_r:
                self.keydown_R()
            # 왼쪽 화살표를 눌렀을 때 이전 수로 되돌리기
            elif event.key == pygame.K_LEFT:
                self.keydown_Left()
            # 오른쪽 화살표 키를 눌렀을 때 다시 앞으로 진행
            elif event.key == pygame.K_RIGHT:
                self.keydown_Right()

            elif event.key == pygame.K_UP:
            # 위 화살표를 누르면 난이도를 증가시킵니다.
                self.keydown_Up()
            elif event.key == pygame.K_DOWN:
                # 아래 화살표를 누르면 난이도를 감소시킵니다.
                self.keydown_Down()
            elif event.key == pygame.K_SPACE:
                self.keydown_Space()   

    def keydown_R(self):
        self.current_state_index = 0
        self.board.reset()
        self.selected_square = None
        self.previous_board_states = [self.board.copy()]
        self.last_moves.clear()
        self.last_move = None
        self.best_move = None
        self.captured_pieces = {'white': [], 'black': []}
        self.captured_pieces_history = [copy.deepcopy(self.captured_pieces)]
        self.move_anlysis_text = None
        self.win_probability_text = "Game in Progress"
        self.baord_win_rate = [[0,0]]
        self.move_analysis_text = "Game Start"

# 왼쪽 화살표를 눌렀을 때 이전 수로 되돌리기
    def keydown_Left(self):
        if self.current_state_index > 0:
            self.current_state_index -= 1
            self.board = self.previous_board_states[self.current_state_index].copy()
            self.captured_pieces = self.captured_pieces_history[self.current_state_index].copy()
            self.last_move = self.last_moves[self.current_state_index - 1] if self.current_state_index > 0 else None
            self.move_anlysis_text = move_analysis(self)
            self.win_probability_text = get_game_state(self)
                # 오른쪽 화살표 키를 눌렀을 때 다시 앞으로 진행
    def keydown_Right(self) :
        if self.current_state_index < len(self.previous_board_states) - 1:
            self.current_state_index += 1
            self.board = self.previous_board_states[self.current_state_index].copy()
            self.captured_pieces = self.captured_pieces_history[self.current_state_index].copy()
            self.last_move = self.last_moves[self.current_state_index - 1] if self.current_state_index > 0 else None
            

    def keydown_Up(self):
    # 위 화살표를 누르면 난이도를 증가시킵니다.
        self.ai_difficulty = min(self.ai_difficulty + 1, 20)
        self.engine = set_engine_difficulty(self.engine, self.ai_difficulty)
    
    def keydown_Down(self):
        # 아래 화살표를 누르면 난이도를 감소시킵니다.
        self.ai_difficulty = max(self.ai_difficulty - 1, 0)
        self.engine = set_engine_difficulty(self.engine, self.ai_difficulty)
   
    def keydown_Space(self):
        self.best_move = get_best_move(self.engine, self.board, self.ai_difficulty)

    def click(self):
        x, y = pygame.mouse.get_pos()
        if x < config.board_size and y >= 40 and y < config.board_size + 40:
            file = x // config.square_size
            rank = 7 - (y - 40) // config.square_size  # 좌표를 체스 보드에 맞게 반전

            clicked_square = chess.square(file, rank)
            piece = self.board.piece_at(clicked_square)
            if piece is not None and piece.color == self.board.turn:
                if self.selected_square != clicked_square:
                    # 다른 기물 선택 시 색상 업데이트
                    self.selected_square = clicked_square
                    self.selected_rect = pygame.Rect((file * config.square_size),
                                                ((7 - rank) * config.square_size) + 40,
                                                config.square_size,
                                                config.square_size)
                else:
                    self.selected_square = None  # 같은 말을 다시 클릭한 경우 선택 해제
                    
            elif self.selected_square is not None:
                move = chess.Move(self.selected_square, clicked_square)
                if move in self.board.legal_moves:
                    self.captured_piece = self.board.piece_at(move.to_square)
                    self.board.push(move)  # 보드 업데이트

                    if self.captured_piece:
                        if self.captured_piece.color == chess.WHITE:
                            self.captured_pieces['black'].append(self.captured_piece)
                        else:
                            self.captured_pieces['white'].append(self.captured_piece)
                    
                self.selected_square = None  # 선택 해제
                self.best_move = None
                self.move_anlysis_text = move_analysis(self)
                                
            else:
                piece = self.board.piece_at(clicked_square)
                if piece is not None and piece.color == self.board.turn:
                    self.selected_square = clicked_square
                    self.selected_rect = pygame.Rect((file * config.square_size),
                                                ((7 - rank) * config.square_size) + 40,
                                                config.square_size,
                                                config.square_size)
                    
    def ai_movement(self) :
        if not self.board.is_game_over() and self.board.turn == chess.BLACK:
            if self.current_state_index < len(self.last_moves):
                # 이전 상태에서의 AI 움직임 재현
                move_to_replay = self.last_moves[self.current_state_index]
                self.board.push(move_to_replay)
                self.last_move = move_to_replay
                self.win_probability_text = get_game_state(self)
                self.previous_board_states[self.current_state_index] = self.board.copy()
                self.captured_pieces_history[self.current_state_index] = copy.deepcopy(self.captured_pieces)
            else :
                result = self.engine.play(self.board, chess.engine.Limit(time=0.1))
                self.captured_piece = self.board.piece_at(result.move.to_square)
                self.board.push(result.move)
                self.last_move = result.move
                self.win_probability_text = get_game_state(self)
                self.last_moves.append(self.last_move)
                if self.captured_piece:
                # 잡힌 기물의 색깔에 따라 리스트에 추가합니다.
                    if self.captured_piece.color == chess.WHITE:
                        self.captured_pieces['black'].append(self.captured_piece)
                    else:
                        self.captured_pieces['white'].append(self.captured_piece)
                        
                self.previous_board_states.append(self.board.copy())
                self.captured_pieces_history.append(copy.deepcopy(self.captured_pieces))
            self.current_state_index += 1                
        