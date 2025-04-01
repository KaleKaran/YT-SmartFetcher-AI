import google.generativeai as genai
from app.config.config import PROMPT

def generate_summary(transcript, custom_prompt=""):
    """
    Generate a summary from transcript using Google Generative AI.
    
    Args:
        transcript (str): Transcript text to summarize
        custom_prompt (str, optional): Custom prompt to use. Defaults to "".
        
    Returns:
        str: Generated summary or error message
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt_to_use = (custom_prompt + transcript) if custom_prompt else (PROMPT + transcript)
        response = model.generate_content(prompt_to_use)

        if hasattr(response, "text"):
            return response.text
        else:
            return "Error: Unexpected response format from API."
    except Exception as e:
        return f"Error generating summary: {str(e)}" 