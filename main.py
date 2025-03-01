import time
import logging
from speech_recognition import wait_for_wake_word, record_command
from screenshot_handler import capture_screenshot
from openai_api import analyze_command
from action_executor import perform_action
from notifier import notify_user
from config import WAKE_WORD, SILENCE_THRESHOLD

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    logging.info("Starting web accessibility app...")

    while True:
        try:
            # Listen continuously for the wake word
            logging.info("Listening for wake word...")
            if wait_for_wake_word(WAKE_WORD):
                logging.info("Wake word detected! Listening for command...")

                # Record the command until silence is detected
                command_text = record_command(silence_threshold=SILENCE_THRESHOLD)
                logging.info(f"Command received: {command_text}")

                # Capture a screenshot of the current browser view
                screenshot = capture_screenshot()

                # This function should return a dict with either the action details or an error key.
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
                        notify_user("Task completed successfully.")
                        logging.info("Action executed successfully.")
                    else:
                        # If the action failed without a specific error from validation, provide a default error message
                        default_error = "Error: Action could not be executed."
                        notify_user(default_error)
                        logging.error(default_error)

            # Short sleeptime to avoid high CPU usage in the loop
            time.sleep(0.5)

        except KeyboardInterrupt:
            logging.info("Shutting down...")
            break

if __name__ == "__main__":
    main()
