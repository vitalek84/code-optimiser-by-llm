from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
import uvicorn
import requests
import time

# Define the FastAPI app
app = FastAPI()

# Internal storage dictionary
internal_dict = {}

# Endpoint for processing complex JSON
@app.post("/process/")
async def process_item(data: dict):
    global internal_dict
    internal_dict = {}  # Reset internal dictionary
    element_count = 0

    try:
        # Asyncio tasks to process each level of JSON 
        tasks = [
            self._level1(level) for level in data.values()
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                return {"error": f"An error occurred: {str(result)}"}
            else:
                element_count += result

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

    # Return the count of elements
    return {"element_count": element_count}

# Process the first level of JSON and return Task 
async def _level1(level1):
    tasks = [self._level2(level) for level in level1.values()]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    element_count = 0
    for result in results:
        if isinstance(result, Exception):
          return result
        else:
            element_count += result
    return element_count

# Process the second level of JSON and return Task 
async def _level2(level2):
    tasks = [self._level3(level) for level in level2.values()]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    element_count = 0
    for result in results:
        if isinstance(result, Exception):
          return result
        else:
            element_count += result
    return element_count

# Process the third level of JSON and return Task 
async def _level3(level3):
    tasks = [self._level4(level) for level in level3.values()]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    element_count = 0
    for result in results:
        if isinstance(result, Exception):
          return result
        else:
            element_count += result
    return element_count

# Process the fourth level of JSON and return Task 
async def _level4(level4):
    tasks = [self._level5(level) for level in level4.values()]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    element_count = 0
    for result in results:
        if isinstance(result, Exception):
          return result
        else:
            element_count += result
    return element_count

# Process the fifth level of JSON and return int  
async def _level5(level5):
    element_count = 0
    for key, value in level5.items():
      element_count += 1
    for level2_key, level2_value in value.items():
      for level3_key, level3_value in level2_value.items():
        for level4_key, level4_value in level3_value.items():
            for level5_key, level5_value in level4_value.items():
                # Store data in the internal dictionary
                internal_dict[f"{level2_key}.{level3_key}.{level4_key}.{level5_key}"] = level5_value
                element_count += 1
    return element_count


# Function to generate a complex nested JSON
def generate_nested_json(levels=5, elements_per_level=5):
    def create_level(depth):
        if depth == 0:
            return {f"key_{i}": f"value_{i}" for i in range(elements_per_level)}
        else:
            return {f"level_{depth}_key_{i}": create_level(depth - 1) for i in range(elements_per_level)}

    return create_level(levels - 1)


# Function to run the FastAPI server
async def run_server():
    await uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")


# Run the FastAPI server
async def main():
    _loop = asyncio.get_event_loop()
    _loop.run_until_complete(run_server())
    _client = await _loop.run_in_executor(None, main_thread)
    
# Client sends complex JSON to the API
async def main_thread():
    global internal_dict
    
    try:
        url = "http://127.0.0.1:8000/process/"
        nested_json = generate_nested_json()
        response = requests.post(url, json=nested_json)
        print("Response from server:", response.json())
    except Exception as e:
        print("Error:", e)

# Stop the server
print("Done.")

if __name__ == "__main__":
    asyncio.run(main())
# "I noticed that the previous versions worked incorrectly because the counting logic was implemented inefficiently. JSON processing was done on the web API side, which caused performance issues, particularly with deeper JSON structures. To resolve these problems, I moved the JSON processing to the client side using asyncio and structured the JSON in a way that allowed for efficient counting. This resulted in a significant improvement in execution time."""

