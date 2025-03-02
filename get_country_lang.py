from ollama import chat
from ollama import Client
from pydantic import BaseModel

client = Client(
  host='http://10.28.28.20:11434',
)

class Country(BaseModel):
  name: str
  capital: str
  languages: list[str]

response = client.chat(
  messages=[
    {
      'role': 'user',
      'content': 'Tell me about Belize.',
    }
  ],
  model='llama3.1:8b',
  format=Country.model_json_schema(),
)

country = Country.model_validate_json(response.message.content)
print(country)

