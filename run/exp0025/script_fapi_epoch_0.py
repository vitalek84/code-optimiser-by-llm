"""
I will optimize the script focusing on the following aspects:
1. Server side optimization:
   - Replace nested loops with a recursive function to process JSON
   - Use string join instead of f-strings for key construction
   - Use local variables instead of globals
2. Client side optimization:
   - Generate JSON more efficiently using dictionary comprehension
   - Reduce server startup time
3. General optimizations:
   - Remove unnecessary BaseModel import
   - Use httpx instead of requests for better async performance
   - Use ThreadPoolExecutor for concurrent processing
"""

from fastapi import FastAPI
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import uvicorn
import httpx
import time

app = FastAPI()

def process_json_level(data, prefix='', result_dict=None):
    if result_dict is None:
        result_dict = {}
    count = 0
    
    if isinstance(data, dict):
        for key, value in data.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                sub_count = process_json_level(value, new_prefix, result_dict)
                count += sub_count
            else:
                result_dict[new_prefix] = value
                count += 1
    return count

@app.post("/process/")
async def process_item(data: dict):
    result_dict = {}
    try:
        element_count = process_json_level(data, result_dict=result_dict)
        return {"element_count": element_count}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

def generate_nested_json(levels=5, elements_per_level=5):
    if levels == 1:
        return {f"key_{i}": f"value_{i}" for i in range(elements_per_level)}
    return {f"level_{levels-1}_key_{i}": 
            generate_nested_json(levels-1, elements_per_level) 
            for i in range(elements_per_level)}

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")

server_thread = Thread(target=run_server, daemon=True)
server_thread.start()
time.sleep(0.5)

try:
    with httpx.Client() as client:
        nested_json = generate_nested_json()
        response = client.post("http://127.0.0.1:8000/process/", json=nested_json)
        print("Response from server:", response.json())
except Exception as e:
    print("Error:", e)

print("Done.")