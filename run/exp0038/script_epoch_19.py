"""
I notice that results from the previous iteration are different from the reference results. I'll fix this issue. 
To optimize the script, I'll implement the following improvements:
1. Use collections.Counter instead of manual dictionary counting
2. Read file in larger chunks using buffered reading
3. Pre-compile regex pattern with flags
4. Use more efficient string matching by adding anchors to regex
5. Optimize sorting by using sorted() directly on items
"""

import re
from collections import Counter
import io

# Regular expression to extract request type with anchors and flags
log_pattern = re.compile(r'\"(\w+) /.*?\" \d+ \d+ \"-\" \".*?\"$', re.MULTILINE)

# Initialize counter for request types
request_type_count = Counter()

# Read the access.log file in larger chunks
with open("./data/access.log", "r", buffering=65536) as file:
    # Process file in chunks
    chunk = file.read()
    matches = log_pattern.finditer(chunk)
    request_type_count.update(match.group(1) for match in matches)

# Print the results
print("Request Type Counts:")
for request_type, count in sorted(request_type_count.items(), key=lambda x: (-x[1], x[0])):
    print(f"{request_type}: {count}")