# config.py

# Wake word that triggers the app
WAKE_WORD = "hello"

# Threshold (in seconds) to determine when the user stops speaking
SILENCE_THRESHOLD = 2.0

# Maximum number of UI elements to include in the prompt to avoid token bloat
MAX_UI_ELEMENTS = 500

# Duration to sleep between listening loops (in seconds)
LOOP_SLEEP_DURATION = 0.3

# OpenAI API parameters
OPENAI_MODEL = "gpt-4"
OPENAI_TEMPERATURE = 0.2
OPENAI_MAX_TOKENS = 150
