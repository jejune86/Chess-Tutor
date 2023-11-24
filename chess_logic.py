# chess_logic.py
from chess_engine import calculate_win_probability

def get_game_state(board,engine,ai_difficulty):
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
    return calculate_win_probability(board,engine,ai_difficulty)

# 여기에 필요한 다른 체스 게임 로직 관련 함수들 추가...
