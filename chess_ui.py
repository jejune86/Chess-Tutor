import config
import chess
import pygame
from chess_engine import move_analysis
# 기물 이미지를 축소하는 함수
def scale_piece_image(image, target_height):
    # 기물 이미지의 비율을 유지하면서 높이를 target_height에 맞게 조정합니다.
    image_height = image.get_height()
    image_width = image.get_width()
    scale_factor = target_height / float(image_height)
    new_width = int(scale_factor * image_width)
    new_image = pygame.transform.scale(image, (new_width, target_height))
    return new_image

def draw_captured_pieces(screen, captured_pieces, top_bottom_space, square_size):
    # 잡은 기물의 이미지를 축소합니다.
    scaled_size = square_size // 2  # 축소된 기물의 크기를 반으로 설정합니다.
    y_offset_top = (top_bottom_space - scaled_size) // 2  # 상단 여백 중앙에 위치시킵니다.
    y_offset_bottom = config.screen_height - top_bottom_space + y_offset_top  # 하단 여백 중앙에 위치시킵니다.
    # 상단에 흰색 기물을 표시합니다.
    for i, piece in enumerate(captured_pieces['black']):
        piece_image = scale_piece_image(config.piece_images[piece.symbol().upper()], scaled_size)
        screen.blit(piece_image, (i * scaled_size, y_offset_top))

    # 하단에 검은색 기물을 표시합니다.
    for i, piece in enumerate(captured_pieces['white']):
        piece_image = scale_piece_image(config.piece_images[piece.symbol().lower()], scaled_size)
        screen.blit(piece_image, (i * scaled_size, y_offset_bottom))

def draw_proffessor(screen) :
    tooltip_rect = config.tooltip_image.get_rect()
    tooltip_rect.topleft = (config.board_size + 10, 150)  # 승리 확률 정보를 추가 공간에 표시하는 위치 설정
    screen.blit(config.tooltip_image, tooltip_rect)
    
    
def write_texts(screen, font, func) :
    text_surface = font.render(func.win_probability_text, True, (0, 0, 0))
    text_surface_rect = text_surface.get_rect()
    text_surface_rect.topleft = (config.board_size + 10, 50)  # 승리 확률 정보를 추가 공간에 표시하는 위치 설정
    screen.blit(text_surface, text_surface_rect)
    
    difficulty_text = f"AI Difficulty: {func.ai_difficulty}"
    difficulty_surface = font.render(difficulty_text, True, (0, 0, 0))
    difficulty_surface_rect = difficulty_surface.get_rect()
    difficulty_surface_rect.topleft = (config.board_size + 10, 10)  # 승리 확률 정보 위에 난이도를 표시합니다.
    screen.blit(difficulty_surface, difficulty_surface_rect)
    
    
def draw_board(screen, func) :
    screen.fill((255, 255, 255))
    # 체스 보드 그리기
    screen.blit(config.board_image, (0, 40))
    pygame.draw.rect(screen, (24,73,33), (0, 0, config.board_size, 40))
    pygame.draw.rect(screen, (24,73,33), (0, config.screen_height - 40, config.board_size, 40))
    
    # 마지막 움직임을 하늘색으로 표시합니다.
    if func.last_move :
        highlight_color = (135, 206, 250)  # 하늘색
        start_square = func.last_move.from_square
        end_square = func.last_move.to_square
        start_rect = pygame.Rect((start_square % 8) * config.square_size,
                                    (7 - start_square // 8) * config.square_size+40,
                                    config.square_size, config.square_size)
        end_rect = pygame.Rect((end_square % 8) * config.square_size, 
                                (7 - end_square // 8) * config.square_size+40,
                                config.square_size, config.square_size)
        pygame.draw.rect(screen, highlight_color, start_rect)
        pygame.draw.rect(screen, highlight_color, end_rect)
    
    if func.best_move:
        # 시작 위치와 목적지를 다른 색으로 강조합니다.
        start_square = func.best_move.from_square
        end_square = func.best_move.to_square
        start_rect = pygame.Rect((start_square % 8) * config.square_size,
                                    (7 - start_square // 8) * config.square_size+40,
                                    config.square_size, config.square_size)
        end_rect = pygame.Rect((end_square % 8) * config.square_size,
                                (7 - end_square // 8) * config.square_size+40,
                                config.square_size, config.square_size)
        pygame.draw.rect(screen, (0, 255, 0), start_rect)  # 시작 위치를 녹색으로 표시
        pygame.draw.rect(screen, (255, 0, 0), end_rect)  # 목적지를 빨간색으로 표시
    
    if func.selected_square:
        pygame.draw.rect(screen, (255,238,138), func.selected_rect)
        
    # 체스 기물 그리기
    for square in chess.SQUARES:
        piece = func.board.piece_at(square)
        if piece is not None:
            x = chess.square_file(square) * config.square_size
            y = (7 - chess.square_rank(square)) * config.square_size + 40
            screen.blit(config.piece_images[piece.symbol()], (x, y))


def write_analysis(screen, font, func) :
    text_surface = font.render(func.move_analysis_text, True, (0, 0, 0))
    text_surface_rect = text_surface.get_rect()
    text_surface_rect.topleft = (config.board_size + 15, 180)  # 승리 확률 정보를 추가 공간에 표시하는 위치 설정
    screen.blit(text_surface, text_surface_rect)