import pygame
import chess
import config
import chess_func
from chess_engine import  KOMODO_PATH
from chess_ui import draw_all

with chess.engine.SimpleEngine.popen_uci(KOMODO_PATH) as engine:
    func = chess_func.ChessGame(chess.Board(),engine)    
    while func.chess_running:
        for event in pygame.event.get():
           func.event_handle(event) 
        draw_all(config.screen, config.font, func)
        func.ai_movement()
               
pygame.quit()
