import os
from dotenv import load_dotenv
from openai import OpenAI


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("Api key not found")

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
    user_prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    responses = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
    )

    if not responses.usage:
        raise RuntimeError("Response usage information not found")

    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {responses.usage.prompt_tokens}")
    print(f"Response tokens: {responses.usage.completion_tokens}")
    print(f"Response: \n{responses.choices[0].message.content}")


if __name__ == "__main__":
    main()
