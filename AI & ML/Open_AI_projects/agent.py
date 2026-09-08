import getpass
import json
import os
import sys

from openai import OpenAI


# The tool: ordinary Python code that runs on your computer.
def multiply(a, b):
    return a * b


# Tell the AI what the tool does and which inputs it accepts.
TOOLS = [
    {
        "type": "function",
        "name": "multiply",
        "description": "Multiply two numbers.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"},
            },
            "required": ["a", "b"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]


def run_agent(client, question):
    messages = [{"role": "user", "content": question}]

    # Limit the number of rounds so the agent cannot loop forever.
    for _ in range(5):
        response = client.responses.create(
            model="gpt-4.1-mini",
            instructions=(
                "You are a friendly beginner assistant. "
                "Always use the multiply tool for multiplication. "
                "Explain your final answer briefly."
            ),
            tools=TOOLS,
            input=messages,
        )

        messages.extend(response.output)

        tool_calls = [
            item for item in response.output
            if item.type == "function_call"
        ]

        # No tool requested: the AI has finished answering.
        if not tool_calls:
            return response.output_text

        for call in tool_calls:
            if call.name != "multiply":
                raise ValueError(f"Unknown tool: {call.name}")

            arguments = json.loads(call.arguments)
            result = multiply(**arguments)

            print(
                f"[Tool] multiply({arguments['a']}, "
                f"{arguments['b']}) = {result}"
            )

            # Send the tool's result back to the AI.
            messages.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": json.dumps({"result": result}),
            })

    return "Stopped after five rounds. Try a simpler question."


def main():
    # This test does not call the API or require a key.
    if "--test" in sys.argv:
        assert multiply(12, 8) == 96
        assert multiply(-3, 4) == -12
        assert multiply(0, 50) == 0
        assert multiply(2.5, 4) == 10
        print("All four tool tests passed.")
        return

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = getpass.getpass(
            "Enter your OpenAI API key (hidden): "
        ).strip()

    if not api_key:
        print("An API key is required to use the AI.")
        return

    client = OpenAI(api_key=api_key)
    print("Agent ready! Type 'exit' to stop.")

    while True:
        question = input("\nYou: ").strip()

        if question.lower() in {"exit", "quit"}:
            break
        if not question:
            continue

        try:
            print("Agent:", run_agent(client, question))
        except Exception as error:
            print(f"Request failed ({type(error).__name__}).")
            print("Check your connection, API key, and API account.")


if __name__ == "__main__":
    main()