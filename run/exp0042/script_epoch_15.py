
"""
I noticed that the base code performs a line-by-line search using regular expressions, which can be inefficient for larger files.
To optimize the execution time, I have made the following improvements:
1. Utilize Python's `collections.Counter` to simplify counting request types and improve performance.
2. Read the entire file at once, as this might leverage any internal buffering that operates more efficiently with large file chunks.
3. Compile the regex once and directly extract results using a list comprehension.
These changes should reduce execution time by minimizing repeated operations and better utilizing built-in efficient data structures.
"""

import re
from collections import Counter

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Read the entire access.log file 
with open("./data/access.log", "r") as file:
    content = file.read()

# Use list comprehension to gather all request types based on matching pattern
request_types = log_pattern.findall(content)

# Count occurrence of each request type using Counter
request_type_count = Counter(request_type for request_type, _ in request_types)

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
