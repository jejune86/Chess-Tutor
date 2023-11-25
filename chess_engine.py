import chess.engine
import math

STOCKFISH_PATH = "stockfish/stockfish-windows-x86-64-avx2.exe"

# 현재 보드 상태를 기반으로 승리 확률 계산
def calculate_win_probability(func):
    func.engine.configure({"Skill Level": 20})
    result = func.engine.analyse(func.board, chess.engine.Limit(time=0.3))
    func.engine.configure({"Skill Level": func.ai_difficulty})
    if "score" in result:
        score = result["score"].relative.score()
        if score is not None:
            # 로지스틱 함수를 사용하여 확률 계산
            probability = 1 / (1 + math.exp(-0.004 * score))
            white_win_probability = probability * 100
            black_win_probability = (1 - probability) * 100
            return white_win_probability,black_win_probability
    return 50,50

# 난이도 조절 버튼을 눌렀을 때 호출될 함수를 정의합니다.
def set_engine_difficulty(engine, level):
    try:
        engine.configure({"Skill Level": level})
    except chess.engine.EngineTerminatedError :
        # 엔진이 종료된 경우, 다시 시작합니다.
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        engine.configure({"Skill Level": level})
    return engine

def get_best_move(func):
    # 최적의 수 계산을 위해 임시로 엔진의 난이도를 최대로 설정합니다.
    func.engine.configure({"Skill Level": 20})
    result = func.engine.play(func.board, chess.engine.Limit(time=0.3))
    best_move = result.move
    # 계산이 끝난 후 원래 난이도로 되돌립니다.
    func.engine.configure({"Skill Level": func.ai_difficulty})
    return best_move

def get_game_state(func):
    if func.board.is_checkmate():
        # 체크메이트인 경우, 현재 턴의 반대 색깔이 이긴 것입니다.
        if func.board.turn:
            return "Black checkmate"
        else:
            return "White checkmate"
    elif func.board.is_stalemate():
        return "Stalemate"
    elif func.board.is_insufficient_material():
        return "Draw due to insufficient material"
    elif func.board.is_seventyfive_moves():
        return "Draw due to 75-move rule"
    elif func.board.is_fivefold_repetition():
        return "Draw due to five-fold repetition"
    elif func.board.can_claim_draw():
        return "Draw claimable"
    # 이외의 게임 진행 중인 상태에서는 승리 확률을 계산합니다.
    white_win_probability, black_win_probability = calculate_win_probability(func)
    return f"White: {white_win_probability:.2f}% - Black: {black_win_probability:.2f}%"

def move_analysis(func) :
    if func.current_state_index > 0 :
        set_engine_difficulty(func.engine,20)
        info_before = func.engine.analyse(func.previous_board_states[func.current_state_index-1], chess.engine.Limit(time=0.1))
        info_after = func.engine.analyse(func.previous_board_states[func.current_state_index], chess.engine.Limit(time=0.1))
        set_engine_difficulty(func.engine,func.ai_difficulty)
        # 평가 점수를 추출합니다.
        score_before = info_before["score"].white().score()
        score_after = info_after["score"].white().score()

        # 점수 차이를 계산합니다.
        score_difference = score_after - score_before

        # 점수 차이를 기반으로 수의 품질을 평가합니다.
        if score_difference is None:
            quality = "Game Start"
        elif score_difference >= 20:
            quality = "good move"
        elif -20 <= score_difference < 20:
            quality = "acceptable move"
        else:
            quality = "poor move"
            
        return quality
    else : return "Game Start"