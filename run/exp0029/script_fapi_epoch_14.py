
# In this version of the code the whole function has been decorated with @profile 
# and put inside function wrapper. 
# @profile indicate that we want to collect statistics about hot-spots in the code
# decorator profile: https://docs.python.org/3/library/profile.html
# To analyze the overhead introduced by the server creation and startup, 
# I am only measuring the time spent inside the process_item function. 
# I also added gc.disable and enable around the server creation to avoid noise in profiling.
# gc: https://docs.python.org/3/library/gc.html
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from threading import Thread
from queue import Queue
import gc
try:
    import cProfile as profile
except ImportError:
    import profile as profile


app = FastAPI()
internal_dict = {}


def process_item(data: dict):
    global internal_dict
    internal_dict = {}  # Reset internal dictionary
    element_count = 0

    try:
        # Nested loops to process the JSON
        for level1_key, level1_value in data.items():
            for level2_key, level2_value in level1_value.items():
                for level3_key, level3_value in level2_value.items():
                    for level4_key, level4_value in level3_value.items():
                        for level5_key, level5_value in level4_value.items():
                            # Store data in the internal dictionary
                            internal_dict[f"{level1_key}.{level2_key}.{level3_key}.{level4_key}.{level5_key}"] = level5_value
                            element_count += 1
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")

    # Return the count of elements
    return {"element_count": element_count}


def generate_nested_json(levels=5, elements_per_level=5):
    def create_level(depth):
        if depth == 0:
            return {f"key_{i}": f"value_{i}" for i in range(elements_per_level)}
        else:
            return {f"level_{depth}_key_{i}": create_level(depth - 1) for i in range(elements_per_level)}

    return create_level(levels - 1)


def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")


def wrapper(func, *args, **kwargs):
    pr = profile.Profile()
    try:
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()
        return result
    finally:
        pr.print_stats(sort='time')


if __name__ == "__main__":
    # Generate complex JSON data
    nested_json = generate_nested_json()

    # Server initialization
    server_thread = Thread(target=run_server, daemon=True)

    print('Start server')
    # Disable garbage collection to avoid noise in profiling
    gc.disable()
    server_thread.start()
    # Allow some time for the server to start
    time.sleep(1)
    gc.enable()

    # Server communication/profiling
    response = wrapper(process_item, nested_json)
    print(response)
    print('Server done.')

    print('Unloading server...')
    server_thread.join()
    print('Done.')

