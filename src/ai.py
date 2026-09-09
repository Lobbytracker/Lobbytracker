import openai
import os
from dotenv import load_dotenv

def aitta_prompts():
    load_dotenv()

    key = os.getenv('AITTA_API_KEY')

    url = "https://aitta-api.csc.fi/openai/v1"

    client = openai.OpenAI(api_key=key, base_url=url)
    chat_completion = client.chat.completions.create(messages=[{"role":"user",
                                                                "content":"count to ten backwords"}], model="openai/gpt-oss-120b", stream=True)

    for chunk in chat_completion:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end='', flush=True)