"""
I noticed that the results of the reference version and my previous version are different. The issue seems to be with server initialization timing. 
Here's my optimization strategy:
1. Reduce server startup time by using a more lightweight ASGI server (hypercorn)
2. Use asyncio for better concurrency
3. Implement a more efficient JSON processing using recursion instead of nested loops
4. Add proper server startup check
5. Use string joining for key creation instead of f-strings
6. Use a connection retry mechanism
"""

from hypercorn.asyncio import serve
from hypercorn.config import Config
from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
import aiohttp
import time

app = FastAPI()
internal_dict = {}

@app.post("/process/")
async def process_item(data: dict):
    global internal_dict
    internal_dict = {}
    element_count = 0
    
    def process_nested(current_dict, prefix=''):
        nonlocal element_count
        for key, value in current_dict.items():
            if isinstance(value, dict):
                process_nested(value, prefix + key + '.' if prefix else key + '.')
            else:
                internal_dict[prefix + key] = value
                element_count += 1
    
    try:
        process_nested(data)
        return {"element_count": element_count}
    except Exception as e:
        return {"error": str(e)}

def generate_nested_json(levels=5, elements_per_level=5):
    def create_level(depth):
        if depth == 0:
            return {f"key_{i}": f"value_{i}" for i in range(elements_per_level)}
        return {f"level_{depth}_key_{i}": create_level(depth - 1) for i in range(elements_per_level)}
    return create_level(levels - 1)

async def wait_for_server(url, timeout=5, max_retries=5):
    async with aiohttp.ClientSession() as session:
        for _ in range(max_retries):
            try:
                async with session.get(f"{url}/docs") as response:
                    if response.status == 200:
                        return True
            except:
                await asyncio.sleep(0.2)
        return False

async def main():
    config = Config()
    config.bind = ["127.0.0.1:8000"]
    config.worker_class = "asyncio"
    server = serve(app, config)
    
    server_task = asyncio.create_task(server)
    
    if not await wait_for_server("http://127.0.0.1:8000"):
        print("Server failed to start")
        return
    
    async with aiohttp.ClientSession() as session:
        url = "http://127.0.0.1:8000/process/"
        nested_json = generate_nested_json()
        async with session.post(url, json=nested_json) as response:
            print("Response from server:", await response.json())
    
    print("Done.")
    await asyncio.sleep(0.1)
    server_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())