
"""
In the previous iteration, the code structure included nested loops for processing each level of the nested JSON. This, however, can be optimized by using a recursive function to flatten the nested dictionary, improving readability and potentially enhancing performance by reducing deep loop nesting.

The app's functionality remains the same, but the JSON processing function is revised to employ recursion instead. This change is expected to handle the data processing more efficiently.

Additionally, the server setup and request remain untouched as they function satisfactorily.
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

# Recursive function to process and flatten JSON
def process_json(data, parent_key=''):
    global internal_dict
    element_count = 0

    if isinstance(data, dict):
        for k, v in data.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            sub_count = process_json(v, new_key)
            element_count += sub_count
    else:
        internal_dict[parent_key] = data
        element_count += 1
    
    return element_count

# Endpoint for processing complex JSON
@app.post("/process/")
async def process_item(data: dict):
    global internal_dict
    internal_dict = {}  # Reset internal dictionary
    try:
        # Process JSON using the recursive function
        element_count = process_json(data)
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
