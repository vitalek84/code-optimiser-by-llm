"""
Optimization strategy for this iteration:
1. Replace string concatenation with a more efficient approach using join
2. Use asyncio.sleep instead of time.sleep for better async performance
3. Implement connection pooling in requests using Session
4. Use a more efficient data structure for counting
5. Implement dictionary comprehension for faster JSON generation
6. Use uvicorn with minimal settings and workers=1 for testing purposes
7. Remove global dictionary as it's not used in the final result
8. Use f-strings for string formatting
"""

from fastapi import FastAPI
import uvicorn
from threading import Thread
import asyncio
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from collections import Counter

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

def run_server():
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="critical", loop="asyncio")
    server = uvicorn.Server(config)
    server.run()

server_thread = Thread(target=run_server, daemon=True)
server_thread.start()

async def main():
    await asyncio.sleep(0.5)
    session = requests.Session()
    retry_strategy = Retry(total=3, backoff_factor=0.1)
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    
    try:
        nested_json = generate_nested_json()
        response = session.post("http://127.0.0.1:8000/process/", json=nested_json)
        print("Response from server:", response.json())
    except Exception as e:
        print("Error:", e)
    finally:
        session.close()
    print("Done.")

asyncio.run(main())