
"""
To optimize the execution time, I propose the following improvements:
1. Use FastAPI's background tasks instead of a global dictionary to avoid memory issues
2. Use string concatenation instead of f-strings for key generation which can be faster
3. Replace nested loops with a recursive function for better memory usage and potentially faster execution
4. Use asyncio for the client request to avoid blocking operations
5. Use httpx instead of requests for better async support
6. Reduce server startup time by using a more efficient configuration
7. Implement dictionary comprehension for faster JSON generation
"""

from fastapi import FastAPI, BackgroundTasks
import uvicorn
from threading import Thread
import asyncio
import httpx
import time

app = FastAPI()

async def process_level(data, prefix="", count=0):
    result = {}
    if isinstance(data, dict):
        for key, value in data.items():
            new_prefix = prefix + "." + key if prefix else key
            if isinstance(value, dict):
                sub_result, sub_count = await process_level(value, new_prefix, count)
                result.update(sub_result)
                count = sub_count
            else:
                result[new_prefix] = value
                count += 1
    return result, count

@app.post("/process/")
async def process_item(data: dict, background_tasks: BackgroundTasks):
    try:
        result, count = await process_level(data)
        background_tasks.add_task(lambda: result.clear())
        return {"element_count": count}
    except Exception as e:
        return {"error": str(e)}

def generate_nested_json(levels=5, elements_per_level=5):
    def create_level(depth):
        if depth == 0:
            return {f"key_{i}": f"value_{i}" for i in range(elements_per_level)}
        return {f"level_{depth}_key_{i}": create_level(depth - 1) 
                for i in range(elements_per_level)}
    return create_level(levels - 1)

def run_server():
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="critical")
    server = uvicorn.Server(config)
    server.run()

async def main():
    server_thread = Thread(target=run_server, daemon=True)
    server_thread.start()
    await asyncio.sleep(0.5)
    
    try:
        async with httpx.AsyncClient() as client:
            nested_json = generate_nested_json()
            response = await client.post("http://127.0.0.1:8000/process/", json=nested_json)
            print("Response from server:", response.json())
    except Exception as e:
        print("Error:", e)
    print("Done.")

if __name__ == "__main__":
    asyncio.run(main())
