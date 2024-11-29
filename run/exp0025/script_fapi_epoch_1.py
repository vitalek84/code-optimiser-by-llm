"""
I will try to optimize this script with the following approaches:
1. Replace the nested loop structure with recursion to process JSON more efficiently
2. Use a more efficient string concatenation method for dictionary keys
3. Use aiohttp instead of requests for async HTTP client
4. Optimize the JSON generation process using list comprehension
5. Remove global dictionary since it's not used outside the endpoint
6. Use faster ASGI server (hypercorn) instead of uvicorn
7. Reduce server startup time
"""

from fastapi import FastAPI
import hypercorn.asyncio
from threading import Thread
import aiohttp
import asyncio
import time
from functools import reduce

app = FastAPI()

@app.post("/process/")
async def process_item(data: dict):
    element_count = [0]
    
    def process_dict(d, path=""):
        for key, value in d.items():
            current_path = f"{path}.{key}" if path else key
            if isinstance(value, dict):
                process_dict(value, current_path)
            else:
                element_count[0] += 1
    
    try:
        process_dict(data)
        return {"element_count": element_count[0]}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

def generate_nested_json(levels=5, elements_per_level=5):
    return reduce(lambda acc, _: {
        f"level_{levels-1}_key_{i}": acc if levels > 1 else f"value_{i}"
        for i in range(elements_per_level)
    }, range(levels-1), {f"key_{i}": f"value_{i}" for i in range(elements_per_level)})

async def make_request():
    async with aiohttp.ClientSession() as session:
        url = "http://127.0.0.1:8000/process/"
        nested_json = generate_nested_json()
        async with session.post(url, json=nested_json) as response:
            print("Response from server:", await response.json())

def run_server():
    asyncio.run(hypercorn.asyncio.serve(app, hypercorn.Config()))

server_thread = Thread(target=run_server, daemon=True)
server_thread.start()
time.sleep(0.5)

asyncio.run(make_request())
print("Done.")