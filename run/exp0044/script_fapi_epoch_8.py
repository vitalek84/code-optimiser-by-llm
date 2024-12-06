
"""
This version optimizes the processing of nested JSON by avoiding unnecessary dictionary resets and reducing the number of string concatenations during key formation. 
It also uses a more efficient approach to traverse and count elements in the JSON structure.
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
    # Reset internal dictionary if needed
    internal_dict.clear()
    
    element_count = 0

    try:
        # Helper function to traverse and count elements
        def traverse_and_count(d, path=""):
            nonlocal element_count
            for key, value in d.items():
                new_path = f"{path}.{key}" if path else key
                if isinstance(value, dict):
                    traverse_and_count(value, new_path)
                else:
                    internal_dict[new_path] = value
                    element_count += 1

        # Start traversal from the root
        traverse_and_count(data)

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
