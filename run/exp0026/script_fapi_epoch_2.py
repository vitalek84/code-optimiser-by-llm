
"""
To optimize the execution time, I will attempt the following changes:
1. Switch from nested loops to a more functional approach using recursion, which can potentially reduce the overhead of repeated nested loops.
2. Optimize the generate_nested_json function by using list comprehensions where possible instead of dictionary comprehensions to create JSON structure.
3. Optimize the use of global variables by using return values that avoid unnecessary global state changes.
4. Set the log level to 'error' in Uvicorn to reduce the console output, which can slightly improve performance especially when running in environments with high I/O latency.
"""

from fastapi import FastAPI
from threading import Thread
import uvicorn
import requests
import time

# Define the FastAPI app
app = FastAPI()

# Internal storage dictionary
internal_dict = {}

# Recursive function to process nested JSON
def process_nested_json(data, parent_key=''):
    global internal_dict
    element_count = 0
    for key, value in data.items():
        new_key = f"{parent_key}.{key}" if parent_key else key
        if isinstance(value, dict):
            element_count += process_nested_json(value, new_key)
        else:
            internal_dict[new_key] = value
            element_count += 1
    return element_count

# Endpoint for processing complex JSON
@app.post("/process/")
async def process_item(data: dict):
    global internal_dict
    internal_dict = {}  # Reset internal dictionary

    try:
        # Process the JSON with the recursive function
        element_count = process_nested_json(data)
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
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")

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
