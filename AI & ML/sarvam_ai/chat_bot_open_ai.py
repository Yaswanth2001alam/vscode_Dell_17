import os

from dotenv import load_dotenv
from sarvamai import SarvamAI


load_dotenv()

api_key = os.getenv("SARVAM_API_KEY")

if not api_key:
    raise ValueError("SARVAM_API_KEY not found in .env")

client = SarvamAI(
    api_subscription_key=api_key
)

print("Sarvam AI Chat")
print("Type 'exit' to stop.\n")


while True:

    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    try:
        response = client.chat.completions(
            model="sarvam-105b",
            messages=[
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        answer = response.choices[0].message.content

        print(f"\nSarvam AI: {answer}\n")

    except Exception as e:
        print(f"\nError: {e}\n")