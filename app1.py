from ollama import chat
from prompts_blueridge import prompt_text_2_sql

messages = [
  {
    'role': 'user',
    'content': 'What are the total number of types available',
    'prompt':prompt_text_2_sql
  },
]

response = chat('mannix/defog-llama3-sqlcoder-8b:latest', messages=messages)
print(response['message']['content'])
