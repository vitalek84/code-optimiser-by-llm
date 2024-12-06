
"""
My initial plan is to replace the current method of iterating and counting request types with a more efficient method using the `collections.Counter` class. In theory, this will lead to a performance boost due to its optimized counting capabilities. If this step shows improvement in execution time, I will then explore ways to reduce regex searches using more efficient logic, if possible. Additionally, I will try to reduce the number of lookups and use in-place sorting for efficiency gains.
"""

import re
from collections import Counter

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Read and process the access.log file using Counter for direct counting
with open("./data/access.log", "r") as file:
    request_type_count = Counter(match.group(1) for line in file
                                 if (match := log_pattern.search(line)))

# Sort the counts in descending order
sorted_request_type_count = dict(request_type_count.most_common())

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
