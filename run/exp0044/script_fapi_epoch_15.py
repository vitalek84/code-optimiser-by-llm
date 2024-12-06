
"""
I noticed that the previous version works incorrectly. I analysed the issue and fixed it. Also I understand that I shouldn’t take into account execution time of not working version.

In this iteration, I'll focus on optimizing the JSON processing part. Instead of using multiple nested loops, I'll use a single loop with recursion to traverse the dictionary. This should reduce the overhead of nested loops and improve performance.
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

def recursive_process(data, keys=(), element_count=0):
    if isinstance(data, dict):
        for key, value in data.items():
            element_count += recursive_process(value, keys + (key,), element_count)
    elif isinstance(data, list):
        for item in data:
            element_count += recursive_process(item, keys, element_count)
    else:
        internal_dict['.'.join(keys)] = data
        element_count += 1
    return element_count

# Endpoint for processing complex JSON
@app.post("/process/")
async def process_item(data: dict):
    global internal_dict
    internal_dict = {}  # Reset internal dictionary
    element_count = recursive_process(data)
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
