import chess.engine
import math

STOCKFISH_PATH = "stockfish/stockfish-windows-x86-64-avx2.exe"

# 현재 보드 상태를 기반으로 승리 확률 계산
def calculate_win_probability(board, engine, ai_difficulty):
    engine.configure({"Skill Level": 20})
    result = engine.analyse(board, chess.engine.Limit(time=0.3))
    engine.configure({"Skill Level": ai_difficulty})
    if "score" in result:
        score = result["score"].relative.score()
        if score is not None:
            # 로지스틱 함수를 사용하여 확률 계산
            probability = 1 / (1 + math.exp(-0.004 * score))
            white_win_probability = probability * 100
            black_win_probability = (1 - probability) * 100
            return f"White: {white_win_probability:.2f}% - Black: {black_win_probability:.2f}%"
    return "Game in progress"

# 난이도 조절 버튼을 눌렀을 때 호출될 함수를 정의합니다.
def set_engine_difficulty(engine, level):
    try:
        engine.configure({"Skill Level": level})
    except chess.engine.EngineTerminatedError :
        # 엔진이 종료된 경우, 다시 시작합니다.
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        engine.configure({"Skill Level": level})
    return engine

def get_best_move(engine, board, ai_difficulty):
    # 최적의 수 계산을 위해 임시로 엔진의 난이도를 최대로 설정합니다.
    engine.configure({"Skill Level": 20})
    result = engine.play(board, chess.engine.Limit(time=0.3))
    best_move = result.move
    # 계산이 끝난 후 원래 난이도로 되돌립니다.
    engine.configure({"Skill Level": ai_difficulty})
    return best_move
