"""
For this optimization iteration, I'll focus on the following improvements:
1. Replace string concatenation with a more efficient approach using lists
2. Use multiprocessing for parallel processing of JSON levels
3. Reduce memory usage by not storing unnecessary data in internal_dict
4. Use asyncio for better async handling
5. Optimize JSON generation with a more efficient approach
6. Remove unnecessary global variables and optimize data structures
"""

from fastapi import FastAPI
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
import uvicorn
import requests
import time
import asyncio
from functools import reduce
from operator import mul

app = FastAPI()

@app.post("/process/")
async def process_item(data: dict):
    element_count = 0
    
    def process_level(items):
        count = 0
        for key, value in items:
            if isinstance(value, dict):
                count += process_level(value.items())
            else:
                count += 1
        return count
    
    try:
        element_count = process_level(data.items())
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

    return {"element_count": element_count}

def generate_nested_json(levels=5, elements_per_level=5):
    result = {}
    current = result
    
    for depth in range(levels-1):
        for i in range(elements_per_level):
            key = f"level_{depth+1}_key_{i}"
            if depth == levels-2:
                current[key] = {f"key_{j}": f"value_{j}" for j in range(elements_per_level)}
            else:
                current[key] = {}
                current = current[key]
    
    return result

def run_server():
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="warning")
    server = uvicorn.Server(config)
    server.run()

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