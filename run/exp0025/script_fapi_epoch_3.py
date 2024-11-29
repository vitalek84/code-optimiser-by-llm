"""
I will attempt to optimize this code by:
1. Using a more efficient data structure for storing the nested dictionary paths
2. Implementing concurrent processing using asyncio for better performance
3. Using a faster JSON serialization library (orjson)
4. Optimizing the nested JSON generation with a more efficient approach
5. Reducing the startup time by using a more lightweight server configuration
6. Using string concatenation instead of f-strings for path generation
"""

from fastapi import FastAPI
import asyncio
import orjson
from threading import Thread
import uvicorn
import httpx
import time

app = FastAPI()

# Internal storage dictionary
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
                new_prefix = prefix + str(key) + '.' if prefix else str(key) + '.'
                process_nested(value, new_prefix)
            else:
                internal_dict[prefix + str(key)] = value
                element_count += 1
    
    try:
        process_nested(data)
    except Exception as e:
        return {"error": str(e)}
    
    return {"element_count": element_count}

def generate_nested_json(levels=5, elements_per_level=5):
    result = {}
    stack = [(result, levels - 1)]
    
    while stack:
        current_dict, depth = stack.pop()
        for i in range(elements_per_level):
            if depth == 0:
                current_dict[f"key_{i}"] = f"value_{i}"
            else:
                new_dict = {}
                current_dict[f"level_{depth}_key_{i}"] = new_dict
                stack.append((new_dict, depth - 1))
    
    return result

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="critical", workers=1)

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