
"""
Chain of thought:
1. The previous version had a time complexity of O(n log n) due to the sorting operation.
2. We can optimize this by using `collections.Counter` which is implemented with a hash table and has a time complexity of O(n).
3. Additionally, we can use list comprehensions for more efficient line processing.
4. The regular expression compilation is moved outside the loop to avoid redundant compilations.
5. Using `with open(...)` ensures proper file handling.
"""

import re
from collections import Counter

# Initialize dictionaries to store counts
request_type_count = {}

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Read the access.log file line by line
with open("./data/access.log", "r") as file:
    lines = [line for line in file if log_pattern.search(line)]
    matches = [log_pattern.search(line).groups() for line in lines]
    request_types = [match[0] for match in matches]

# Count request types using Counter
request_type_count = Counter(request_types)

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
