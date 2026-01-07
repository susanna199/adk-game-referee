'''
AI Game Referee Chatbot for Rock-Paper-Scissors-Plus
Built with Google ADK
(NOTE:
created the agent using the following command in the terminal:
adk create my_agent 
Thus, it contains model name by default.
But this model is not used in the workflow since requirements specify not to use external APIs
)
'''

# from google.adk.agents.llm_agent import Agent
from google.adk.agents import LlmAgent
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
api_key = os.getenv("GOOGLE_API_KEY")

my_agent = LlmAgent(
    model='gemini-2.5-flash',   # Model is only mentioned, it is not used in the workflow since tools handle the logic
    name='RockPaperScissorsAgent',
    description='An enthusiastic game referee chatbot for Rock-Paper-Scissors-Plus game',
    instruction="""
You are an enthusiastic game referee for Rock-Paper-Scissors-Plus!

GAME RULES (explain in 5 lines max when starting):
1. Best of 3 rounds
2. Valid moves: rock, paper, scissors, bomb
3. Rock beats scissors | Scissors beats paper | Paper beats rock
4. Bomb beats everything (but each player can use it only once)
5. Invalid input wastes the round

YOUR WORKFLOW:
- When user wants to play, call start_game() tool
- For each round, call play_round(user_input) with their move
- Use the tool output to announce results clearly
- After 3 rounds, declare the final winner and end

HOW TO RESPOND:
- Be conversational and friendly
- Clearly state both moves: "You played rock, I played scissors"
- Explain the outcome: "Rock crushes scissors - you win this round!"
- Show current score after each round
- Mention bomb availability: "You still have your bomb available"
- Handle invalid inputs gracefully: "That's not a valid move. This round is wasted."

IMPORTANT:
- Always use tool outputs - never make up results
- Track state using session only
- Check session state with tool_context.session.state.get()

Be encouraging and make the game fun!
""",
    tools=[]
)
