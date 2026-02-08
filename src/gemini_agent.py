import os
import PIL.Image
from google import genai
from google.genai import types
from dotenv import load_dotenv
from src.dota_client import get_team_recent_matches

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

try:
    with open("data/patch_7_40c.txt", "r", encoding="utf-8") as f:
        PATCH_CONTEXT = f.read()
except FileNotFoundError:
    PATCH_CONTEXT = "No patch notes found."

# --- STEP 1: VISION ---
def identify_heroes_from_image(image_file):
    img = PIL.Image.open(image_file)
    prompt = "List the Dota 2 heroes for Radiant and Dire. Format: 'Radiant: [Hero1, Hero2...], Dire: [Hero1...]'."
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=[prompt, img]
        )
        return response.text
    except Exception as e:
        return f"Vision Error: {e}"

# --- STEP 2: REASONING ---
def analyze_data_and_predict(team1, team2, heroes_text):
    
   
    SYSTEM_INSTRUCTION = f"""
    You are a Dota 2 Analyst 
    
    CONTEXT:
    - Patch Notes: {PATCH_CONTEXT}
    - Draft: {heroes_text}
    
    TASK:
    1. Call `get_team_recent_matches` for {team1} and {team2}.
    2. **Look at the 'stats' field in the JSON** (Winrate & Duration are already calculated there).
    3. Compare these stats with the Heroes Drafted.
       - Example: If 'avg_duration' is 30 mins (Fast) but they picked Spectre (Slow hero), mark as HIGH RISK.
    4. Predict the Winner.
    """
    
    
    tools = [get_team_recent_matches]
    
    try:
        response = client.models.generate_content(
            model='gemini-3-pro-preview', 
            contents=f"Analyze {team1} vs {team2}. Use the tools to get stats.",
            config=types.GenerateContentConfig(
                tools=tools,
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.4,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False)
            )
        )
        return response.text
    except Exception as e:
        return f"Analysis Error: {e}"

# --- MAIN ---
def analyze_matchup_with_image(team1, team2, image_file=None):
    draft_info = "No image provided."
    if image_file:
        draft_info = identify_heroes_from_image(image_file)
        
    return analyze_data_and_predict(team1, team2, draft_info)