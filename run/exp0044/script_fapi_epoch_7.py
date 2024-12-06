
"""
Chain of thought:
- The previous version had an issue where the `element_count` variable was accessed outside its scope, leading to an error. This has been fixed by properly returning the result from the FastAPI endpoint.
- To further optimize execution time, we can reduce the overhead of nested loops and string concatenation in the internal dictionary storage. We will use a more efficient data structure like defaultdict from collections.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from threading import Thread
import uvicorn
import requests
import time
from collections import defaultdict

# Define the FastAPI app
app = FastAPI()

# Internal storage dictionary
internal_dict = defaultdict(dict)

# Endpoint for processing complex JSON
@app.post("/process/")
async def process_item(data: dict):
    global internal_dict
    internal_dict.clear()  # Reset internal dictionary
    element_count = 0

    try:
        # Nested loops to process the JSON
        for level1_key, level1_value in data.items():
            for level2_key, level2_value in level1_value.items():
                for level3_key, level3_value in level2_value.items():
                    for level4_key, level4_value in level3_value.items():
                        for level5_key, level5_value in level4_value.items():
                            # Store data in the internal dictionary
                            internal_dict[level1_key][level2_key][level3_key][level4_key][level5_key] = level5_value
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
