import pyautogui
import webbrowser
import logging
import os

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
                # Register Brave browser
                brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
                if os.path.exists(brave_path):
                    webbrowser.register('brave', None, webbrowser.BackgroundBrowser(brave_path))
                    webbrowser.get('brave').open(target)
                else:
                    webbrowser.open(target)  # Fallback to default browser if Brave is not found
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
            # Use the 'direction' key from the API response
            direction = action_details.get("direction", "").lower()
            if "down" in direction:
                pyautogui.scroll(-300)  # Negative value scrolls down.
                logging.info("Scrolled down.")
                return True
            elif "up" in direction:
                pyautogui.scroll(300)   # Positive value scrolls up.
                logging.info("Scrolled up.")
                return True
            else:
                logging.error(f"Scroll direction '{direction}' not recognized.")
                return False
            
        elif action == "change":
            #Change tabs with pyautogui
            if value:
                if "next" in value:
                    pyautogui.hotkey('ctrl', 'tab')
                    logging.info("Changed to next tab.")
                    return True
                elif "previous" in value:
                    pyautogui.hotkey('ctrl', 'shift', 'tab')
                    logging.info("Changed to previous tab.")
                    return True
                else:
                    logging.error(f"Tab change value '{value}' not recognized.")
                    return False
        else:
            logging.error(f"Action '{action}' is not supported.")
            return False

    except Exception as e:
        logging.error(f"Error executing action: {e}")
        return False
