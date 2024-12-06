
"""
I noticed that the previous version works incorrectly. I analysed the issue and fixed it. The execution time was not reduced since there was an error previously.
Optimisation Plan:
1. Replace the nested loop approach with a recursive function to process the JSON, which should reduce the overhead associated with accessing dictionary keys and should improve the overall processing time.
2. Update the usage of threads to make the code more efficient, using asyncio instead of waiting with time.sleep.
3. Ensure that the data processing logic's recursion base case is equivalent to the nested depth provided by the input data.
4. Verify if the server is available before sending requests.
"""
from fastapi import FastAPI
from threading import Thread
import uvicorn
import requests
import time
import asyncio

# Define the FastAPI app
app = FastAPI()

# Internal storage dictionary
internal_dict = {}

def process_recursive(data, prefix=''):
    global internal_dict
    element_count = 0

    if isinstance(data, dict):
        for key, value in data.items():
            current_prefix = f"{prefix}.{key}" if prefix else key
            elements = process_recursive(value, current_prefix)
            element_count += elements
    else:
        internal_dict[prefix] = data
        element_count = 1

    return element_count

# Endpoint for processing complex JSON
@app.post("/process/")
async def process_item(data: dict):
    global internal_dict
    internal_dict = {}  # Reset internal dictionary

    try:
        # Use recursive function to process the JSON
        element_count = process_recursive(data)
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

# Helper function to check if server is available
async def wait_until_server_is_ready():
    url = "http://127.0.0.1:8000/process/"
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 404:  # Not Found indicates the server is running but endpoint doesn't exist
                break
        except requests.ConnectionError:
            pass  # The server is not yet running
        await asyncio.sleep(0.1)

# Start the server in a separate thread
server_thread = Thread(target=run_server, daemon=True)
server_thread.start()

# Wait asynchronously until the server is ready
async def send_json():
    await wait_until_server_is_ready()
    # Client sends complex JSON to the API
    try:
        url = "http://127.0.0.1:8000/process/"
        nested_json = generate_nested_json()
        response = requests.post(url, json=nested_json)
        print("Response from server:", response.json())
    except Exception as e:
        print("Error:", e)

asyncio.run(send_json())

# Stop the server
print("Done.")
