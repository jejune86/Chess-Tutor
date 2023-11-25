import pygame
import chess
import config
import copy
import chess_func
from chess_engine import  STOCKFISH_PATH
from chess_ui import draw_captured_pieces, write_texts, draw_proffessor, draw_board


# Pygame 초기화
pygame.init()
font = pygame.font.SysFont("sans-serif", 30)


screen = pygame.display.set_mode((config.screen_width, config.screen_height))
pygame.display.set_caption("Chess Tutor")


with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
    func = chess_func.ChessGame(chess.Board(),engine)
    engine.configure({"Skill Level": func.ai_difficulty})
    while func.chess_running:
        for event in pygame.event.get():
            func.event_handle(event)  #키보드와 클릭 이벤트 다루기
                    
        # 화면 지우기
        draw_board(screen, func.board, func.last_move, func.best_move, func.selected_square, func.selected_rect)
        # 승리 확률 정보 표시
        write_texts(screen,font, func.win_probability_text, func.ai_difficulty)
        draw_captured_pieces(screen, func.captured_pieces, config.top_bottom_space, config.square_size)
        draw_proffessor(screen)
        pygame.display.flip()

        # AI 움직임 계산 및 수행
        func.ai_movement()
            
            

                
# Pygame 종료
pygame.quit()
