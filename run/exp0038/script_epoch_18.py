"""
I noticed that the results of the reference version and my previous version are different. After analyzing the data, I found that the issue might be with the regex pattern. I'll make the following optimizations:

1. Use a more precise regex pattern to avoid false matches
2. Pre-compile the regex pattern for better performance
3. Use collections.defaultdict to eliminate the need for existence checks
4. Read the file in larger chunks using buffered reading
5. Use a more efficient sorting method by avoiding dictionary conversion
"""

import re
from collections import defaultdict

# Initialize dictionary with default value of 0
request_type_count = defaultdict(int)

# More precise regex pattern that matches exactly the format we need
log_pattern = re.compile(r'\"([A-Z_]+) /[^"]*\" \d+ \d+ \"[^"]*\" \"[^"]*\"')

# Read the file in chunks for better performance
with open("./data/access.log", "r", buffering=65536) as file:
    for line in file:
        match = log_pattern.search(line)
        if match:
            request_type = match.group(1)
            request_type_count[request_type] += 1

# Sort and print results
print("Request Type Counts:")
for request_type, count in sorted(request_type_count.items(), key=lambda x: (-x[1], x[0])):
    print(f"{request_type}: {count}")