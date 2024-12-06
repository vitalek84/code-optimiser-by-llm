
"""
I notice that the previous version performs correctly with respect to functional output, producing identical results to the base version. However, no optimizations had been applied yet, so the execution time remains unchanged from the base version. 

To optimize, I will utilize the `collections.Counter` which should be faster for counting occurrences than the custom dictionary incrementing method employed in the current code. The `Counter` is optimized for counting and will help decrease execution time. I will also test reading the file all at once for a very slight optimization, taking advantage of list comprehensions and generator expressions for concise and potentially faster processing. The regular expression remains because it already exactly extracts the necessary data without performing any extra work.
"""

import re
from collections import Counter

# Regular expression to extract request type
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Read the access.log file all at once
with open("./data/access.log", "r") as file:
    log_lines = file.readlines()

# Use a Counter to count request types efficiently
request_types = (log_pattern.search(line).group(1) for line in log_lines if log_pattern.search(line))
request_type_count = Counter(request_types)

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
