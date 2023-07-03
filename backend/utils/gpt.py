from dotenv import load_dotenv
import os
import random
import openai


load_dotenv()

openai_keys = [
    os.getenv("OPENAI_KEY1"),
    os.getenv("OPENAI_KEY2"),
    os.getenv("OPENAI_KEY3"),
]


async def translator(sentence: str):
    if await is_english(sentence):
        return sentence
    prefix = {
        "role": "system",
        "content": "Translate the following text to English.",
    }
    model = "gpt-4"
    openai.api_key = random.sample(openai_keys, 1)[0]
    messages = [prefix, {"role": "user", "content": sentence}]
    completion = openai.ChatCompletion.create(
        model=model, messages=messages, temperature=0, top_p=1, stop="\n"
    )
    res = completion.choices[0].message.content
    res = res.replace('"', "")
    return res


async def is_english(s):
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,.-")
    return all(char in allowed_chars for char in s)
