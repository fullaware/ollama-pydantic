import json
from pydantic import BaseModel
from ollama import Client
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize colorama

DEBUG = True  # Set to False to turn off debug printing

client = Client(
  host='http://10.28.28.20:11434',
)

class Element(BaseModel):
  element_name: str
  atomic_number: int
  uses: list[str]

valid_uses = ["fuel", "lifesupport", "energystorage", "construction", "electronics", "coolants", "industrial", "medical", "propulsion", "shielding", "agriculture", "mining"]

with open("elements.json", "r") as f:
    data = json.load(f)

for element in data:
    while True:
        response = client.chat(
          messages=[
            {
              'role': 'user',
              'content': f'Respond in JSON with a list of uses for the element {element["name"]} atomic number {element["number"]} using ONLY the following use strings: {valid_uses}. Ensure that the uses are strictly from this list and relevant to the element. Exclude lighting',
            }
          ],
          model='granite3.1-dense:8b',
          format=Element.model_json_schema(),
        )
        validated = Element.model_validate_json(response.message.content)
        element_uses = validated.uses

        # Check if all uses are valid and atomic_number is a non-zero int
        if all(use in valid_uses for use in element_uses) and isinstance(validated.atomic_number, int) and validated.atomic_number != 0:
            if DEBUG:
                print(Fore.GREEN + f"Accepted: {validated}")
            
            # Embed the uses array in matching JSON objects
            for e in data:
                if e["number"] == element["number"]:
                    e["uses"] = element_uses
                    if DEBUG:
                        print(Fore.GREEN + f"Array: {e}")

            # Write the updated data back to the elements.json file
            with open("elements.json", "w") as f:
                json.dump(data, f, indent=2)
            break  # Exit the loop if all uses are valid and atomic_number is a non-zero int
        else:
            if DEBUG:
                print(Fore.RED + f"Rejected: {validated}")





