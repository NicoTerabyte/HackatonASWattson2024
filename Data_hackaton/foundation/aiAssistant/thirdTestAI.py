import os
import openai
# from azure.ai.textanalytics import TextAnalyticsClient
# from azure.core.credentials import AzureKeyCredential

# Imposta le credenziali per Text Analytics di Azure
# azure_key = "4b3f4e6cba854c2c8b5b644e897e0c84"
# endpoint = "https://asw-poc-shared-aoai.openai.azure.com/"  # Inserisci l'endpoint corretto
# text_analytics_client = TextAnalyticsClient(endpoint, AzureKeyCredential(azure_key))

openai.api_type = "azure"
openai.api_base = "https://ai-riders2932149880941.openai.azure.com/"
openai.api_version = "2024-15-02-preview"

openai.api_key = "ede9ceac74d646c2ad904bf51a4bb715"

message_text = [
    {
		"role":"system",
		"content": "you're an expert of beauty skincare and healthy products"
    },
	{
		"role":"user",
		"content":"Hi how are you?"
    }
]


completion = openai.ChatCompletion.create(
	engine="gpt-4",
	messages=message_text,
	temperature=0.7,
	max_tokens=800,
	top_p=0.95,
	frequency_penalty=0,
	presence_penalty=0,
	stop=None
)

print(completion)
