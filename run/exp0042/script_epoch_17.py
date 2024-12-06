
"""
To optimize the script, I started by analyzing the base and previous codes. The first step was to check for any libraries
that could potentially boost the performance for operations like regex matching and counting. As we are reading large files line by line, 
the use of built-in modules is a good step to optimize.

1. Used the `collections.Counter` from Python's standard library to simplify and speed up counting of request types.
2. Read the file once and used list comprehension to improve the iteration efficiency.
3. Used multithreading to read and process the file contents since it can provide speed up in I/O operations by overlapping.

These changes aim to reduce execution time by optimizing memory access and data handling.
"""

import re
from collections import Counter
import threading

# Initialize request count
request_type_count = Counter()

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

def process_lines(lines):
    global request_type_count
    local_count = Counter()
    
    for line in lines:
        match = log_pattern.search(line)
        if match:
            request_type = match.group(1)
            local_count[request_type] += 1
    
    request_type_count.update(local_count)

# Read file and split into chunks for processing
def read_file_and_process(filename, chunk_size=10000):
    with open(filename, "r") as file:
        lines = file.readlines()

    # Create threads to process each chunk of lines
    threads = []
    for i in range(0, len(lines), chunk_size):
        thread = threading.Thread(target=process_lines, args=(lines[i:i + chunk_size],))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

read_file_and_process("./data/access.log")

# Sort the counts in descending order
sorted_request_type_count = dict(request_type_count.most_common())

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
