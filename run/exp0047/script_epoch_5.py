
"""
Optimization Strategy:
1. Use `collections.Counter` for counting occurrences which is optimized for such tasks.
2. Read the entire file content at once instead of reading line by line to reduce I/O operations.
3. Pre-compile the regular expression outside the loop to avoid re-compilation in each iteration.
4. Use a more efficient way to extract and count request types.
"""

from collections import Counter
import re

# Initialize dictionary to store counts
request_type_count = Counter()

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Read the entire access.log file content at once
with open("./data/access.log", "r") as file:
    log_content = file.read()

# Find all matches and count request types
for match in log_pattern.finditer(log_content):
    request_type = match.group(1)
    request_type_count[request_type] += 1

# Sort the counts in descending order
sorted_request_type_count = request_type_count.most_common()

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count:
    print(f"{request_type}: {count}")
