from constants import *
from functions import *

if __name__ == "__main__":
    while True:
        # Wait for the user to say the greeting word
        print(f"Say '{GREETING_PROMPT}' to start your question")
        print(f"Say '{TERMINATE_PROMPT}' to stop talking")
        if microphone_listening() == False:
            break

