import os
from openai import AzureOpenAI

client = AzureOpenAI(
  api_key = "4b3f4e6cba854c2c8b5b644e897e0c84",
  api_version = "2024-02-01",
  azure_endpoint = "https://asw-poc-shared-aoai.openai.azure.com/"
)
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
