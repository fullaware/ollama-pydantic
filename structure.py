from ollama import Client
from pydantic import BaseModel

client = Client(
  host='http://10.28.28.20:11434',
)

class President(BaseModel):
  name: str
  number: int 
  years: list[int]

response = client.chat(
  messages=[
    {
      'role': 'user',
      'content': 'Tell me about US President George Washington, what number was he and what years did he serve?',
    }
  ],
  model='llama3.1:8b',
  format=President.model_json_schema(),
)

president = President.model_validate_json(response.message.content)
print(president)

