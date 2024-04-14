import os
import time
from openai import AzureOpenAI
import requests


client = AzureOpenAI(
  api_key = "ede9ceac74d646c2ad904bf51a4bb715",
  api_version = "2024-02-15-preview",
  azure_endpoint = "https://ai-riders2932149880941.openai.azure.com/"
)
<<<<<<< HEAD

assistant = client.beta.assistants.create(
    name="Riders",
    instructions=f"You are a helpful AI assistant, which knows perfectly the products dataset"
    f"Be free to connect emotionally with customers, which are most likely Gen Z and Gen Alpha"
    f"So you need to know their behaviour to make them recommendations",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4"
)

# print(assistant.model_dump_json(indent=2))

thread = client.beta.threads.create()
# print(thread)


'''
# Add a user question to the thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I have dry skin, what product you recommend to me?"
)
# Run the thread
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
)

# Retrieve the status of the run
run = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)

status = run.status
print(status)

'''
thread_message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="How does AI work? Explain it in simple terms.",
)
#print(thread_message)

thread_messages = client.beta.threads.messages.list(thread_id=thread.id)
#print(thread_messages.data) # shows all the messages in the thread

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
)
#print(run)

counter = 0
while run.status != 'completed':
  run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
  if counter % 10 == 0:
    print(f"\t\t{run}")
    counter += 1
    time.sleep(5)

'''
#implement the chatbot
response = client.chat.completions.create(
    model="gpt-",
    messages=[
        { "role": "system", "content": "You are a helpful assistant." },
        { "role": "user", "content": [
            {
                "type": "text",
                "text": "Describe this picture:"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": "<image URL>"
                }
            }
        ] }
    ],
    max_tokens=2000
)
print(response)
'''
