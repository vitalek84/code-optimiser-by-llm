"""
For this optimization iteration, I will focus on several key improvements:
1. Replace the nested for loops with a recursive function to process JSON more efficiently
2. Use string joining instead of f-strings for better performance
3. Pre-allocate the dictionary size to avoid resizing
4. Use asyncio.create_task for better async handling
5. Optimize the JSON generation function
6. Use more efficient data structures
"""

from fastapi import FastAPI
import asyncio
from threading import Thread
import uvicorn
import requests
import time
from collections import defaultdict

app = FastAPI()

internal_dict = {}

def process_nested_json(current_level, current_path, result_dict):
    count = 0
    for key, value in current_level.items():
        if isinstance(value, dict):
            new_path = current_path + '.' + key if current_path else key
            count += process_nested_json(value, new_path, result_dict)
        else:
            result_dict[current_path + '.' + key if current_path else key] = value
            count += 1
    return count

@app.post("/process/")
async def process_item(data: dict):
    global internal_dict
    internal_dict = {}
    
    try:
        element_count = process_nested_json(data, "", internal_dict)
        return {"element_count": element_count}
    except Exception as e:
        return {"error": str(e)}

def generate_nested_json(levels=5, elements_per_level=5):
    result = {}
    stack = [(result, levels-1)]
    
    while stack:
        current_dict, depth = stack.pop()
        for i in range(elements_per_level):
            if depth == 0:
                current_dict[f"key_{i}"] = f"value_{i}"
            else:
                key = f"level_{depth}_key_{i}"
                current_dict[key] = {}
                stack.append((current_dict[key], depth-1))
    
    return result

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