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
if not OPENAI_API_KEY:
    logging.error("OpenAI API key is not set.")
    raise RuntimeError("API key not set.")
client = OpenAI(api_key="OPENAI_API_KEY")

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
    try:
        # Extract UI elements from the screenshot
        ui_elements = extract_ui_elements(screenshot)
        
        # Log each extracted element
        logging.info("OCR Extracted UI Elements:")
        for el in ui_elements:
            logging.info(f"Text: '{el['text']}' at ({el['left']}, {el['top']}), size: {el['width']}x{el['height']}")
        
        # Build a string summary (limit to first MAX_UI_ELEMENTS to avoid token bloat)
        from config import MAX_UI_ELEMENTS
        ui_elements_str = "\n".join(
            [f"{el['text']} at ({el['left']}, {el['top']}, {el['width']}x{el['height']})" for el in ui_elements[:MAX_UI_ELEMENTS]]
        )
        
        # Log the UI elements summary that will be sent in the prompt
        logging.info("UI Elements Summary:\n" + ui_elements_str)
        
        # Build the prompt
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
        
        # (Streaming response code continues as before)
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        streaming_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            max_tokens=150,
            temperature=0.2
        )
        
        full_message = ""
        print("Streaming response:")
        for chunk in streaming_response:
            token = chunk.choices[0].delta.content
            if token is None:
                token = ""
            print(token, end="", flush=True)
            full_message += token
        print()  # Newline after streaming
        
        # Log the full message received before parsing
        logging.info("Full streaming response:\n" + full_message)
        
        try:
            result = json.loads(full_message)
        except json.JSONDecodeError:
            logging.error("Failed to parse JSON response from OpenAI API. Full message: " + full_message)
            return {"error": "Failed to parse API response."}
        
        return result

    except Exception as e:
        logging.error(f"Error in analyze_command: {e}")
        return {"error": "API error occurred."}

