import openai


openai.api_key = "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"

f = open('prefix.txt')
prefix = {"role": "user", "content": f.read()}
f.close()

answer = {"role": "system", "content": "Yes, I'm ready. Please provide me with a keyword, and I will generate a detailed prompt based on the given structure and guidelines."}

messages = [prefix, answer]
while True:
    content = input("User: ")
    messages.append({"role": "user", "content": content})
    completion = openai.ChatCompletion.create(
    #   model="gpt-3.5-turbo",
        model="gpt-4",
        messages=messages
    )

    chat_response = completion
    answer = chat_response.choices[0].message.content
    print(f'ChatGPT: {answer}')
    messages.append({"role": "assistant", "content": answer})
