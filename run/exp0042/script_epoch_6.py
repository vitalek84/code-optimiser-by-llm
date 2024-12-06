
"""
I noticed that the current and initial versions are basically the same and have the same results. I will work on optimizing the code by leveraging collections.Counter to simplify the counting process and potentially improve performance. Using `collections.Counter` allows for more efficient counting since it is optimized for high performance. I will also condense the logic into a more Pythonic approach by utilizing list comprehension. This approach may also leverage lower level optimizations from the `collections` library.
"""

import re
from collections import Counter

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Read the access.log file line by line and count request types
with open("./data/access.log", "r") as file:
    request_type_count = Counter(
        log_pattern.search(line).group(1)
        for line in file
        if log_pattern.search(line)
    )

# Sort the counts in descending order
sorted_request_type_count = request_type_count.most_common()

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count:
    print(f"{request_type}: {count}")
