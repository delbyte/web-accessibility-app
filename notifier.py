import logging
from plyer import notification

def notify_user(message, title="Browser Automation"): # Sends a notif to the user on their desktop. Args: message(the message to display), title(the title of the notif)
    try:
        notification.notify(
            title=title,
            message=message,
            app_name="Web Accessibility App",
            timeout=3 
        )
        logging.info("Notification sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send notification: {e}")
