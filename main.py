import time
import logging
from voice_recognition import wait_for_wake_word, record_command
from screenshot_handler import capture_screenshot
from openai_api import analyze_command
from action_executor import perform_action
from notifier import notify_user
from config import WAKE_WORD, SILENCE_THRESHOLD, LOOP_SLEEP_DURATION

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    logging.info("Starting web accessibility app...")
    
    while True:
        try:
            # Listen continuously for the wake word (e.g., "browser")
            logging.info("Listening for wake word...")
            if wait_for_wake_word(WAKE_WORD):
                # Notify that the wake word was detected
                notify_user("Wake word detected!")
                logging.info("Wake word detected! Notifying user.")
                
                # Notify that the app is now ready to accept a command
                notify_user("Ready to accept command!")
                logging.info("Ready to accept command!")

                # Record the command until a period of silence is detected
                command_text = record_command(silence_threshold=SILENCE_THRESHOLD)
                logging.info(f"Command received: {command_text}")

                # Capture a screenshot of the current browser view
                screenshot = capture_screenshot()
                
                # Process the command with the OpenAI API
                action_details = analyze_command(command_text, screenshot)
                logging.info(f"Action details: {action_details}")
                
                # Check if the API validation returned an error message
                if "error" in action_details:
                    error_message = action_details["error"]  # Should be less than 100 characters.
                    notify_user(error_message)
                    logging.error(f"Validation error: {error_message}")
                else:
                    # Execute the action based on the API response
                    if perform_action(action_details):
                        logging.info(f"Action details from API: {action_details}")
                        notify_user("Task completed successfully.")
                        logging.info("Action executed successfully.")
                    else:
                        notify_user("Error: Unable to complete the task.")
                        logging.error("Action execution failed.")

            # Short sleep to avoid high CPU usage in the loop
            time.sleep(LOOP_SLEEP_DURATION)
            
        except KeyboardInterrupt:
            logging.info("Shutting down...")
            break

if __name__ == "__main__":
    main()
