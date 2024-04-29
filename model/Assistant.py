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

class Assistant:
    def __init__(self):
        load_dotenv()
        self.client = self.initialize_client()
        self.assistant = self.create_assistant()
        self.thread = self.client.beta.threads.create()

    def initialize_client(self):
        client = AzureOpenAI(
            api_key = os.getenv("OPENAI_KEY"),
            api_endpoint = os.getenv("OPENAI_URI"),
            azure_endpoint = os.getenv("OPENAI_VERSION"),
        )
        return client

    # instructions are hardcoded for the beauty assistant
    def create_assistant(self):
        return self.client.beta.assistants.create(
            name="AI Beauty coach/advisor",
            instructions=f"You are a helpful beauty assistant, which knows perfectly the products dataset"
            f"Be free to connect emotionally with customers, which are most likely Gen Z and Gen Y"
            f"So you need to know their behaviour to make them recommendations",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4"
        )

    # read the assistant file
    def read_assistant_file(file_id:str, self):
        response_content = self.client.files.content(file_id)
        return response_content.read()

    def print_messages(messages: Iterable[MessageFile], self) -> None:
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
                            content = self.read_assistant_file(file_id)
                            print(f"Annotation Content:\n{str(content)}\n")

    # handle user prompt (instructions are hardcoded for the beauty assistant how to respond to the user prompt)
    def process_prompt(prompt: str, self) -> None:
        self.client.beta.threads.messages.create(thread_id=self.thread.id, role="user", content=prompt)
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            instructions="Please address the user as Lucy. The user has account. Be assertive, accurate, polite, and kind. Ask if the user has further questions. "
            + "The current date and time is: "
            + datetime.now().strftime("%x %X")
            + ". ",
        )
        print("processing ...")
        while True:
            run = self.client.beta.threads.runs.retrieve(thread_id=self.thread.id, run_id=run.id)
            if run.status == "completed":
                # Handle completed
                messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
                self.print_messages(messages)
                break
            if run.status == "failed":
                messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
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

    def selfClean(self):
        self.client.beta.assistants.delete(self.assistant.id)
        self.client.beta.threads.delete(self.thread.id)