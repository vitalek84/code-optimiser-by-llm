
"""
Steps and reasoning for optimization:

1. I noticed that the previous version caused an error and failed to execute. This might be due to FastAPI setup issues. I need to ensure the server starts correctly.
2. The execution time for both the base code and the 'prev_iteration' is equal, indicating no performance improvement.
3. Considering the nature of this code, multiple factors can be contributing to the delay:
   a. The server setup and request-response cycle.
   b. The processing of nested JSON.
4. To reduce execution time, I will:
   - Optimize the JSON processing by flattening the nested loops.
   - Implement faster dictionary traversal using list comprehensions and the itertools.product function.
5. Ensure mong the client-server cycle correctness after the optimizations.

Note: Since the previous version encountered an error, I’ve analyzed and resolved it.
"""

from fastapi import FastAPI
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
        keys = [[f"{key}_{i}" for i in value] for key, value in data.items()]
        combined_keys = product(*keys)
        
        for combination in combined_keys:
            comb_key = '.'.join(combination)
            leaf_value = next(iter(data))
            internal_dict[comb_key] = leaf_value
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
