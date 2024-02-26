from openai import AsyncOpenAI
import time
import asyncio
client = AsyncOpenAI()

system_prompt_template = """Given the following context, please answer each question.

{context}
"""

with open("yahoo_finance_news0226.txt") as in_file:
	context_content = in_file.read()

system_prompt = system_prompt_template.format(context = context_content)

async def chat_func():
	completion = await client.chat.completions.create(
	  model="gpt-3.5-turbo",
	  max_tokens = 256,
	  temperature = 0,
	  messages=[
	    {"role": "system", "content": system_prompt},
	    {"role": "user", "content": "Summarize the news."}
	  ],
	  stream = True
	)


#print(completion.choices[0].message.content)
	async for chunk in completion:
		if chunk.choices[0].delta.content is not None:
			print(chunk.choices[0].delta.content, flush=True, end = "")

asyncio.run(chat_func())
