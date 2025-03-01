import openai
import os
import base64
import io
import json
import logging
from dotenv import load_dotenv

# Load environment variables and set API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def analyze_command(command_text, screenshot):
    """
    Sends the command text and screenshot to the OpenAI API.
    
    Args:
        command_text (str): The transcribed command from the user.
        screenshot (PIL.Image): A Pillow Image object of the current browser view.
        
    Returns:
        dict: A dictionary containing the action details (or an 'error' key with a short message).
              Example success response:
              {
                  "action": "click",
                  "target": "login button",
                  "value": ""
              }
              Example error response:
              {
                  "error": "No matching UI element found."
              }
    """
    try:
        # Convert screenshot to base64 string
        buffer = io.BytesIO()
        screenshot.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
        
        # Build a prompt for the OpenAI API
        prompt = (
            "You are a browser automation assistant. Given the following browser screenshot (base64 encoded, truncated for brevity) "
            "and a user's command, determine the necessary action to perform on the browser. Return a JSON object with the following keys:\n"
            "  - 'action': one of 'click', 'open', 'type', 'scroll', etc.\n"
            "  - 'target': the target element, URL, or field (if applicable).\n"
            "  - 'value': any additional text required (if applicable).\n\n"
            "If the command cannot be executed, return a JSON object with an 'error' key containing a short error message (under 100 characters).\n\n"
            f"User Command: \"{command_text}\"\n"
            f"Screenshot (base64, first 500 characters): \"{img_str[:500]}...\""
        )

        # Call the OpenAI ChatCompletion API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for browser automation."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=150,
        )

        # Extract and parse the API response
        message = response["choices"][0]["message"]["content"].strip()
        try:
            result = json.loads(message)
        except json.JSONDecodeError:
            logging.error("Failed to parse JSON response from OpenAI API.")
            return {"error": "Failed to parse API response."}
        
        return result

    except Exception as e:
        logging.error(f"Error in analyze_command: {e}")
        return {"error": "API error occurred."}
