
"""
The previous code was identical to the base code and showed no improvement in execution time. The reported error in the previous iteration suggests that the code faced an issue on the user's PC.

To optimize, I will attempt to improve the efficiency of the nested loops which process the JSON:

1. Use itertools.product to flatten the nested loops into a single loop, reducing the overhead associated with deeply nested loops.
2. This should ideally reduce computational complexity and improve the time by eliminating the need for multiple nested loops.
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

    try:
        # Flatten the nested loops using itertools.product
        keys = []
        values = [[]]

        for key, value in data.items():
            keys.append(key)
            values.append(value)

        all_combinations = product(*values)
        element_count = 0

        for combination in all_combinations:
            nested_key = '.'.join(keys)
            internal_dict[nested_key] = combination
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
