import chess.engine
import math
import random

KOMODO_PATH = r"komodo-14\komodo-14_224afb\Windows\komodo-14.1-64bit.exe"


# 현재 보드 상태를 기반으로 승리 확률 계산
def calculate_win_probability(func):
    func.engine.configure({"Skill": 25})
    result = func.board_analysis
    func.engine.configure({"Skill": func.ai_difficulty})

    score_info = result["score"]

    if score_info.is_mate():
        # 체크메이트 상황 처리
        if score_info.white().mate() > 0:
            # 현재 턴의 플레이어가 이길 경우
            return 100, 0
        else:
            # 현재 턴의 플레이어가 질 경우
            return 0, 100
    
    score = result["score"].white().score()
    
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
            return "Black Checkmate"
        else:
            return "White Chckmate"
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
    if func.board.is_checkmate() :
        if func.board.turn:
            return "Checkmate. \nTry again..."
        else:
            return "Checkmate! \nYou win!!"
    elif func.board.is_stalemate():
        return "Stalemate, Draw!"
    elif func.board.is_insufficient_material():
        return "Draw!"
    elif func.board.is_seventyfive_moves():
        return "Draw!"
    elif func.board.is_fivefold_repetition():
        return "Draw!"
    elif func.board.can_claim_draw():
        return "Draw!"
    
    func.engine.configure({"Skill": 25})
    score_after_move = func.board_analysis['score']
    player_score = score_after_move.white().score(mate_score=100000)
    
    if score_after_move and score_after_move.is_mate():
        mate_in = score_after_move.white().mate()
        if mate_in > 0:
            func.engine.configure({"Skill": func.ai_difficulty})
            return f"Almost done! \nYou can checkmate \nin {mate_in} move(s)!"
        else:
            func.engine.configure({"Skill": func.ai_difficulty})
            return f"Be cautious! \nYour opponent can checkmate \nin {-mate_in} move(s)!"

 
    ai_moves = []
    for i in range(3) :
        ai_moves.append(func.engine.play(prev_board, chess.engine.Limit(time=0.1)).move)


    # 플레이어 수와 AI 수 비교
    if move in ai_moves:
        func.engine.configure({"Skill": func.ai_difficulty})
        return "Excellent choice! \nYour move aligns \nwith my move!"
    
    else:
        # AI의 최적 수로 업데이트한 보드의 점수 계산
        board_copy_after_ai_move = prev_board.copy()
        board_copy_after_ai_move.push(ai_moves[0])
        ai_score = func.engine.analyse(board_copy_after_ai_move, chess.engine.Limit(time=0.1))['score'].white().score(mate_score=100000)
        func.engine.configure({"Skill": func.ai_difficulty})

        if ai_score is not None and  player_score is not None :
            score_diff = ai_score - player_score
            return generate_feedback(score_diff)
        else :
            return "Hmm.. That's wierd."
    
    
def generate_feedback(score_difference):
    if score_difference >= 150:
        return "Outstanding move! \nYou've mastered this situation."
    elif 100 <= score_difference < 150:
        return "Excellent move. \nSignificantly better than the AI's suggestion."
    elif 50 <= score_difference < 100:
        return "Very good move. \nYou have a clear advantage."
    elif 20 <= score_difference < 50:
        return "Good move. \nYou're slightly ahead."
    elif -20 <= score_difference < 20:
        return "Average move. \nConsider exploring other options."
    elif -50 <= score_difference < -20:
        return "Suboptimal move. \nThis could weaken your position."
    elif -100 <= score_difference < -50:
        return "Poor move. \nYou're likely at a disadvantage."
    elif score_difference < -100:
        return "Bad move. \nYou're jeopardizing your position."
    else:
        return "Not a good move. \nConsider rethinking your strategy."
