# Description: This script uses the Ollama API to update the uses of elements in a MongoDB database.
#

import os
from pydantic import BaseModel, Field, ValidationError
from ollama import Client
from colorama import Fore, Style, init
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

init(autoreset=True)  # Initialize colorama

DEBUG = True  # Set to False to turn off debug printing
OVERWRITE_USES = True  # Set to True to overwrite existing uses

ollama_client = Client(
  host=os.getenv('OLLAMA_URI'), # http://localhost:11434
)

class ClassPercentage(BaseModel):
    class_: str = Field(..., alias='class')
    percentage: int

class Element(BaseModel):
    element_name: str
    atomic_number: int
    uses: list[str]
    classes: list[ClassPercentage]

valid_uses = ["fuel", "lifesupport", "energystorage", "construction", "electronics", "coolants", "industrial", "medical", "propulsion", "shielding", "agriculture", "mining"]
valid_classes = {
    "classes": [
        {"class": "C", "percentage": "INT 0 to 100"},
        {"class": "S", "percentage": "INT 0 to 100"},
        {"class": "M", "percentage": "INT 0 to 100"}
    ]
}

MONGO_URI = os.getenv('MONGO_URI')
data = []

if MONGO_URI:
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client.asteroids
    collection = db.elements
    data = list(collection.find({}))
else:
    raise ValueError("MONGO_URI environment variable is not set")

for element in data:
    if not OVERWRITE_USES and "uses" in element:
        if DEBUG:
            print(Fore.YELLOW + f"Skipping element {element['name']} with existing uses")
        continue

    while True:
        response = ollama_client.chat(
          messages=[
            {
              'role': 'user',
              'content': f'Respond in JSON with a list of uses for the element {element["name"]} atomic number {element["number"]} using ONLY the following use strings: {valid_uses}. Ensure that the uses are strictly from this list and relevant to the element. Exclude lighting. As part of the JSON document include a classes field where the schema looks like {valid_classes}, the percentage should be its likelihood of appearing in each asteroid class.',
            }
          ],
          model='granite3.1-dense:8b',
          format=Element.model_json_schema(),
        )
        try:
            validated = Element.model_validate_json(response.message.content)
            element_uses = validated.uses
            element_classes = validated.classes

            # Check if all uses are valid and atomic_number is a non-zero int
            if all(use in valid_uses for use in element_uses) and isinstance(validated.atomic_number, int) and validated.atomic_number != 0:
                if DEBUG:
                    print(Fore.GREEN + f"Accepted: {validated}")
                
                # Embed the uses array and classes array in matching JSON objects
                collection.update_one(
                    {"number": element["number"]},
                    {"$set": {"uses": element_uses, "classes": [cls.model_dump(by_alias=True) for cls in element_classes]}}
                )

                break  # Exit the loop if all uses are valid and atomic_number is a non-zero int
            else:
                if DEBUG:
                    print(Fore.RED + f"Rejected: {validated}")
        except ValidationError as e:
            if DEBUG:
                print(Fore.RED + f"Validation error: {e}")





