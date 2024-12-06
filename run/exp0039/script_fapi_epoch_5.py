"""
This is the first optimisation iteration. For improving execution time I suggest following changes:
1. Replace nested loops with a recursive function that will process the JSON data more efficiently.
2. Use f-strings concatenation only once by collecting path parts in a list.
3. Use a more efficient dictionary comprehension for generating nested JSON.
4. Remove global dictionary since it's not used outside the function.
5. Replace time.sleep with a more reliable server startup check.
6. Add httpx library instead of requests as it's more performant.
7. Add asyncio support for better async handling.
8. Add ProcessPoolExecutor for parallel JSON generation.
"""

from fastapi import FastAPI
import uvicorn
import httpx
from threading import Thread
import asyncio
from concurrent.futures import ProcessPoolExecutor

app = FastAPI()

@app.post("/process/")
async def process_item(data: dict):
    element_count = [0]
    result_dict = {}
    
    def process_nested(obj, path_parts=[]):
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_path = path_parts + [key]
                if isinstance(value, dict):
                    process_nested(value, new_path)
                else:
                    result_dict['.'.join(new_path)] = value
                    element_count[0] += 1
    
    try:
        process_nested(data)
        return {"element_count": element_count[0]}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

def generate_nested_json(levels=5, elements_per_level=5):
    if levels == 1:
        return {f"key_{i}": f"value_{i}" for i in range(elements_per_level)}
    return {f"level_{levels-1}_key_{i}": generate_nested_json(levels-1, elements_per_level) 
            for i in range(elements_per_level)}

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")

async def check_server():
    async with httpx.AsyncClient() as client:
        while True:
            try:
                await client.get("http://127.0.0.1:8000/")
                break
            except:
                await asyncio.sleep(0.1)

async def main():
    server_thread = Thread(target=run_server, daemon=True)
    server_thread.start()
    
    await check_server()
    
    with ProcessPoolExecutor() as executor:
        nested_json = executor.submit(generate_nested_json).result()
    
    async with httpx.AsyncClient() as client:
        response = await client.post("http://127.0.0.1:8000/process/", json=nested_json)
        print("Response from server:", response.json())
    
    print("Done.")

if __name__ == "__main__":
    asyncio.run(main())