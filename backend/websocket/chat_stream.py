import openai
import time


openai.api_key = "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"

f = open('prefix.txt')
prefix = {"role": "user", "content": f.read()}
f.close()

prefix["content"] += str("\n" + "一隻憂鬱的海獅")
messages = [prefix]
start = time.time()
completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=messages,
    temperature=0,
)
waste_seconds = (time.time() - start)
print(f"1st time {waste_seconds}")
chat_response = completion
answer = chat_response.choices[0].message.content
print(answer)
# messages.append({"role": "assistant", "content": answer})

# messages.append({"role": "user", "content": "一隻憂鬱的海獅"})
# start = time.time()
# completion = openai.ChatCompletion.create(
# #   model="gpt-3.5-turbo",
#     model="gpt-4",
#     messages=messages,
#     temperature=0,
# )
# waste_seconds = (time.time() - start)
# print(f"2nd time {waste_seconds}")
# chat_response = completion
# answer = chat_response.choices[0].message.content
# print(answer)

# messages = [prefix]
# messages.append({"role": "assistant", "content": "Photorealistic Image: A cute, chubby cat lounging on a soft, plush pillow in a cozy, sunlit living room, with a warm color palette and soft shadows, inspired by professional pet photography, using a 35mm lens, medium shot, with natural sunlight streaming through the windows, and a soft bokeh effect in the background."})
# messages.append({"role": "user", "content": "一隻憂鬱的海獅"})
# start = time.time()
# completion = openai.ChatCompletion.create(
# #   model="gpt-3.5-turbo",
#     model="gpt-4",
#     messages=messages,
#     temperature=0,
# )
# waste_seconds = (time.time() - start)
# print(f"3nd time {waste_seconds}")
# chat_response = completion
# answer = chat_response.choices[0].message.content
# print(answer)