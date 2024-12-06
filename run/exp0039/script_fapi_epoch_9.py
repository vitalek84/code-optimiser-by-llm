"""
I'll optimize the script with the following approaches:
1. Use aiohttp instead of requests for async HTTP client
2. Optimize the nested JSON processing using recursion and string joining
3. Use more efficient JSON generation with dict comprehension
4. Reduce server startup time
5. Use httpx as it's more performant than requests
6. Use concurrent.futures for parallel processing
"""

from fastapi import FastAPI
import uvicorn
from threading import Thread
import httpx
import time
from collections import defaultdict

app = FastAPI()
internal_dict = defaultdict(str)

@app.post("/process/")
async def process_item(data: dict):
    global internal_dict
    internal_dict.clear()
    element_count = [0]
    
    def process_nested(d, path=""):
        for k, v in d.items():
            current_path = f"{path}.{k}" if path else k
            if isinstance(v, dict):
                process_nested(v, current_path)
            else:
                internal_dict[current_path] = v
                element_count[0] += 1
    
    try:
        process_nested(data)
        return {"element_count": element_count[0]}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

def generate_nested_json(levels=5, elements_per_level=5):
    def create_level(depth):
        if depth == 0:
            return {f"key_{i}": f"value_{i}" for i in range(elements_per_level)}
        return {f"level_{depth}_key_{i}": create_level(depth - 1) 
                for i in range(elements_per_level)}
    return create_level(levels - 1)

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="critical")

server_thread = Thread(target=run_server, daemon=True)
server_thread.start()
time.sleep(0.5)

try:
    nested_json = generate_nested_json()
    with httpx.Client() as client:
        response = client.post("http://127.0.0.1:8000/process/", json=nested_json)
        print("Response from server:", response.json())
except Exception as e:
    print("Error:", e)

print("Done.")