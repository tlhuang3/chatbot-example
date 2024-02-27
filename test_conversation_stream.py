from openai import OpenAI
client = OpenAI()
import pprint

messages=[
    {"role": "system", "content": "You are a brilliant Michelin-starred level chef"},
    {"role": "user", "content": "I am Allan. I want to make a lunch plan for my weekdays."},
    {"role": "assistant", "content": "Hello, Allan. What kind of nutrition do you want to include?"},
  ]


history = []
print(messages)
while True:
	user_input = input("\nEnter your message: (Enter 'Exit' to exit)")
	if user_input.lower() == 'exit':
		break
	messages.append({"role": "user", "content": user_input})
	
	completion = client.chat.completions.create(                                        model="gpt-3.5-turbo",
        temperature = 0.2,
        messages= messages + history,
	stream = True	
        ) 
	
	#Receive tokens in a streaming way
	buffer = ""
	for chunk in completion:
		if chunk.choices[0].delta.content is not None:
			next_token = chunk.choices[0].delta.content
			print(next_token, flush=True, end = "")
			buffer += next_token
	print()
	history.append({"role": "assistant", "content": buffer})
