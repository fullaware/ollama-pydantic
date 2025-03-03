# ollama-pydantic example

# Project Overview

This project includes three Python scripts designed to interact with different data sources and update specific fields in JSON or MongoDB documents. The scripts leverage the Ollama API for data classification and the Pydantic library for data validation.

# Problem
## Asteroids

With a collection of 958524 asteroids, it is important that they have a `class` of either `C` (Carbonaceous),`S` (Silicaceous),`M` (Metallic) or `O` (Other, unclassified).  I used Pydantic and Ollama to read each asteroid name and update it's document with its classification.

## Elements
119 Elements in the periodic table, they each needed to be classified for it's possible uses out of `"fuel", "lifesupport", "energystorage", "construction", "electronics", "coolants", "industrial", "medical", "propulsion", "shielding", "agriculture", "mining"`. I used Pydantic and Ollama to read each element and update it's document with its uses.

## Scripts

### 1. `update_element_uses.py`

This script reads element data from a JSON file, validates the data using Pydantic models, and updates the JSON file with validated uses and classes for each element.

#### Capabilities:
- Reads element data from `elements.json`.
- Uses Pydantic models to validate element data.
- Validates that the `classes` field includes "C", "S", and "M"
- Updates the `uses` and `classes` fields in the JSON file.
- Debugging support with color-coded output using `colorama`.

### 2. `update_element_uses_mdb.py`

This script reads element data from a MongoDB collection, validates the data using Pydantic models, and updates the MongoDB documents with validated uses and classes for each element.

#### Capabilities:
- Connects to a MongoDB database using a URI from environment variables.
- Uses Pydantic models to validate element data.
- Validates that the `classes` field includes "C", "S", and "M"
- Updates the `uses` and `classes` fields in MongoDB documents.
- Debugging support with color-coded output using `colorama`.

### 3. `update_asteroids_classes.py`

This script reads asteroid data from a MongoDB collection, validates the data using Pydantic models, and updates the MongoDB documents with validated classes for each asteroid.

#### Capabilities:
- Connects to a MongoDB database using a URI from environment variables.
- Uses Pydantic models to validate asteroid data.
- Validates that the `class` field is one of "C", "S", or "M".
- Updates the `class` field in MongoDB documents only if it doesn't already exist.
- Debugging support with color-coded output using `colorama`.

## Usage

### Environment Setup

1. Create a `.env` file in the project root directory with the following variables:
    ```env
    OLLAMA_URI=http://localhost:11434
    MONGO_URI=mongodb://localhost:27017
    ```

2. Install the required Python packages:
    ```sh
    pip install pydantic ollama colorama pymongo python-dotenv
    ```

### Running the Scripts

1. **`update_element_uses.py`**:
    ```sh
    python update_element_uses.py
    ```

2. **`update_element_uses_mdb.py`**:
    ```sh
    python update_element_uses_mdb.py
    ```

3. **`update_asteroids_classes.py`**:
    ```sh
    python update_asteroids_classes.py
    ```

## Debugging

- Set `DEBUG = True` in the scripts to enable debug printing with color-coded output.
- Set `OVERWRITE_CLASS = True` in [update_asteroids_classes.py](http://_vscodecontentref_/0) to overwrite existing class fields.

## Notes

- Ensure that the MongoDB server is running and accessible via the URI specified in the [.env](http://_vscodecontentref_/1) file.
- The [elements.json](http://_vscodecontentref_/2) file should be present in the project root directory for [update_element_uses.py](http://_vscodecontentref_/3).

This README provides an overview of the capabilities and usage of the scripts in this project. For more detailed information, refer to the individual script files.
