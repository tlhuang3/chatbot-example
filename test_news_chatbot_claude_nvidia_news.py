from anthropic import AsyncAnthropic
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

with open ("nvidia_news_0309.txt") as in_file:
    context_content = in_file.read()


system_prompt = system_prompt_template.format(
    context=context_content, 
    today=datetime.today().strftime('%Y-%m-%d')
)


async def chat_func(history):
    client = AsyncAnthropic()

    async with client.messages.stream(
        messages=history,
        model="claude-3-opus-20240229",
        max_tokens=1024,
        temperature=0
    ) as result:
        buffer = ""
        async for r in result.text_stream:
            next_token = r
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
        if not history:
            history.append({"role": "user", "content": system_prompt + " " + user_input})
        else:
            history.append({"role": "user", "content": user_input}) 
        # notice every time we call the chat function
        # we pass all the history to the API
        bot_response = await chat_func(history)

        history.append({"role": "assistant", "content": bot_response})

asyncio.run(continous_chat())