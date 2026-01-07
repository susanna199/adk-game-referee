import random
from google.adk.sessions import InMemorySessionService
import uuid
import re

# Import agent and tools
from my_agent.agent import my_agent
from utils import validate_moves, resolve_round

# Register tools with agent
my_agent.tools = [validate_moves, resolve_round]

# Configuration
APP_NAME = "rock_paper_scissors_game"
USER_ID = "player_1"
SESSION_ID = str(uuid.uuid4())

initial_state = {
    "user_score": 0,
    "bot_score": 0,
    "user_bomb_usage": False,
    "bot_bomb_usage": False
}


# ===== AGENT BOUNDARY: Input Interpretation =====
class InputInterpreter:
    """Responsible for understanding user intent"""
    
    @staticmethod
    def parse_user_move(user_input: str) -> str:
        """Parse and normalize user input"""
        user_input = user_input.strip().lower()
        
        # Handle abbreviations
        if user_input == 'r':
            return 'rock'
        elif user_input == 'p':
            return 'paper'
        elif user_input == 's':
            return 'scissors'
        elif user_input == 'b':
            return 'bomb'
        
        # Check for valid moves in input
        pattern = r'\b(rock|paper|scissors|bomb)\b'
        match = re.search(pattern, user_input)
        
        if match:
            return match.group(1)
        else:
            return 'invalid'


# ===== AGENT BOUNDARY: Bot Decision Making =====
class BotPlayer:
    """Responsible for bot's move decisions"""
    
    @staticmethod
    def decide_move(bot_bomb_used: bool) -> str:
        """Generate bot's move based on game state"""
        if bot_bomb_used:
            return random.choice(['rock', 'paper', 'scissors'])
        return random.choice(['rock', 'paper', 'scissors', 'bomb'])


# ===== AGENT BOUNDARY: Response Generator =====
class ResponseGenerator:
    """Responsible for generating user-facing messages"""
    
    @staticmethod
    def explain_outcome(user_move: str, bot_move: str, user_round_score: int, 
                       bot_round_score: int, round_wasted: bool) -> str:
        """Generate explanation of round outcome"""
        if round_wasted:
            return "Invalid move! This round is wasted."
        
        # Draw
        if user_round_score == 0 and bot_round_score == 0:
            if user_move == 'bomb' and bot_move == 'bomb':
                return "Both bombs collide! It's a draw!"
            else:
                return f"Both played {user_move}. It's a draw!"
        
        # User wins
        if user_round_score == 1:
            if user_move == 'bomb':
                return f"Your bomb destroys {bot_move}! You win this round!"
            elif user_move == 'rock' and bot_move == 'scissors':
                return "Rock crushes scissors! You win this round!"
            elif user_move == 'paper' and bot_move == 'rock':
                return "Paper covers rock! You win this round!"
            elif user_move == 'scissors' and bot_move == 'paper':
                return "Scissors cut paper! You win this round!"
        
        # Bot wins
        if bot_round_score == 1:
            if bot_move == 'bomb':
                return f"Bot's bomb destroys your {user_move}! Bot wins this round!"
            elif bot_move == 'rock' and user_move == 'scissors':
                return "Rock crushes scissors! Bot wins this round!"
            elif bot_move == 'paper' and user_move == 'rock':
                return "Paper covers rock! Bot wins this round!"
            elif bot_move == 'scissors' and user_move == 'paper':
                return "Scissors cut paper! Bot wins this round!"
        
        return "Round complete!"


# ===== AGENT BOUNDARY: Game Referee =====
class GameRefereeAgent:
    """
    Main agent responsible for:
    - Orchestrating game flow
    - Enforcing rules via tools
    - Managing state
    - Coordinating other components
    """
    
    def __init__(self, session_service, session_id, app_name, user_id):
        self.session_service = session_service
        self.session_id = session_id
        self.app_name = app_name
        self.user_id = user_id
        self.game_session = None
        
        # Components
        self.input_interpreter = InputInterpreter()
        self.bot_player = BotPlayer()
        self.response_generator = ResponseGenerator()
    
    async def initialize_game(self):
        """Initialize game session"""
        self.game_session = await self.session_service.create_session(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=self.session_id,
            state=initial_state
        )
        self._display_welcome()
    
    def _display_welcome(self):
        """Display game rules"""
        print("\n" + "="*50)
        print("     WELCOME TO ROCK PAPER SCISSORS BOMB")
        print("="*50)
        print("\nRULES:")
        print("1. Best of 3 rounds - highest score wins")
        print("2. rock beats scissors | scissors beats paper | paper beats rock")
        print("3. bomb beats everything (use once per game)")
        print("4. Invalid input wastes the round")
        print("5. Game ends automatically after 3 rounds")
    
    async def play_game(self):
        """Main game loop - agent orchestration"""
        rounds_played = 0
        max_rounds = 3
        
        while rounds_played < max_rounds:
            await self._play_round(rounds_played + 1)
            rounds_played += 1
        
        self._display_final_result()
    
    async def _play_round(self, round_number: int):
        """Execute a single round"""
        print("\n" + "="*50)
        print(f"           ROUND {round_number} of 3")
        print("="*50)
        
        # Show status
        self._display_status()
        
        # Get moves (using bounded components)
        print("\nEnter your move (rock/paper/scissors/bomb or r/p/s/b):")
        user_input = input("Your move: ")
        user_move = self.input_interpreter.parse_user_move(user_input)
        
        bot_bomb_used = self.game_session.state.get("bot_bomb_usage", False)
        bot_move = self.bot_player.decide_move(bot_bomb_used)
        
        print(f"\nYou played: {user_move}")
        print(f"Bot played: {bot_move}")
        
        # Validate using tool (agent uses tools for game logic)
        validation_result = self._validate_and_update(user_move, bot_move)
        
        # Generate response (using bounded component)
        outcome = self.response_generator.explain_outcome(
            user_move, bot_move,
            validation_result.get("user_round_score", 0),
            validation_result.get("bot_round_score", 0),
            validation_result.get("round_wasted", False)
        )
        print(f"\n{outcome}")
        
        # Show updated scores
        user_score = self.game_session.state.get("user_score", 0)
        bot_score = self.game_session.state.get("bot_score", 0)
        print(f"\nScore after Round {round_number}: You {user_score} - {bot_score} Bot")
    
    def _validate_and_update(self, user_move: str, bot_move: str) -> dict:
        """Agent uses tool to validate and update state"""
        # Mock tool context
        class ToolContext:
            def __init__(self, session):
                self.session = session
        
        tool_context = ToolContext(self.game_session)
        return validate_moves(user_move, bot_move, tool_context)
    
    def _display_status(self):
        """Display current game status"""
        user_bomb_status = "available" if not self.game_session.state.get("user_bomb_usage", False) else "used"
        bot_bomb_status = "available" if not self.game_session.state.get("bot_bomb_usage", False) else "used"
        
        print(f"\nCurrent Score: You {self.game_session.state.get('user_score', 0)} - {self.game_session.state.get('bot_score', 0)} Bot")
        print(f"Your bomb: {user_bomb_status} | Bot's bomb: {bot_bomb_status}")
    
    def _display_final_result(self):
        """Display final game result"""
        final_user_score = self.game_session.state.get("user_score", 0)
        final_bot_score = self.game_session.state.get("bot_score", 0)
        
        print("\n" + "="*50)
        print("           GAME OVER")
        print("="*50)
        print(f"\nFinal Score: You {final_user_score} - {final_bot_score} Bot\n")
        
        if final_user_score > final_bot_score:
            print("Congratulations! YOU WIN THE GAME!")
        elif final_bot_score > final_user_score:
            print("Bot wins this time! Better luck next game!")
        else:
            print("It's a DRAW! Well played!")
        
        print("\n" + "="*50 + "\n")


async def main():
    # Initialize session service
    session_service = InMemorySessionService()
    
    # Create and run game referee agent
    referee = GameRefereeAgent(
        session_service=session_service,
        session_id=SESSION_ID,
        app_name=APP_NAME,
        user_id=USER_ID
    )
    
    await referee.initialize_game()
    await referee.play_game()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
