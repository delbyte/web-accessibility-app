from openai import OpenAI
import os
import json
import logging
import pytesseract
import cv2
import numpy as np
from dotenv import load_dotenv

# Set the tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load environment variables and set API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key="your_api_key_here")

def extract_ui_elements(screenshot):
    """
    Uses pytesseract to extract UI elements (text and positions) from the screenshot.
    Returns a list of dictionaries with keys: 'text', 'left', 'top', 'width', 'height'.
    """
    # Convert Pillow image to a numpy array
    image_np = np.array(screenshot)
    # Convert to grayscale for better OCR results
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    # Run pytesseract to get OCR data with bounding boxes
    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)
    
    elements = []
    n_boxes = len(data['level'])
    for i in range(n_boxes):
        text = data['text'][i].strip()
        if text:  # Only include non-empty texts
            left = data['left'][i]
            top = data['top'][i]
            width = data['width'][i]
            height = data['height'][i]
            elements.append({
                "text": text,
                "left": left,
                "top": top,
                "width": width,
                "height": height
            })
    return elements

def analyze_command(command_text, screenshot):
    """
    Processes the command by extracting UI elements via OCR from the screenshot,
    then sending this information along with the command to OpenAI for processing.
    
    Args:
        command_text (str): The user's spoken command.
        screenshot (PIL.Image): A Pillow Image object of the current browser view.
        
    Returns:
        dict: A structured response from the API with keys such as 'action', 'target', 'value', and 'position'.
              Example success:
              {
                  "action": "click",
                  "target": "login button",
                  "value": "",
                  "position": {"x": 500, "y": 400}
              }
              Example error:
              {
                  "error": "No matching UI element found."
              }
    """
    try:
        # Extract UI elements from the screenshot
        ui_elements = extract_ui_elements(screenshot)
        
        # Build a string summary of UI elements (limit to first 20 to avoid token bloat)
        ui_elements_str = "\n".join(
            [f"{el['text']} at ({el['left']}, {el['top']}, {el['width']}x{el['height']})" for el in ui_elements[:20]]
        )
        
        # Build the prompt for GPT-4
        prompt = (
            "You are a browser automation assistant. Based on the following list of UI elements extracted from a browser screenshot "
            "and the user's command, determine the necessary action to perform. Return a JSON object with the following keys:\n"
            "  - 'action': one of 'click', 'open', 'type', 'scroll', etc.\n"
            "  - 'target': the target element description or URL.\n"
            "  - 'value': any additional text required (if applicable).\n"
            "  - 'position': an object with 'x' and 'y' coordinates (ideally the center of the UI element's bounding box) where the action should occur.\n\n"
            "If the command cannot be executed, return a JSON object with an 'error' key containing a short error message (under 100 characters).\n\n"
            f"User Command: \"{command_text}\"\n\n"
            "UI Elements:\n"
            f"{ui_elements_str}"
        )
        
        # Call the OpenAI ChatCompletion API
        response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=150
        )
        
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
