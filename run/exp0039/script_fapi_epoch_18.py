"""
This is my first iteration to optimize the code. Here's my thought process:

1. The main performance bottleneck appears to be in the nested loops processing the JSON data.
2. Instead of using multiple nested loops, we can use a recursive function to process the nested dictionary.
3. We'll use f-strings for string formatting as they are faster than string concatenation.
4. We'll use an optimized dictionary traversal method.
5. We'll minimize the global variable usage and optimize the data structure.
6. We'll use asyncio for better performance in the FastAPI endpoint.
7. We'll reduce the server startup time by using a smaller sleep duration.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from threading import Thread
import uvicorn
import requests
import time
import asyncio

app = FastAPI()

internal_dict = {}

def process_nested_dict(data, prefix='', result_dict=None):
    count = 0
    if result_dict is None:
        result_dict = {}
    
    if isinstance(data, dict):
        for key, value in data.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                sub_count = process_nested_dict(value, new_prefix, result_dict)
                count += sub_count
            else:
                result_dict[new_prefix] = value
                count += 1
    return count

@app.post("/process/")
async def process_item(data: dict):
    global internal_dict
    internal_dict = {}
    
    try:
        element_count = process_nested_dict(data, result_dict=internal_dict)
        return {"element_count": element_count}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

def generate_nested_json(levels=5, elements_per_level=5):
    def create_level(depth):
        if depth == 0:
            return {f"key_{i}": f"value_{i}" for i in range(elements_per_level)}
        return {f"level_{depth}_key_{i}": create_level(depth - 1) for i in range(elements_per_level)}
    
    return create_level(levels - 1)

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")

server_thread = Thread(target=run_server, daemon=True)
server_thread.start()

time.sleep(0.5)

try:
    url = "http://127.0.0.1:8000/process/"
    nested_json = generate_nested_json()
    response = requests.post(url, json=nested_json)
    print("Response from server:", response.json())
except Exception as e:
    print("Error:", e)

print("Done.")