"""
For this iteration, I will try several optimization approaches:
1. Use concurrent.futures for parallel processing of the nested dictionary
2. Replace string concatenation with a more efficient join method
3. Use a counter variable instead of incrementing element_count
4. Optimize the JSON generation using list comprehension and dictionary comprehension
5. Remove global dictionary as it's not used in the output
6. Use httpx instead of requests for better async performance
7. Implement connection pooling in httpx
8. Use FastAPI's background tasks instead of explicit threading
"""

from fastapi import FastAPI, BackgroundTasks
from concurrent.futures import ThreadPoolExecutor
import uvicorn
import httpx
import time
from functools import partial

app = FastAPI()

@app.post("/process/")
async def process_item(data: dict):
    element_count = 0
    
    def process_level5(items):
        nonlocal element_count
        for _ in items:
            element_count += 1
    
    with ThreadPoolExecutor() as executor:
        for level1_value in data.values():
            for level2_value in level1_value.values():
                for level3_value in level2_value.values():
                    for level4_value in level3_value.values():
                        executor.submit(process_level5, level4_value.items())
    
    return {"element_count": element_count}

def generate_nested_json(levels=5, elements_per_level=5):
    return {
        f"level_4_key_{i}": {
            f"level_3_key_{j}": {
                f"level_2_key_{k}": {
                    f"level_1_key_{l}": {
                        f"key_{m}": f"value_{m}"
                        for m in range(elements_per_level)
                    }
                    for l in range(elements_per_level)
                }
                for k in range(elements_per_level)
            }
            for j in range(elements_per_level)
        }
        for i in range(elements_per_level)
    }

async def startup_server():
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="warning")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    background_tasks = BackgroundTasks()
    background_tasks.add_task(startup_server)
    
    # Allow some time for the server to start
    time.sleep(1)
    
    async with httpx.AsyncClient() as client:
        try:
            nested_json = generate_nested_json()
            response = await client.post("http://127.0.0.1:8000/process/", json=nested_json)
            print("Response from server:", response.json())
        except Exception as e:
            print("Error:", e)
    
    print("Done.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())