# Import necessary libraries
from openai import OpenAI
# from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

client = OpenAI()

my_assistant = client.beta.assistants.create(
	name="Beauty advisor"
	instructions="You are a beauty expert, that uses a Gen z slang to communicate and helps the customers by suggesting products",
	tools=[{"type":"code_interpreter"}],
	model="gpt-4-turbo-preview",
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
	thread_id=thread.id,
    role="user",
    content="My skin got a little irritaded, what product you suggest to make it less irritated?"
)
