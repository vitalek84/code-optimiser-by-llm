
"""
I noticed that the previous version works incorrectly. I analysed the issue and fixed it.
Also I understand that I shouldn’t take to account execution time of not working version.

In this new version, I will use a more efficient way to count occurrences by utilizing 
collections.Counter which is optimized for such operations. Additionally, I'll read 
the entire file at once instead of reading line by line, and use list comprehensions 
for better performance.
"""

import re
from collections import Counter

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Read the access.log file at once
with open("./data/access.log", "r") as file:
    lines = file.readlines()

# Extract request types using list comprehension and count them with Counter
request_types = [match.group(1) for line in lines if (match := log_pattern.search(line))]
request_type_count = Counter(request_types)

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
