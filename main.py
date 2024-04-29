from model.Assistant import Assistant

assistant = Assistant()

print("Welcome to the AI Beauty Coach/Advisor\nHow can I help you today?")
question = input("Type your question or problem:\n")
assistant.process_prompt(question)