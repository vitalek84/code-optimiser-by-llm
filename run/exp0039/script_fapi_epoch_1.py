"""
For this optimization iteration, I'll focus on several key improvements:
1. Replace string concatenation with a more efficient method using join
2. Use dictionary comprehension instead of nested loops
3. Optimize the JSON generation using a more efficient approach
4. Reduce server startup overhead by using a lower log level
5. Replace global dictionary with a local one since it's reset on each request
6. Use httpx instead of requests for better async performance
"""

from fastapi import FastAPI
from pydantic import BaseModel
from threading import Thread
import uvicorn
import httpx
import time
from functools import reduce

app = FastAPI()

@app.post("/process/")
async def process_item(data: dict):
    element_count = 0
    internal_dict = {}

    try:
        def process_nested(d, prefix=()):
            nonlocal element_count
            for key, value in d.items():
                if isinstance(value, dict):
                    process_nested(value, prefix + (key,))
                else:
                    internal_dict['.'.join(prefix + (key,))] = value
                    element_count += 1

        process_nested(data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

    return {"element_count": element_count}

def generate_nested_json(levels=5, elements_per_level=5):
    def create_level(depth):
        return {
            f"level_{depth}_key_{i}" if depth else f"key_{i}": 
            create_level(depth - 1) if depth else f"value_{i}"
            for i in range(elements_per_level)
        }
    return create_level(levels - 1)

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="critical")

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