
"""
I noticed that the previous version had the same execution time as the base code. So, I will attempt a new optimization approach.
In this version, I will utilize the 'collections.Counter' to manage the counting process more efficiently. 
This allows dictionary updates in a more Pythonic and potentially faster way, especially for large data sets.
Additionally, I will use 'with open' as a context manager for consistent file handling.
"""

import re
from collections import Counter

# Initialize Counter to store counts
request_type_count = Counter()

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Read the access.log file line by line
with open("./data/access.log", "r") as file:
    for line in file:
        match = log_pattern.search(line)
        if match:
            # Extract request type
            request_type = match.group(1)
            # Count request types
            request_type_count.update([request_type])

# Sort the counts in descending order
sorted_request_type_count = request_type_count.most_common()

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count:
    print(f"{request_type}: {count}")
