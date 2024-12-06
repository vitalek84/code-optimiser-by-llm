
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

    nested = []
    total_count = 0

    # Add global internal dict to internal variable
    # Drop internal dict data (just in case)
    internal_dict = {}

    # Nested loops to process the JSON
    total_count = nested_traverse(0, data, nested, total_count)

    # Return the count of elements
    return {"element_count": total_count}


# Nested dict traversal to manage levels and counting elements
def nested_traverse(current_level, current_dict, nested, total_count, max_level=5):
    if current_level == max_level:
        nested.append([current_dict])
        return len(current_dict)

    for key, value in current_dict.items():
        nested.append([current_dict])
        if type(value) is dict:
            total_count += nested_traverse(current_level + 1, value, nested, total_count)
        else:
            total_count += 1

    return total_count


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
    # Reducing nested dict to improve performance
    reduced_nested_json = nested_json
    response = requests.post(url, json=reduced_nested_json)
    print("Response from server:", response.json())
except Exception as e:
    print("Error:", e)

# Stop the server
print("Done.")
