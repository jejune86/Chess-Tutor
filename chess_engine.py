import chess.engine
import math

KOMODO_PATH = r"komodo-14\komodo-14_224afb\Windows\komodo-14.1-64bit.exe"



def calculate_win_probability(func):
    func.engine.configure({"Skill": 25})
    result = func.board_analysis
    func.engine.configure({"Skill": func.ai_difficulty})

    score_info = result["score"]

    if score_info.is_mate():
        if score_info.white().mate() > 0:
            return 100, 0
        else:
            return 0, 100
    
    score = result["score"].white().score()
    
    if score is not None:
        probability = 1 / (1 + math.exp(-0.004 * score))
        white_win_probability = probability * 100
        black_win_probability = (1 - probability) * 100
        return white_win_probability,black_win_probability
        
    return 50,50


def set_engine_difficulty(engine, level):
    try:
        engine.configure({"Skill": level})
    except chess.engine.EngineTerminatedError :
        engine = chess.engine.SimpleEngine.popen_uci(KOMODO_PATH)
        engine.configure({"Skill": level})
    return engine


def get_best_move(func):
    func.engine.configure({"Skill": 25})
    result = func.engine.play(func.board, chess.engine.Limit(time=0.1))
    best_move = result.move
    func.engine.configure({"Skill": func.ai_difficulty})
    return best_move


def get_game_state(func):
    if func.board.is_checkmate():
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
    white_win_probability, black_win_probability = calculate_win_probability(func)
    return f"White: {white_win_probability:.2f}% - Black: {black_win_probability:.2f}%"


def move_analysis(func, prev_board, move):
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

 
  

    ai_move = func.engine.play(prev_board, chess.engine.Limit(time=0.1)).move


    if move  == ai_move:
        func.engine.configure({"Skill": func.ai_difficulty})
        return "Excellent choice! \nYour move aligns \nwith my move!"
    
    else:
        board_copy_after_ai_move = prev_board.copy()
        board_copy_after_ai_move.push(ai_move)
        try:
            ai_score = func.engine.analyse(board_copy_after_ai_move, chess.engine.Limit(time=0.1))['score'].white().score(mate_score=100000)
        except KeyError:
            # 'score' 키가 없을 때 처리할 로직
            return "Unable to calculate score."

        if ai_score is not None and  player_score is not None :
            score_diff = player_score - ai_score
            return generate_feedback(score_diff)
        else :
            return "Hmm.. That's wierd."
    
    
def generate_feedback(score_difference):
    if score_difference >= 150:
        return "Outstanding move! \nYou've mastered this situation."
    elif 100 <= score_difference < 150:
        return "Excellent move. \nSignificantly better than \nthe AI's suggestion."
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
