
"""
I noticed the previous code execution time was slow due to deeply nested loops handling JSON.
To optimize, I will pre-compute the keys at each level to minimize Python loop overhead.
Using itertools.product will help flatten the iteration process and improve execution efficiency.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from threading import Thread
import uvicorn
import requests
import time
from itertools import product

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
        # Pre-compute keys using itertools.product to minimize nested loops overhead
        level_keys = [list(level.keys()) for level in [data, *data.values(), *data.get(list(data.keys())[0], {}).values(),
                                                       *data.get(list(data.keys())[0], {}).get(list(data.get(list(data.keys())[0], {})), {}).values(),
                                                       *data.get(list(data.keys())[0], {}).get(list(data.get(list(data.keys())[0], {})), {})
                                                       .get(list(data.get(list(data.keys())[0], {}).get(list(data.get(list(data.keys())[0], {})), {})), {}).values()]]
        for keys_tuple in product(*level_keys):
            level1_key, level2_key, level3_key, level4_key, level5_key = keys_tuple
            # Store data in the internal dictionary
            internal_dict[f"{level1_key}.{level2_key}.{level3_key}.{level4_key}.{level5_key}"] = \
                data[level1_key][level2_key][level3_key][level4_key][level5_key]
            element_count += 1

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
