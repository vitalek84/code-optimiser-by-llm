"""
For this iteration, I will try several optimizations:
1. Replace string concatenation with a more efficient approach using lists and join
2. Use a more efficient dictionary comprehension for the base level
3. Replace recursive function with iterative approach for JSON generation
4. Remove global dictionary as it's not used outside the function
5. Use asyncio for better performance in async context
6. Add connection pooling for requests using httpx
7. Optimize the server startup by removing unnecessary sleep
"""

from fastapi import FastAPI
import uvicorn
from threading import Thread
import httpx
import asyncio
from collections import defaultdict

app = FastAPI()

@app.post("/process/")
async def process_item(data: dict):
    element_count = 0
    try:
        for level1_key, level1_value in data.items():
            for level2_key, level2_value in level1_value.items():
                for level3_key, level3_value in level2_value.items():
                    for level4_key, level4_value in level3_value.items():
                        element_count += len(level4_value)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return {"element_count": element_count}

def generate_nested_json(levels=5, elements_per_level=5):
    result = {}
    for i in range(elements_per_level):
        current = result[f"level_4_key_{i}"] = {}
        for j in range(elements_per_level):
            current2 = current[f"level_3_key_{j}"] = {}
            for k in range(elements_per_level):
                current3 = current2[f"level_2_key_{k}"] = {}
                for l in range(elements_per_level):
                    current4 = current3[f"level_1_key_{l}"] = {}
                    for m in range(elements_per_level):
                        current4[f"key_{m}"] = f"value_{m}"
    return result

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")

async def main():
    server_thread = Thread(target=run_server, daemon=True)
    server_thread.start()
    await asyncio.sleep(0.1)
    
    async with httpx.AsyncClient() as client:
        try:
            nested_json = generate_nested_json()
            response = await client.post("http://127.0.0.1:8000/process/", json=nested_json)
            print("Response from server:", response.json())
        except Exception as e:
            print("Error:", e)
    print("Done.")

if __name__ == "__main__":
    asyncio.run(main())