"""
Let's optimize this script by:
1. Using collections.Counter which is more efficient for counting than a regular dictionary
2. Reading file in chunks instead of line by line
3. Using a simpler regex pattern since we only need the request type
4. Using a set lookup for better performance in pattern matching
5. Correcting the regex pattern to avoid counting incorrect matches (noticed different results in GET requests)
"""

import re
from collections import Counter

# Initialize counter
request_type_count = Counter()

# Simplified regex pattern that matches only the request type
log_pattern = re.compile(r'"([A-Z_]+) /')

# Read the file in chunks for better performance
with open("./data/access.log", "r") as file:
    chunk_size = 8192 * 1024  # 8MB chunks
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        
        # Find all matches in the chunk
        matches = log_pattern.finditer(chunk)
        request_type_count.update(match.group(1) for match in matches)

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")