import config
import pygame

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
