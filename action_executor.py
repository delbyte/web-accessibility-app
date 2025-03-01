import pyautogui
import webbrowser
import logging

def perform_action(action_details):
    """
    Executes the action based on the provided details.
    
    Expected action_details format (for a click action):
    {
        "action": "click",
        "target": "login button",
        "value": "",
        "position": {"x": 500, "y": 400}
    }
    
    For other actions, the API should supply the necessary information.
    
    Returns:
        True if action was executed successfully, False otherwise.
    """
    try:
        action = action_details.get("action", "").lower()
        target = action_details.get("target", "").lower()
        value = action_details.get("value", "")
        position = action_details.get("position")

        logging.info(f"Performing action: {action}, target: {target}, value: {value}, position: {position}")

        if action == "click":
            # Expect the API to provide the exact coordinates of the UI element.
            if position and "x" in position and "y" in position:
                x = position["x"]
                y = position["y"]
                pyautogui.moveTo(x, y, duration=0.2)
                pyautogui.click()
                logging.info(f"Clicked on {target} at ({x}, {y}).")
                return True
            else:
                logging.error("Position for click action not provided by API.")
                return False

        elif action == "open":
            # Use webbrowser to open a URL if provided.
            if target:
                webbrowser.open(target)
                logging.info(f"Opened {target} in the browser.")
                return True
            else:
                logging.error("No URL provided for open action.")
                return False

        elif action == "type":
            # Use typewrite for typing actions.
            if value:
                pyautogui.typewrite(value, interval=0.05)
                logging.info(f"Typed '{value}'.")
                return True
            else:
                logging.error("No text provided for type action.")
                return False

        elif action == "scroll":
            # For scrolling, assume target provides the direction (if no direction is provided, scroll down by default)
            if target == "down":
                pyautogui.scroll(-300)  # Negative scroll for down.
                logging.info("Scrolled down.")
                return True
            elif target == "up":
                pyautogui.scroll(300)   # Positive scroll for up.
                logging.info("Scrolled up.")
                return True
            else:
                pyautogui.scroll(-300)  # Negative scroll for down.
                logging.info("Scrolled down.")
            

        else:
            logging.error(f"Action '{action}' is not suppsorted.")
            return False

    except Exception as e:
        logging.error(f"Error executing action: {e}")
        return False
