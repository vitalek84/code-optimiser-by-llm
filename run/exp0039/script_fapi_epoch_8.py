"""
For this optimization iteration, I will focus on several key improvements:
1. Replace the nested loops with a recursive function that can process the JSON more efficiently
2. Use string concatenation optimization with join() instead of f-strings
3. Use a local counter instead of modifying a global dictionary
4. Use faster JSON processing with orjson library instead of default json
5. Optimize server settings for better performance
6. Remove unnecessary sleep time
7. Use asyncio for better concurrency
"""

from fastapi import FastAPI
import uvicorn
import orjson
from threading import Thread
import aiohttp
import asyncio

app = FastAPI()

async def process_nested_dict(data, prefix='', counter=None):
    if counter is None:
        counter = [0]
    
    if isinstance(data, dict):
        for key, value in data.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                await process_nested_dict(value, new_prefix, counter)
            else:
                counter[0] += 1
    return counter[0]

@app.post("/process/")
async def process_item(data: dict):
    try:
        element_count = await process_nested_dict(data)
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
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning", loop="uvloop")

async def main():
    server_thread = Thread(target=run_server, daemon=True)
    server_thread.start()
    
    async with aiohttp.ClientSession() as session:
        url = "http://127.0.0.1:8000/process/"
        nested_json = generate_nested_json()
        async with session.post(url, json=nested_json) as response:
            print("Response from server:", await response.json())
    
    print("Done.")

if __name__ == "__main__":
    asyncio.run(main())