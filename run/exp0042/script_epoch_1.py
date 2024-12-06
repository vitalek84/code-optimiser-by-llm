
"""
In the previous version, the code was iterating over each line of the file and using regular expressions to parse the data.
While this approach correctly returns results identical to the base code, its execution time is not optimized.
To improve performance:
1. Use collections.defaultdict for simpler and potentially faster counting.
2. Use regex only once per line processing to minimize overhead.
3. Attempt to read the log file in chunks to make I/O operations more efficient.
"""

import re
from collections import defaultdict

# Initialize defaultdict to store counts
request_type_count = defaultdict(int)

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Read the access.log file in chunks to improve performance
with open("./data/access.log", "r") as file:
    while chunk := file.read(8192):  # Reading by chunks of 8KB
        for line in chunk.splitlines():
            match = log_pattern.search(line)
            if match:
                # Extract request type
                request_type = match.group(1)
                # Count request types using defaultdict
                request_type_count[request_type] += 1

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
