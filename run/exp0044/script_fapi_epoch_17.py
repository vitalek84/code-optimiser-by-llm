
"""
Chain of thought:
1. The previous version had an execution time of 1,335,036 microseconds and returned the correct results.
2. There was no error in the previous iteration, but I noticed that the nested loops were deeply nested and could potentially be optimized.
3. To optimize the nested loops, I will use a more efficient data structure to store the elements and avoid the deep nesting of loops.
4. I will also use the `json` library to generate the complex JSON instead of the custom function to ensure consistency and potential performance improvements.
5. Finally, I will add some logging to understand if there are any issues during execution.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from threading import Thread
import uvicorn
import requests
import time
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

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
        # Flatten the nested JSON using a stack-based approach
        stack = [(key, value) for key, value in data.items()]
        while stack:
            level_key, level_value = stack.pop(0)
            if isinstance(level_value, dict):
                stack.extend([(f"{level_key}.{sub_key}", sub_value) for sub_key, sub_value in level_value.items()])
            else:
                internal_dict[level_key] = level_value
                element_count += 1
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
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

    return json.dumps(create_level(levels - 1))


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
    response = requests.post(url, json=json.loads(nested_json))
    print("Response from server:", response.json())
except Exception as e:
    logging.error(f"Error during client request: {str(e)}")
    print("Error:", e)

# Stop the server
print("Done.")
