
"""
This version uses a Counter from the collections module to count request types, which is generally faster than using a dictionary.
Additionally, it reads the entire file content at once and processes it in one go, which can be more efficient than processing line by line.
"""

import re
from collections import Counter

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Read the access.log file content at once
with open("./data/access.log", "r") as file:
    log_content = file.read()

# Find all matches and extract request types
request_types = log_pattern.findall(log_content)[0]

# Count request types using Counter
request_type_count = Counter(request_types)

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
