import config
import chess
import pygame

def draw_all(screen, font, func) :
    draw_board(screen, func)
    write_texts(screen, font, func)
    draw_captured_pieces(screen, func.captured_pieces, config.top_bottom_space, config.square_size)
    draw_proffessor(screen)
    write_analysis(screen, font, func)
    pygame.display.flip()


def scale_piece_image(image, target_height):
    image_height = image.get_height()
    image_width = image.get_width()
    scale_factor = target_height / float(image_height)
    new_width = int(scale_factor * image_width)
    new_image = pygame.transform.scale(image, (new_width, target_height))
    return new_image

def draw_captured_pieces(screen, captured_pieces, top_bottom_space, square_size):
    scaled_size = square_size // 2  
    y_offset_top = (top_bottom_space - scaled_size) // 2  
    y_offset_bottom = config.screen_height - top_bottom_space + y_offset_top  
    for i, piece in enumerate(captured_pieces['black']):
        piece_image = scale_piece_image(config.piece_images[piece.symbol().upper()], scaled_size)
        screen.blit(piece_image, (i * scaled_size, y_offset_top))
        
    for i, piece in enumerate(captured_pieces['white']):
        piece_image = scale_piece_image(config.piece_images[piece.symbol().lower()], scaled_size)
        screen.blit(piece_image, (i * scaled_size, y_offset_bottom))

def draw_proffessor(screen) :
    tooltip_rect = config.tooltip_image.get_rect()
    tooltip_rect.topleft = (config.board_size + 10, 140)  
    screen.blit(config.tooltip_image, tooltip_rect)
    
    dr_rect = config.dr_image.get_rect()
    dr_rect.topleft = (config.board_size + 100, 450)  
    screen.blit(config.dr_image, dr_rect)
    
    
    
    
def write_texts(screen, font, func) :  
    difficulty_text = f"AI Difficulty: {func.ai_difficulty}"
    difficulty_surface = font.render(difficulty_text, True, (0, 0, 0))
    difficulty_surface_rect = difficulty_surface.get_rect()
    difficulty_surface_rect.topleft = (config.board_size + 10, 10) 
    screen.blit(difficulty_surface, difficulty_surface_rect)
    
    text_surface = font.render(func.win_probability_text, True, (0, 0, 0))
    text_surface_rect = text_surface.get_rect()
    text_surface_rect.topleft = (config.board_size + 10, 50)  #
    screen.blit(text_surface, text_surface_rect)
    
    
def draw_board(screen, func) :
    screen.fill((255, 255, 255))
    screen.blit(config.board_image, (0, 40))
    pygame.draw.rect(screen, (24,73,33), (0, 0, config.board_size, 40))
    pygame.draw.rect(screen, (24,73,33), (0, config.screen_height - 40, config.board_size, 40))
    
    if func.last_move :
        highlight_color = (129, 211, 235)  
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
        start_square = func.best_move.from_square
        end_square = func.best_move.to_square
        start_rect = pygame.Rect((start_square % 8) * config.square_size,
                                    (7 - start_square // 8) * config.square_size+40,
                                    config.square_size, config.square_size)
        end_rect = pygame.Rect((end_square % 8) * config.square_size,
                                (7 - end_square // 8) * config.square_size+40,
                                config.square_size, config.square_size)
        pygame.draw.rect(screen, (128, 180, 99), start_rect)  
        pygame.draw.rect(screen, (239, 64, 74), end_rect)  
    
    
    if func.selected_square is not None and func.selected_rect is not None: 
        pygame.draw.rect(screen, (255,204,78), func.selected_rect)

    for square in chess.SQUARES:
        piece = func.board.piece_at(square)
        if piece is not None:
            x = chess.square_file(square) * config.square_size
            y = (7 - chess.square_rank(square)) * config.square_size + 40
            screen.blit(config.piece_images[piece.symbol()], (x, y))
            
    if func.promotion:
        draw_promotion_dialog(screen)
    
        
        

def write_analysis(screen, font, func) :
    lines = func.move_analysis_text.split('\n')
    y = 240
    for line in lines:
        text_surface = font.render(line, True, (0, 0, 0))
        screen.blit(text_surface, (config.board_size+40, y))
        y += text_surface.get_height() + 10
        
        
def draw_promotion_dialog(screen):
    dialog_width, dialog_height = 340, 100
    dialog_x = (config.board_size - dialog_width) // 2
    dialog_y = (config.screen_height - dialog_height) // 2

    dialog_background = pygame.Surface((dialog_width, dialog_height))
    dialog_background.set_alpha(180) 
    dialog_background.fill((255, 255, 255)) 
    screen.blit(dialog_background, (dialog_x, dialog_y))

    pieces = ['R', 'N', 'B', 'Q']
    x_offset = dialog_x + 10
    y_offset = dialog_y + 10
    for i, piece in enumerate(pieces):
        screen.blit(config.piece_images[piece], (x_offset + i * 80, y_offset))
    

