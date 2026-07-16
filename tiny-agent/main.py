import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("Api key not found")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    responses = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    if not responses.usage:
        raise RuntimeError("Response usage information not found")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {responses.usage.prompt_tokens}")
        print(f"Response tokens: {responses.usage.completion_tokens}")

    print(f"Response: \n{responses.choices[0].message.content}")


if __name__ == "__main__":
    main()
