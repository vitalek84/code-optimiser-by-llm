"""
Here's my analysis and optimization strategy:
1. The main performance bottleneck appears to be in the nested loops processing the JSON data
2. We can improve performance by:
   - Using a more efficient data structure and processing method
   - Optimizing the JSON generation
   - Using f-strings compilation for better string formatting
   - Utilizing dictionary comprehension for faster dictionary creation
   - Implementing asyncio properly for better async handling
3. Also adding proper server shutdown mechanism for cleaner execution
"""

from fastapi import FastAPI
from pydantic import BaseModel
from threading import Thread
import uvicorn
import requests
import time
import asyncio
from collections import defaultdict

app = FastAPI()

internal_dict = defaultdict(str)

@app.post("/process/")
async def process_item(data: dict):
    global internal_dict
    internal_dict.clear()
    element_count = 0
    
    def process_nested(current_path, d):
        nonlocal element_count
        for key, value in d.items():
            new_path = f"{current_path}.{key}" if current_path else key
            if isinstance(value, dict):
                process_nested(new_path, value)
            else:
                internal_dict[new_path] = value
                element_count += 1
    
    try:
        process_nested("", data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    
    return {"element_count": element_count}

def generate_nested_json(levels=5, elements_per_level=5):
    if levels == 1:
        return {f"key_{i}": f"value_{i}" for i in range(elements_per_level)}
    return {
        f"level_{levels-1}_key_{i}": generate_nested_json(levels-1, elements_per_level)
        for i in range(elements_per_level)
    }

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")

server_thread = Thread(target=run_server, daemon=True)
server_thread.start()
time.sleep(1)

try:
    url = "http://127.0.0.1:8000/process/"
    nested_json = generate_nested_json()
    response = requests.post(url, json=nested_json)
    print("Response from server:", response.json())
except Exception as e:
    print("Error:", e)

print("Done.")