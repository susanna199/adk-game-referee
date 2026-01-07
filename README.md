# Rock Paper Scissors Bomb – AI Game Referee

This repo has the codes to run an AI game referee for Rock–Paper–Scissors–Plus (with bomb move) built using **Python** and **Google Agent Development Kit (ADK)**. The referee enforces rules, validates moves, tracks state across rounds, and runs a best-of-3 game between a human player and a bot via CLI.

## Project Overview

This project demonstrates:
-  Game logic with bomb mechanic (beats all moves, usable once per player)
-  State management using ADK session variables
-  Tool-based validation and state alteration
-  Clear separation of concerns (intent understanding, game logic, response generation)
-  No external API calls (deterministic execution)

## State Model
Game state is managed using Google ADK's InMemorySessionService, which provides persistent storage across all game rounds. The state is structured as a Python dictionary with the following schema:
```python
{
    "user_score": int,        # Cumulative score across 3 rounds
    "bot_score": int,         # Cumulative score across 3 rounds  
    "user_bomb_usage": bool,  # Tracks if user has used their bomb
    "bot_bomb_usage": bool    # Tracks if bot has used its bomb
}
```

## State Properties and Design Decisions:

1. Cumulative Scoring and Boolean Bomb Flags: A single session is created at the start of the game and session variables (user_score, bot_score) are reused throughout all rounds. This is done to ensure scores and bomb_usage (using user_bomb_usage, bot_bomb_usage) is correctly accounted for.
3. State Stored in Session: Game state variables are stored in the ADK session object, not embedded in conversational text.
4. Tool-Driven Mutations: State changes happen through the tool defined in utils.py file (validate_moves)

### ADK Primitives Used:

1. InMemorySessionService – Manages game state persistence across rounds
2. ToolContext – Enables tools to access and mutate session state

### Tool Definitions (utils.py):
1. validate_moves: This tool checks move legality and prevents reusing bomb, implementing all basic game rules (like Rock beats scissors and not paper, bomb beats all etc)
2. resolve_round: Determines the final game outcome

## Scope for Improvement:
- Input Validation: Strengthen handling input, moving beyond regex to handle cases like 'pa per' (which has a space in between) 
- Structured Input/Output with Pydantic: Returning tool outputs in dictionary format ensure structured information when passed to Agent.
- Persistent Storage: Include DatabaseSessionService that will ensure session recovery that saves state to the database (for potential alteration)

