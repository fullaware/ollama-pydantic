import os
import logging
from pydantic import BaseModel, field_validator, ValidationError
from ollama import Client
from colorama import Fore, Style, init
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

init(autoreset=True)  # Initialize colorama

DEBUG = True  # Set to False to turn off debug printing
LOGGING = False  # Set to True to enable logging to progress.log
OVERWRITE_CLASS = False  # Set to True to overwrite existing uses

# Set up logging
if LOGGING:
    logging.basicConfig(filename='progress.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

ollama_client = Client(
  host=os.getenv('OLLAMA_URI'), # http://localhost:11434
)

class Asteroid(BaseModel):
  name: str
  class_: str

  @field_validator('class_')
  def validate_class(cls, v):
    if v not in {"C", "S", "M"}:
      raise ValueError("Class must be one of 'C', 'S', or 'M'")
    return v

MONGO_URI = os.getenv('MONGO_URI')
data = []

if MONGO_URI:
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client.asteroids
    collection = db.asteroids
    data = list(collection.find({}))
else:
    raise ValueError("MONGO_URI environment variable is not set")

counter = 0  # Initialize counter

for asteroid in data:
    if not OVERWRITE_CLASS and "class" in asteroid:
        if DEBUG:
            counter += 1
            message = f"Skipping asteroid {asteroid.get('name', 'unknown')} with existing class"
            print(Fore.YELLOW + f"{counter}: " + message)
            if LOGGING:
                logging.debug(message)
        continue

    if 'name' not in asteroid:
        if DEBUG:
            counter += 1
            message = "Error: Asteroid data missing 'name' key"
            print(Fore.RED + f"{counter}: " + message)
            if LOGGING:
                logging.debug(message)
        continue

    while True:
        response = ollama_client.chat(
          messages=[
            {
              'role': 'user',
              'content': f'Respond in JSON with only one of the following letters C, S, or M. These are the possible class of asteroid {asteroid["name"]}.',
            }
          ],
          model='granite3.1-dense:8b',
          format=Asteroid.model_json_schema(),
        )
        try:
            validated = Asteroid.model_validate_json(response.message.content)
            asteroid_class = validated.class_

            # Check if the class is valid
            if asteroid_class in {"C", "S", "M"}:
                if DEBUG:
                    counter += 1
                    message = f"Accepted: {validated}"
                    print(Fore.GREEN + f"{counter}: " + message)
                    if LOGGING:
                        logging.debug(message)
                
                # Embed the class in matching JSON objects
                collection.update_one(
                    {"name": asteroid["name"], "class": {"$exists": False}},
                    {"$set": {"class": asteroid_class}}
                )

                break  # Exit the loop if the class is valid
            else:
                if DEBUG:
                    counter += 1
                    message = f"Rejected: {validated}"
                    print(Fore.RED + f"{counter}: " + message)
                    if LOGGING:
                        logging.debug(message)
        except ValidationError as e:
            if DEBUG:
                counter += 1
                message = f"Validation error: {e}"
                print(Fore.RED + f"{counter}: " + message)
                if LOGGING:
                    logging.debug(message)
            # Retry the asteroid
            continue





