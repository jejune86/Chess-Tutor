import chess.engine
import math
import random

KOMODO_PATH = r"komodo-14\komodo-14_224afb\Windows\komodo-14.1-64bit.exe"


# 현재 보드 상태를 기반으로 승리 확률 계산
def calculate_win_probability(func):
    func.engine.configure({"Skill": 25})
    result = func.engine.analyse(func.board, chess.engine.Limit(time=0.1))
    func.engine.configure({"Skill": func.ai_difficulty})
    if "score" in result:
        score_info = result["score"]

        if score_info.is_mate():
            # 체크메이트 상황 처리
            if score_info.white().mate() > 0:
                # 현재 턴의 플레이어가 이길 경우
                return 100, 0
            else:
                # 현재 턴의 플레이어가 질 경우
                return 0, 100
        
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
        engine.configure({"Skill": level})
    except chess.engine.EngineTerminatedError :
        # 엔진이 종료된 경우, 다시 시작합니다.
        engine = chess.engine.SimpleEngine.popen_uci(KOMODO_PATH)
        engine.configure({"Skill": level})
    return engine

def get_best_move(func):
    # 최적의 수 계산을 위해 임시로 엔진의 난이도를 최대로 설정합니다.
    func.engine.configure({"Skill": 25})
    result = func.engine.play(func.board, chess.engine.Limit(time=0.1))
    best_move = result.move
    # 계산이 끝난 후 원래 난이도로 되돌립니다.
    func.engine.configure({"Skill": func.ai_difficulty})
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


def move_analysis(func, prev_board, move):
    # 엔진에 최상의 분석을 요청
    func.engine.configure({"Skill": 25})
    ai_moves = []
    for i in range(3) :
        ai_moves.append(func.engine.play(prev_board, chess.engine.Limit(time=0.1)).move)

    # 플레이어 수와 AI 수 비교
    if move in ai_moves:
        return "Excellent choice! \nYour move aligns \nwith my move!"
    
    else:
        # AI의 최적 수로 업데이트한 보드의 점수 계산
        board_copy_after_ai_move = prev_board.copy()
        board_copy_after_ai_move.push(ai_moves[0])
        info_after_ai_move = func.engine.analyse(board_copy_after_ai_move, chess.engine.Limit(time=0.1))

        # 플레이어의 수로 업데이트한 보드의 점수 계산
        board_copy_after_move = prev_board.copy()
        board_copy_after_move.push(move)
        info_after_move = func.engine.analyse(board_copy_after_move, chess.engine.Limit(time=0.1))

        func.engine.configure({"Skill": func.ai_difficulty})
        
        if info_after_move['score'].white().mate() :
            mate_in = info_after_move['score'].white().mate()
            if mate_in > 0:
                return f"Brilliant move! \nYou can checkmate \nin {mate_in} move(s)!"
            else:
                return "Be cautious! \nYour opponent can checkmate \nin {mate_in} move(s)!"

        # 일반 점수 비교 및 피드백 생성
        score_diff = info_after_move['score'].relative.score(mate_score=100000) - info_after_ai_move['score'].relative.score(mate_score=100000)
        return generate_feedback(score_diff)
    
    
def generate_feedback(score_difference):
    if score_difference >= 100:
        return "Brilliant move! \nYou're dominating the game."
    elif 50 <= score_difference < 100:
        return "Very good move. \nYou're gaining an advantage."
    elif 10 <= score_difference < 50:
        return "Good move. \nYou're making progress."
    elif -10 <= score_difference < 10:
        return "Fair move. \nThere could be other \ninteresting options"
    elif -50 <= score_difference < -10:
        return "Risky move. \nConsider your \nopponent's opportunities."
    elif score_difference < -50:
        return "Problematic move. \nThis might put you \nin a tough spot."
    else:
        return "Not a good move. \nYou're likely falling behind."
