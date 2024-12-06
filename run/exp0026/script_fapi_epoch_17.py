
"""
I noticed that the previous version works incorrectly because it produced an unexpected error when processing the JSON data. The error seems to relate to the way keys are being accessed in the nested dictionary. The previous execution time is therefore not meaningful and should not be considered. I have analyzed the issue, suspecting recursive access/pipeline, and tried to fix it by flattening the JSON structure in one go using a single function to avoid the nested loops. Additionally, I've ensured correctness and consistency with the reference results by correcting the JSON processing logic.
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

# Recursive function to flatten JSON in a single pass
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for key in x:
                flatten(x[key], name + key + '.')
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

# Endpoint for processing complex JSON
@app.post("/process/")
async def process_item(data: dict):
    global internal_dict
    internal_dict = {}  # Reset internal dictionary

    try:
        # Flatten the JSON and get the element count
        internal_dict = flatten_json(data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

    # Return the count of elements
    return {"element_count": len(internal_dict)}


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
