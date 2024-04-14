from datetime import datetime
import os
from dotenv import load_dotenv

import time
from pathlib import Path
from typing import Iterable
from openai import AzureOpenAI
from openai.types import FileObject
from openai.types.beta.threads.text_content_block import TextContentBlock
from openai.types.beta.threads.messages import MessageFile

load_dotenv()

should_cleanup: bool = True

api_key = os.getenv("OPENAI_KEY")
api_endpoint = os.getenv("OPENAI_URI")
api_version = os.getenv("OPENAI_VERSION")

# Create Client
client = AzureOpenAI(
  api_key = api_key,
  api_version = api_version,
  azure_endpoint = api_endpoint,
)

# Create Assistant
assistant = client.beta.assistants.create(
    name="AI Beauty coach/advisor",
    instructions=f"You are a helpful beauty assistant, which knows perfectly the products dataset"
    f"Be free to connect emotionally with customers, which are most likely Gen Z and Gen Alpha"
    f"So you need to know their behaviour to make them recommendations",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4"
)

# Create thread
thread = client.beta.threads.create()

# read the assistant file
def read_assistant_file(file_id:str):
    response_content = client.files.content(file_id)
    return response_content.read()

def print_messages(messages: Iterable[MessageFile]) -> None:
    message_list = []

    # Get all the messages till the last user message
    for message in messages:
        message_list.append(message)
        if message.role == "user":
            break

    # Reverse the messages to show the last user message first
    message_list.reverse()

    # Print the user or Assistant messages or images
    for message in message_list:
        for item in message.content:
            # Determine the content type
            if isinstance(item, TextContentBlock):
                print(f"{message.role}:\n{item.text.value}\n")
                file_annotations = item.text.annotations
                if file_annotations:
                    for annotation in file_annotations:
                        file_id = annotation.file_path.file_id
                        content = read_assistant_file(file_id)
                        print(f"Annotation Content:\n{str(content)}\n")

def process_prompt(prompt: str) -> None:
    client.beta.threads.messages.create(thread_id=thread.id, role="user", content=prompt)
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Please address the user as Lucy. The user has account. Be assertive, accurate, polite, and kind. Ask if the user has further questions. "
        + "The current date and time is: "
        + datetime.now().strftime("%x %X")
        + ". ",
    )
    print("processing ...")
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run.status == "completed":
            # Handle completed
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            print_messages(messages)
            break
        if run.status == "failed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            answer = messages.data[0].content[0].text.value
            print(f"Failed User:\n{prompt}\nAssistant:\n{answer}\n")
            # Handle failed
            break
        if run.status == "expired":
            # Handle expired
            print(run)
            break
        if run.status == "cancelled":
            # Handle cancelled
            print(run)
            break
        if run.status == "requires_action":
            # Handle function calling and continue processing
            pass
        else:
            time.sleep(5)

# Problem/Question of the user
print(process_prompt("My skin got a little irritated, what product you suggest to make it less irritated?"))
print(process_prompt("I have acne and I want to get rid of it, what ?"))

if should_cleanup:
    client.beta.assistants.delete(assistant.id)
    client.beta.threads.delete(thread.id)

'''
# Upload files to the assistant from the data folder // at this moment not applicable
DATA_FOLDER = "data/"
ai_files = []

def upload_file(client: AzureOpenAI, path: str) -> FileObject:
    print(path)
    with Path(path).open("rb") as f:
        return client.files.create(file=f, purpose="assistants")

arr = os.listdir(DATA_FOLDER)
assistant_files = []
for file in arr:
    filePath = DATA_FOLDER + file
    assistant_file = upload_file(client, filePath)
    ai_files.append(assistant_file)
    assistant_files.append(assistant_file)

file_ids = [file.id for file in assistant_files]
file_ids
'''

'''
# elif stmt to display images
elif isinstance(item, ImageFileContentBlock):
    # Retrieve image from file id
    data_in_bytes = read_assistant_file(item.image_file.file_id)
    # Convert bytes to image
    readable_buffer = io.BytesIO(data_in_bytes)
    image = Image.open(readable_buffer)
    # Resize image to fit in terminal
    width, height = image.size
    image = image.resize((width // 2, height // 2), Image.LANCZOS)
    # Display image
    image.show()
'''