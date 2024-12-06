"""
Let's optimize the code with the following improvements:
1. Use aiohttp for asynchronous HTTP requests instead of synchronous requests
2. Replace string concatenation with a more efficient join method
3. Use a more efficient dictionary comprehension for JSON generation
4. Reduce server startup time by decreasing sleep duration
5. Add connection pooling for better HTTP performance
6. Use asyncio for better async/await pattern support
"""

from fastapi import FastAPI
from threading import Thread
import uvicorn
import aiohttp
import asyncio
import time
from typing import Dict

app = FastAPI()
internal_dict: Dict[str, str] = {}

@app.post("/process/")
async def process_item(data: dict):
    global internal_dict
    internal_dict = {}
    element_count = 0
    
    try:
        stack = [([], key, value) for key, value in data.items()]
        while stack:
            path, key, value = stack.pop()
            if isinstance(value, dict):
                path.append(key)
                stack.extend((path[:], k, v) for k, v in value.items())
            else:
                internal_dict['.'.join(path + [key])] = value
                element_count += 1
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    
    return {"element_count": element_count}

def generate_nested_json(levels=5, elements_per_level=5):
    def create_level(depth):
        return {f"key_{i}": f"value_{i}" for i in range(elements_per_level)} if depth == 0 else \
               {f"level_{depth}_key_{i}": create_level(depth - 1) for i in range(elements_per_level)}
    return create_level(levels - 1)

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")

async def main():
    server_thread = Thread(target=run_server, daemon=True)
    server_thread.start()
    await asyncio.sleep(0.5)
    
    try:
        async with aiohttp.ClientSession() as session:
            url = "http://127.0.0.1:8000/process/"
            nested_json = generate_nested_json()
            async with session.post(url, json=nested_json) as response:
                result = await response.json()
                print("Response from server:", result)
    except Exception as e:
        print("Error:", e)
    print("Done.")

if __name__ == "__main__":
    asyncio.run(main())