import json
from pydantic import BaseModel, field_validator, ValidationError
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
  classes: dict[str, int]

  @field_validator('classes')
  def validate_classes(cls, v):
    if set(v.keys()) != {"C", "S", "M"}:
      raise ValueError("Classes must include 'C', 'S', and 'M'")
    return v

valid_uses = ["fuel", "lifesupport", "energystorage", "construction", "electronics", "coolants", "industrial", "medical", "propulsion", "shielding", "agriculture", "mining"]
asteroid_classes = ["C", "S", "M"]

with open("elements.json", "r") as f:
    data = json.load(f)

for element in data:
    while True:
        response = client.chat(
          messages=[
            {
              'role': 'user',
              'content': f'Respond in JSON with a list of uses for the element {element["name"]} atomic number {element["number"]} using ONLY the following use strings: {valid_uses}. Ensure that the uses are strictly from this list and relevant to the element. Exclude lighting.  Assign the likelyhood in whole number percentages of this element appearing in C, S, M class asteroids.',
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
                
                # Embed the uses and classes array in matching JSON objects
                for e in data:
                    if e["number"] == element["number"]:
                        e["uses"] = element_uses
                        e["classes"] = element_classes
                        # if DEBUG:
                        #     print(Fore.GREEN + f"Array: {e}")

                # Write the updated data back to the elements.json file
                with open("elements.json", "w") as f:
                    json.dump(data, f, indent=2)
                break  # Exit the loop if all uses are valid and atomic_number is a non-zero int
            else:
                if DEBUG:
                    print(Fore.RED + f"Rejected: {validated}")
        except ValidationError as e:
            if DEBUG:
                print(Fore.RED + f"Validation error: {e}")





