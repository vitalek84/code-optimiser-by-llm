
"""
Optimization Strategy:
1. Use a more efficient way to read and process the log file.
2. Utilize `collections.Counter` for counting occurrences, which is generally faster than manually managing dictionaries.
3. Compile the regular expression pattern only once outside of the loop.
4. Read the entire file content at once instead of reading line by line (if memory allows).
"""

import re
from collections import Counter

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Read the entire access.log file content at once
with open("./data/access.log", "r") as file:
    log_content = file.read()

# Find all matches in the file content
matches = log_pattern.findall(log_content)

# Extract request types and count them using Counter
request_type_count = Counter(request[0] for request in matches)

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
