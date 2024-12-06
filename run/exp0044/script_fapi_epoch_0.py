
"""
This version optimizes the nested loops used to process the JSON data. 
By flattening the dictionary keys using a recursive function, we can reduce 
the complexity of accessing and storing elements in the internal dictionary.

Additionally, I added type hints for better performance and readability.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from threading import Thread
import uvicorn
import requests
import time

# Define the FastAPI app
app = FastAPI()

# Internal storage dictionary
internal_dict = {}

# Endpoint for processing complex JSON
@app.post("/process/")
async def process_item(data: dict):
    global internal_dict
    internal_dict = {}  # Reset internal dictionary
    element_count = 0

    try:
        # Helper function to flatten the nested dictionary
        def flatten(d, parent_key='', sep='.'):
            items = {}
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict):
                    items.update(flatten(v, new_key, sep=sep))
                else:
                    internal_dict[new_key] = v
                    element_count += 1
            return items

        # Flatten the JSON data and store in the internal dictionary
        flatten(data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

    # Return the count of elements
    return {"element_count": element_count}

# Function to generate a complex nested JSON
def generate_nested_json(levels=5, elements_per_level=5):
    def create_level(depth):
        if depth == 0:
            return {f"key_{i}": f"value_{i}" for i in range(elements_per_level)}
        else:
            return {f"level_{depth}_key_{i}": create_level(depth - 1) for i in range(elements_per_level)}

    return create_level(levels - 1)

# Function to run the FastAPI server
def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")

# Start the server in a separate thread
server_thread = Thread(target=run_server, daemon=True)
server_thread.start()

# Allow some time for the server to start
time.sleep(1)

# Client sends complex JSON to the API
try:
    url = "http://127.0.0.1:8000/process/"
    nested_json = generate_nested_json()
    response = requests.post(url, json=nested_json)
    print("Response from server:", response.json())
except Exception as e:
    print("Error:", e)

# Stop the server
print("Done.")
