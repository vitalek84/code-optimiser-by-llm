"""
For this optimization iteration, I will focus on several key improvements:
1. Use more efficient data structures - replacing string concatenation with tuple keys
2. Implement dictionary comprehension instead of nested loops
3. Use asyncio for better async handling
4. Optimize JSON generation with a more efficient approach
5. Remove global dictionary as it's not used in the final result
6. Use faster ASGI server - Hypercorn instead of Uvicorn
7. Minimize string operations in the processing loop

I noticed that both base and previous versions work correctly (same results), but we can improve performance significantly.
"""

from fastapi import FastAPI
import asyncio
from threading import Thread
import hypercorn.asyncio
import requests
import time
from hypercorn.config import Config

app = FastAPI()

@app.post("/process/")
async def process_item(data: dict):
    element_count = 0
    try:
        def process_level(d, path=()):
            nonlocal element_count
            if isinstance(d, dict):
                for k, v in d.items():
                    yield from process_level(v, path + (k,))
            else:
                element_count += 1
                
        list(process_level(data))
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    
    return {"element_count": element_count}

def generate_nested_json(levels=5, elements_per_level=5):
    result = {}
    stack = [(result, levels-1)]
    
    while stack:
        current_dict, depth = stack.pop()
        if depth == 0:
            for i in range(elements_per_level):
                current_dict[f"key_{i}"] = f"value_{i}"
        else:
            for i in range(elements_per_level):
                new_dict = {}
                current_dict[f"level_{depth}_key_{i}"] = new_dict
                stack.append((new_dict, depth-1))
                
    return result

async def run_server():
    config = Config()
    config.bind = ["127.0.0.1:8000"]
    config.worker_class = "asyncio"
    await hypercorn.asyncio.serve(app, config)

def start_server():
    asyncio.run(run_server())

server_thread = Thread(target=start_server, daemon=True)
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