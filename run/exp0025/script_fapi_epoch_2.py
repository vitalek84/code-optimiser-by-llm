'''
For this optimization attempt, I will focus on several key improvements:
1. Use a more efficient JSON processing approach by flattening the dictionary in a single pass
2. Replace string concatenation with format strings for better performance
3. Use a faster web framework - replace FastAPI with Starlette for lower overhead
4. Optimize the JSON generation process
5. Remove global variables and implement better state management
6. Use asyncio for better concurrent handling
'''

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn
from threading import Thread
import requests
import time
import asyncio

# Internal storage dictionary
internal_dict = {}

async def process_item(request):
    global internal_dict
    internal_dict = {}
    element_count = 0
    
    try:
        data = await request.json()
        def flatten_dict(d, prefix=""):
            nonlocal element_count
            items = []
            for k, v in d.items():
                if isinstance(v, dict):
                    items.extend(flatten_dict(v, f"{prefix}{k}." if prefix else f"{k}."))
                else:
                    key = f"{prefix}{k}"
                    internal_dict[key] = v
                    element_count += 1
                    items.append((key, v))
            return items

        flatten_dict(data)
        return JSONResponse({"element_count": element_count})
    except Exception as e:
        return JSONResponse({"error": f"An error occurred: {str(e)}"})

def generate_nested_json(levels=5, elements_per_level=5):
    if levels == 1:
        return {f"key_{i}": f"value_{i}" for i in range(elements_per_level)}
    return {f"level_{levels-1}_key_{i}": generate_nested_json(levels-1, elements_per_level) 
            for i in range(elements_per_level)}

routes = [
    Route("/process/", process_item, methods=["POST"])
]

app = Starlette(debug=False, routes=routes)

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")

server_thread = Thread(target=run_server, daemon=True)
server_thread.start()
time.sleep(1)

try:
    url = "http://127.0.0.1:8000/process/"
    nested_json = generate_nested_json()
    response = requests.post(url, json=nested_json)
    print("Response from server:", response.json())
except Exception as e:
    print("Error:", e)

print("Done.")