import pyautogui as pag
import logging

def capture_screenshot():
    """
    Captures a screenshot of the current screen.

    Returns:
        A Pillow Image object representing the screenshot.
    """
    try:
        logging.info("Capturing screenshot...")
        screenshot = pag.screenshot()
        logging.info("Screenshot captured successfully.")
        return screenshot
    except Exception as e:
        logging.error(f"Failed to capture screenshot: {e}")
        return None
