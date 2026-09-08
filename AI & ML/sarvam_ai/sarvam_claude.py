"""
Basic Sarvam AI chat completion script.

Setup:
    1. pip install -r requirements.txt
    2. Create a .env file (copy .env.example) and add your real API key
    3. Run: python main.py
"""

import os
import sys
from dotenv import load_dotenv
from sarvamai import SarvamAI

# Load variables from .env into the environment
load_dotenv()

API_KEY = os.getenv("SARVAM_API_KEY")

if not API_KEY:
    print("ERROR: SARVAM_API_KEY not found. Make sure you have a .env file "
          "with a line like: SARVAM_API_KEY=your_key_here")
    sys.exit(1)

# Initialize the Sarvam AI client
client = SarvamAI(api_subscription_key=API_KEY)


def ask_sarvam(user_message: str) -> str:
    """Send a single user message to Sarvam AI and return the reply text."""
    response = client.chat.completions(
        model="sarvam-105b",  # Sarvam's flagship chat model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    print("Sarvam AI basic chat script")
    print("Type your message (or 'exit' to quit)\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        if not user_input:
            continue

        try:
            reply = ask_sarvam(user_input)
            print(f"Sarvam: {reply}\n")
        except Exception as e:
            print(f"Something went wrong: {e}\n")