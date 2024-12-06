
"""
Chain of Thought:
1. I noticed that the results of the reference version and my previous version are different. I will analyze the issue and try to fix it,
   ensuring the results match the reference version.
2. The performance issue might be due to the way the file is read and processed line by line.
3. I'll attempt to optimize it using the multiprocessing module to speed up file processing, as the log file might be large.
4. I will parallelize the computation by dividing the log file into equal chunks based on the number of available CPU cores.
5. Use a multiprocessing Manager to safely merge results from different processes.
"""

import re
import os
from multiprocessing import Pool, Manager

# Function to process a chunk of log lines
def process_lines(log_lines, return_dict):
    local_request_type_count = {}

    # Regular expression to extract request type
    log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

    for line in log_lines:
        match = log_pattern.search(line)
        if match:
            request_type = match.group(1)
            if request_type in local_request_type_count:
                local_request_type_count[request_type] += 1
            else:
                local_request_type_count[request_type] = 1

    # Merge local results into the manager dictionary
    for request_type, count in local_request_type_count.items():
        if request_type in return_dict:
            return_dict[request_type] += count
        else:
            return_dict[request_type] = count

def main():
    # Determine the number of CPU cores available
    cpu_count = os.cpu_count()

    # Read all lines from the file
    with open("./data/access.log", "r") as file:
        lines = file.readlines()

    # Split lines into roughly equal-sized chunks
    chunk_size = len(lines) // cpu_count
    chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]

    # Ensure that the last chunk includes any remaining lines
    if len(chunks) > cpu_count:  # Handle case where line count is not perfectly divisible
        chunks[-2].extend(chunks[-1])
        chunks = chunks[:-1]

    with Manager() as manager:
        # Create a shared dictionary to store results with the Manager
        return_dict = manager.dict()

        # Setup and start the multiprocessing pool
        pool = Pool(cpu_count)
        pool.starmap(process_lines, [(chunk, return_dict) for chunk in chunks])

        # Close and join the pool to ensure completion
        pool.close()
        pool.join()

        # Sort the counts in descending order
        sorted_request_type_count = dict(sorted(return_dict.items(), key=lambda item: item[1], reverse=True))

        # Print the results
        print("Request Type Counts:")
        for request_type, count in sorted_request_type_count.items():
            print(f"{request_type}: {count}")

if __name__ == "__main__":
    main()
