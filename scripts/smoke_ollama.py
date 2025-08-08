#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from openai import OpenAI


def main():
    load_dotenv()
    base_url = os.getenv('OPENAI_BASE_URL', 'http://localhost:11434/v1')
    api_key = os.getenv('OPENAI_API_KEY', 'ollama')
    model = os.getenv('OPENAI_MODEL', 'gpt-oss-120b')

    client = OpenAI(api_key=api_key, base_url=base_url)
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Say hello in one short sentence."}],
    )
    print(resp.choices[0].message.content)


if __name__ == "__main__":
    main()

