
"""
Chain of thought:
1. The current implementation uses nested loops to process the JSON data, which can be optimized using a recursive approach.
2. By using a generator function, we can avoid storing all elements in memory at once, reducing memory usage and potentially speeding up the processing.
3. The use of `Thread` for running the server is not necessary if we don't need to keep the script running after the client request is processed.
4. Removing unnecessary imports and optimizing the JSON generation process can further reduce execution time.
"""

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import requests

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
        # Recursive function to flatten the JSON and count elements
        def flatten_json(d, parent_key='', sep='.'):
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict):
                    yield from flatten_json(v, new_key, sep=sep)
                else:
                    internal_dict[new_key] = v
                    yield 1

        element_count = sum(flatten_json(data))
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

# Start the server
run_server()

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
