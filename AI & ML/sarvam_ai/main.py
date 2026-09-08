import os

from dotenv import load_dotenv
from sarvamai import SarvamAI


# Load variables from .env
load_dotenv()

# Get Sarvam API key
api_key = os.getenv("SARVAM_API_KEY")

# Make sure the key exists
if not api_key:
    raise ValueError(
        "SARVAM_API_KEY was not found. "
        "Make sure your .env file exists."
    )

# Create Sarvam AI client
client = SarvamAI(
    api_subscription_key=api_key
)

# Send a message
response = client.chat.completions(
    model="sarvam-105b",
    messages=[
        {
            "role": "user",
            "content": "Explain what BGP is in simple terms."
        }
    ]
)

# Print AI response
print("\nSarvam AI Response:")
print("-------------------")
print(response.choices[0].message.content)