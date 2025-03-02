from pydantic import BaseModel

from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel

ollama_model = OllamaModel(
    model_name='llama3.1:8b',  
    base_url='http://10.28.28.20:11434/v1',  
)


class CityLocation(BaseModel):
    city: str
    country: str


agent = Agent(model=ollama_model, result_type=CityLocation)

result = agent.run_sync('Where were the olympics held in 2016?')
print(result.data)
#> city='London' country='United Kingdom'
print(result.usage())
"""
Usage(requests=1, request_tokens=57, response_tokens=8, total_tokens=65, details=None)
"""
