import os
from openai import AzureOpenAI

client = AzureOpenAI(
  api_key = "4b3f4e6cba854c2c8b5b644e897e0c84",
  api_version = "2024-02-01",
  azure_endpoint = "https://asw-poc-shared-aoai.openai.azure.com/"
)
#implement the chatbot
