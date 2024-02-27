from openai import OpenAI
client = OpenAI()
import pprint

messages=[
    {"role": "system", "content": "You are a brilliant Michelin-starred level chef"},
    {"role": "user", "content": "I am Allan. I want to make a lunch plan for my weekdays."},
    {"role": "assistant", "content": "Hello, Allan. What kind of nutrition do you want to include?"},
  ]


def update_chat(messages, role, content):
	messages.append({"role": role, "content": content})
	return messages

def get_response(messages):
	completion = client.chat.completions.create(                                           
          model="gpt-3.5-turbo",                                                                     
          temperature = 0.2,
          messages= messages,
        ) 

	return completion.choices[0].message.content

while True:
	pprint.pprint(messages)
	user_input = input("\nEnter your message: (Enter 'Exit' to exit)")
	if user_input.lower() == 'exit':
		break
	messages = update_chat(messages, "user", user_input)
	model_response = get_response(messages)
	messages = update_chat(messages, "assistant", model_response)
#asyncio.run(chat_func())
