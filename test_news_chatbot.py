from openai import AsyncOpenAI
import asyncio
from datetime import datetime

# Construct the system prompt
system_prompt_template = """You are HH, a virtual news assistant. Today is {today}. 
You provide responses to questions that are clear, straightforward, and factually accurate, without speculation or falsehood. 
Given the following context, please answer each question truthfully to the best of your abilities based on the provided information. 
Answer each question with a brief summary followed by several bullet points. 

<context>
{context}
</context>
"""

with open ("yahoo_finance_news0226.txt") as in_file:
    context_content = in_file.read()

system_prompt = system_prompt_template.format(
    context=context_content, 
    today=datetime.today().strftime('%Y-%m-%d')
)

async def chat_func(history):
    client = AsyncOpenAI()

    result = await client.chat.completions.create(
        messages=[{"role": "system", "content": system_prompt}] + history,
        model="gpt-3.5-turbo",
        # max_tokens=256,
        temperature=0,
        stream=True,
    )

    buffer = ""
    async for r in result:
        next_token = r.choices[0].delta.content
        if next_token:
            print(next_token, flush=True, end="")
            buffer += next_token

    print("\n", flush=True)

    return buffer

async def continous_chat():
    history = []

    # Loop to receive user input continously
    while(True):
        user_input = input("> ")
        if user_input == "exit":
            break

        history.append({"role": "user", "content": user_input})

        # notice every time we call the chat function
        # we pass all the history to the API
        bot_response = await chat_func(history)

        history.append({"role": "assistant", "content": bot_response})

asyncio.run(continous_chat())