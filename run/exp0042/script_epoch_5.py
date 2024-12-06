
"""
I am attempting to optimize the previous version by:
1. Utilizing the collections.Counter class to simplify and speed up the counting process of request types, as it is more efficient than a traditional dictionary.
2. Reading the file more efficiently using a memory-mapped file, which should speed up the file I/O operations.
"""

import re
import mmap
from collections import Counter

# Regular expression to extract request type
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Initialize Counter to store counts
request_type_count = Counter()

# Read the access.log file using memory mapping for faster access
with open("./data/access.log", "r") as file:
    with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
        for line in iter(mmapped_file.readline, b""):
            match = log_pattern.search(line.decode('utf-8'))
            if match:
                # Extract and count request type
                request_type = match.group(1)
                request_type_count[request_type] += 1

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
