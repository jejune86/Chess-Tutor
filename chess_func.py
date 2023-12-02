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
        self.win_probability_text = ""
        self.move_analysis_text = "Let's get started!"
        self.undo = False
        self.promotion = False
        self.promo_move = None
        self.board_analysis = None
    
    def event_handle(self, event) :
        if event.type == pygame.QUIT:
            self.chess_running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.click()
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.keydown_R()
            elif event.key == pygame.K_LEFT:
                self.keydown_Left()
            elif event.key == pygame.K_RIGHT:
                self.keydown_Right()
            elif event.key == pygame.K_UP:
                self.keydown_Up()
            elif event.key == pygame.K_DOWN:
                self.keydown_Down()
            elif event.key == pygame.K_SPACE:
                self.keydown_Space()   
            elif event.key == pygame.K_q:
                self.chess_running = False
                

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
        self.move_analysis_text = None
        self.win_probability_text = ""
        self.move_analysis_text = "Let's get started!"
        self.undo = False
        self.promotion = False
        self.promo_move = None
        self.board_analysis = None


    def keydown_Left(self):
        if self.board.is_game_over() :
            self.board = self.previous_board_states[self.current_state_index].copy()
            self.captured_pieces = self.captured_pieces_history[self.current_state_index].copy()
            self.last_move = self.last_moves[self.current_state_index - 1] if self.current_state_index > 0 else None
            self.get_analysis()
            self.win_probability_text = get_game_state(self)
            self.best_move = None
            self.undo = True 
            config.move_sound.play()
            
        elif self.current_state_index > 0:
            self.current_state_index -= 1
            self.board = self.previous_board_states[self.current_state_index].copy()
            self.captured_pieces = self.captured_pieces_history[self.current_state_index].copy()
            self.last_move = self.last_moves[self.current_state_index - 1] if self.current_state_index > 0 else None
            self.get_analysis()
            self.win_probability_text = get_game_state(self)
            self.best_move = None
            self.undo = True
            config.move_sound.play()
              
    def keydown_Right(self) :
        if self.current_state_index < len(self.previous_board_states) - 1:
            self.current_state_index += 1
            self.board = self.previous_board_states[self.current_state_index].copy()
            self.captured_pieces = self.captured_pieces_history[self.current_state_index].copy()
            self.last_move = self.last_moves[self.current_state_index - 1] if self.current_state_index > 0 else None
            self.best_move = None
            self.get_analysis()
            self.win_probability_text = get_game_state(self)
            config.move_sound.play()

    def keydown_Up(self):
        self.ai_difficulty = min(self.ai_difficulty + 1, 25)
        self.engine = set_engine_difficulty(self.engine, self.ai_difficulty)
    
    def keydown_Down(self):
        self.ai_difficulty = max(self.ai_difficulty - 1, 0)
        self.engine = set_engine_difficulty(self.engine, self.ai_difficulty)
   
    def keydown_Space(self):
        self.best_move = get_best_move(self)


    def click(self):
        x, y = pygame.mouse.get_pos()

        if self.promotion:
            prev_board = self.board.copy() 
            piece_type = self.handle_promotion_click(x, y)
            if piece_type is not None:
                self.promo_move.promotion = piece_type
                move = self.promo_move
                self.captured_piece = self.board.piece_at(move.to_square)
                self.board.push(move)  
                if self.captured_piece:
                    if self.captured_piece.color == chess.WHITE:
                        self.captured_pieces['black'].append(self.captured_piece)
                    else:
                        self.captured_pieces['white'].append(self.captured_piece)
                        
                self.get_analysis()
                self.move_analysis_text = move_analysis(self, prev_board, move)
                self.undo = False
                self.selected_rect = None
                self.selected_square = None  
                self.best_move = None
                self.promotion = False
                self.promo_move = None
                self.win_probability_text = get_game_state(self)
                config.move_sound.play()
                return 
            
        if x < config.board_size and y >= 40 and y < config.board_size + 40:
            prev_board = self.board.copy()   
            file = x // config.square_size
            rank = 7 - (y - 40) // config.square_size  
            
            clicked_square = chess.square(file, rank)
            piece = self.board.piece_at(clicked_square)
            
            if piece is not None and piece.color == self.board.turn:
                if self.selected_square is None or self.selected_square != clicked_square:
                    self.selected_square = clicked_square
                    self.selected_rect = pygame.Rect((file * config.square_size),
                                                ((7 - rank) * config.square_size) + 40,
                                                config.square_size,
                                                config.square_size)
                else:
                    self.selected_square = None 
                    self.selected_rect = None
                    
            elif self.selected_square is not None:
                move = chess.Move(self.selected_square, clicked_square)
                p_move = chess.Move(self.selected_square, clicked_square,chess.QUEEN)
                
                if p_move in self.board.legal_moves :
                    self.promotion = True
                    self.promo_move = move
                    return
                
                if move in self.board.legal_moves :
                    self.captured_piece = self.board.piece_at(move.to_square)
                    if self.captured_piece:
                        if self.captured_piece.color == chess.WHITE:
                            self.captured_pieces['black'].append(self.captured_piece)
                        else:
                            self.captured_pieces['white'].append(self.captured_piece)
                    self.board.push(move)  
                    self.get_analysis()
                    self.move_analysis_text = move_analysis(self, prev_board, move)
                    self.win_probability_text = get_game_state(self)
                    self.undo = False
                    config.move_sound.play()
                                        
                self.selected_square = None 
                self.best_move = None
                
                
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
            if self.undo:
                move_to_replay = self.last_moves[self.current_state_index-1]
                self.board.push(move_to_replay)
                self.last_move = move_to_replay
                self.get_analysis()
                self.win_probability_text = get_game_state(self)
            else :
                result = self.engine.play(self.board, chess.engine.Limit(time=0.1))
                self.captured_piece = self.board.piece_at(result.move.to_square)
                self.board.push(result.move)
                self.last_move = result.move
                self.get_analysis()
                self.win_probability_text = get_game_state(self)
                self.last_moves = self.last_moves[:self.current_state_index]
                self.last_moves.append(self.last_move)
                if self.captured_piece:
                    if self.captured_piece.color == chess.WHITE:
                        self.captured_pieces['black'].append(self.captured_piece)
                    else:
                        self.captured_pieces['white'].append(self.captured_piece)
                self.previous_board_states = self.previous_board_states[:self.current_state_index+1]
                self.previous_board_states.append(self.board.copy())
                self.captured_pieces_history = self.captured_pieces_history[:self.current_state_index+1]
                self.captured_pieces_history.append(copy.deepcopy(self.captured_pieces)) 
            
            if self.board.is_game_over() :
                if self.board.is_checkmate() :
                    if self.board.turn:
                        self.move_analysis_text = "Checkmate. \nTry again..."
                    else:
                        self.move_analysis_text = "Checkmate! \nYou win!!"
                elif self.board.is_stalemate():
                    self.move_analysis_text = "Stalemate, Draw!"
                elif self.board.is_insufficient_material():
                    self.move_analysis_text = "Draw!"
                elif self.board.is_seventyfive_moves():
                    self.move_analysis_text = "Draw!"
                elif self.board.is_fivefold_repetition():
                    self.move_analysis_text = "Draw!"
                elif self.board.can_claim_draw():
                    self.move_analysis_text = "Draw!"             
            else :
                self.current_state_index += 1  
            config.move_sound.play()


    def handle_promotion_click(self, x, y):
        dialog_width, dialog_height = 340, 100
        dialog_x = (config.board_size - dialog_width) // 2
        dialog_y = (config.screen_height - dialog_height) // 2
        piece_size = dialog_height

        if dialog_x <= x <= dialog_x + dialog_width and dialog_y <= y <= dialog_y + dialog_height:
            relative_x = x - dialog_x
            if 0 <= relative_x < piece_size:
                return chess.ROOK
            elif piece_size <= relative_x < 2 * piece_size:
                return chess.KNIGHT
            elif 2 * piece_size <= relative_x < 3 * piece_size:
                return chess.BISHOP
            elif 3 * piece_size <= relative_x < 4 * piece_size:
                return chess.QUEEN

        return None  
    
    def get_analysis(self) :
        self.engine.configure({"Skill": 25})
        self.board_analysis = self.engine.analyse(self.board, chess.engine.Limit(time=0.1))
        self.engine.configure({"Skill": self.ai_difficulty})
        
        
        