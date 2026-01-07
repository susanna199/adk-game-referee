from google.adk.tools import ToolContext
import random
from google.adk.tools import ToolContext
import random

def validate_moves(user_move: str, bot_move: str, tool_context: ToolContext) -> dict:
    """
    Validates the moves and calculates round scores.
    """
    
    valid_moves = ['rock', 'paper', 'scissors', 'bomb']
    
    # Get current state
    current_user_score = tool_context.session.state.get("user_score", 0)
    current_bot_score = tool_context.session.state.get("bot_score", 0)
    user_bomb_used = tool_context.session.state.get("user_bomb_usage", False)
    bot_bomb_used = tool_context.session.state.get("bot_bomb_usage", False)
    
    # Check if user used bomb when already used
    if user_move == 'bomb' and user_bomb_used:
        return {
            "status": "invalid",
            "message": "You already used your bomb!",
            "user_round_score": 0,
            "bot_round_score": 0,
            "round_wasted": True,
            "new_user_score": current_user_score,
            "new_bot_score": current_bot_score,
            "user_bomb_usage": user_bomb_used,
            "bot_bomb_usage": bot_bomb_used
        }
    
    # Check if user move is valid
    if user_move not in valid_moves:
        return {
            "status": "invalid",
            "message": "Invalid move! Round wasted.",
            "user_round_score": 0,
            "bot_round_score": 0,
            "round_wasted": True,
            "new_user_score": current_user_score,
            "new_bot_score": current_bot_score,
            "user_bomb_usage": user_bomb_used,
            "bot_bomb_usage": bot_bomb_used
        }
    
    # Update bomb usage flags
    if user_move == 'bomb':
        user_bomb_used = True
    if bot_move == 'bomb':
        bot_bomb_used = True
    
    # Calculate scores based on YOUR ORIGINAL CONDITIONALS
    user_round_score = 0
    bot_round_score = 0
    
    if user_move == 'rock':
        if bot_move == 'rock':
            user_round_score, bot_round_score = 0, 0
        elif bot_move == 'paper':
            user_round_score, bot_round_score = 0, 1
        elif bot_move == 'scissors':
            user_round_score, bot_round_score = 1, 0
        elif bot_move == 'bomb':
            user_round_score, bot_round_score = 0, 1
    elif user_move == 'paper':
        if bot_move == 'rock':
            user_round_score, bot_round_score = 1, 0
        elif bot_move == 'paper':
            user_round_score, bot_round_score = 0, 0
        elif bot_move == 'scissors':
            user_round_score, bot_round_score = 0, 1
        elif bot_move == 'bomb':
            user_round_score, bot_round_score = 0, 1
    elif user_move == 'scissors':
        if bot_move == 'rock':
            user_round_score, bot_round_score = 0, 1
        elif bot_move == 'paper':
            user_round_score, bot_round_score = 1, 0
        elif bot_move == 'scissors':
            user_round_score, bot_round_score = 0, 0
        elif bot_move == 'bomb':
            user_round_score, bot_round_score = 0, 1
    elif user_move == 'bomb':
        if bot_move == 'rock':
            user_round_score, bot_round_score = 1, 0
        elif bot_move == 'paper':
            user_round_score, bot_round_score = 1, 0
        elif bot_move == 'scissors':
            user_round_score, bot_round_score = 1, 0
        elif bot_move == 'bomb':
            user_round_score, bot_round_score = 0, 0
    
    # Calculate new total scores
    new_user_score = current_user_score + user_round_score
    new_bot_score = current_bot_score + bot_round_score
    
    # UPDATE SESSION STATE DIRECTLY
    tool_context.session.state["user_score"] = new_user_score
    tool_context.session.state["bot_score"] = new_bot_score
    tool_context.session.state["user_bomb_usage"] = user_bomb_used
    tool_context.session.state["bot_bomb_usage"] = bot_bomb_used
    
    return {
        "status": "valid",
        "message": "Moves validated successfully",
        "user_round_score": user_round_score,
        "bot_round_score": bot_round_score,
        "round_wasted": False,
        "new_user_score": new_user_score,
        "new_bot_score": new_bot_score,
        "user_bomb_usage": user_bomb_used,
        "bot_bomb_usage": bot_bomb_used
    }


def resolve_round(user_total_score: int, bot_total_score: int, tool_context: ToolContext) -> dict:
    """
    Determines the winner of a round based on cumulative scores.
    """
    if user_total_score > bot_total_score:
        result = "User wins the round!"
        winner = "user"
    elif bot_total_score > user_total_score:
        result = "Bot wins the round!"
        winner = "bot"
    else:
        result = "Round is a draw!"
        winner = "draw"
    
    return {
        "status": "success",
        "result": result,
        "winner": winner,
        "user_total_score": user_total_score,
        "bot_total_score": bot_total_score
    }
