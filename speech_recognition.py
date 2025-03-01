import speech_recognition as sr
import logging

def wait_for_wake_word(wake_word): #Listen for the wake word continuously and return true when found
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Calibrate for ambient noise to improve recognition accuracy.
        recognizer.adjust_for_ambient_noise(source)
        logging.info("Microphone calibrated. Listening for wake word...")
        while True:
            try:
                # Listen for a short phrase
                audio = recognizer.listen(source, phrase_time_limit=3)
                try:
                    transcript = recognizer.recognize_google(audio).lower()
                    logging.debug(f"Transcript received: {transcript}")
                    if wake_word.lower() in transcript:
                        return True
                except sr.UnknownValueError:
                    # Could not understand the audio; continue listening.
                    continue
                except sr.RequestError as e:
                    logging.error(f"Google Speech Recognition service error: {e}")
                    continue
            except Exception as e:
                logging.error(f"Error during wake word listening: {e}")
    return False


