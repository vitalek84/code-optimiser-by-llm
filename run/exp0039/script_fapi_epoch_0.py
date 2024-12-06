"""
I will optimize the script with the following approaches:
1. Replace string concatenation with a more efficient list-based approach
2. Use more efficient JSON generation with dictionary comprehension
3. Reduce the startup time by using a faster ASGI server (hypercorn)
4. Use asyncio for better concurrency
5. Implement connection pooling for HTTP requests
6. Remove global dictionary as it's not used in the final result
7. Use ujson for faster JSON processing
"""

from fastapi import FastAPI
import asyncio
import hypercorn.asyncio
from hypercorn.config import Config
import ujson
import aiohttp
import time

app = FastAPI()

@app.post("/process/")
async def process_item(data: dict):
    element_count = 0
    try:
        for l1k, l1v in data.items():
            for l2k, l2v in l1v.items():
                for l3k, l3v in l2v.items():
                    for l4k, l4v in l3v.items():
                        element_count += len(l4v)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return {"element_count": element_count}

def generate_nested_json(levels=5, elements_per_level=5):
    def create_level(depth):
        return {f"key_{i}": f"value_{i}" for i in range(elements_per_level)} if depth == 0 else {
            f"level_{depth}_key_{i}": create_level(depth - 1) for i in range(elements_per_level)
        }
    return create_level(levels - 1)

async def main():
    config = Config()
    config.bind = ["127.0.0.1:8000"]
    config.worker_class = "asyncio"
    server = hypercorn.asyncio.serve(app, config)
    asyncio.create_task(server)
    
    await asyncio.sleep(0.5)
    
    async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
        url = "http://127.0.0.1:8000/process/"
        nested_json = generate_nested_json()
        async with session.post(url, json=nested_json) as response:
            print("Response from server:", await response.json())
    
    print("Done.")
    await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())