
"""
I noticed that the previous version works incorrectly. I analyzed the issue and fixed it. 
I understand that I shouldn’t take into account the execution time of the not-working version.
In the initial version, we are using nested loops to parse a complex JSON structure. This is inefficient especially since the structure is fixed at 5 levels.
To optimize execution time, we'll try a recursive approach to flatten JSON.
The use of a single recursive function should reduce call stack overhead and improve efficiency.
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

# Recursive function to process JSON
def process_dict(prefix, d):
    global internal_dict
    element_count = 0
    
    for k, v in d.items():
        new_key = f"{prefix}.{k}"
        if isinstance(v, dict):
            element_count += process_dict(new_key, v)
        else:
            internal_dict[new_key] = v
            element_count += 1
    
    return element_count

# Endpoint for processing complex JSON
@app.post("/process/")
async def process_item(data: dict):
    global internal_dict
    internal_dict = {}  # Reset internal dictionary

    try:
        # Using recursive approach to process the JSON
        element_count = process_dict("", data)
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
