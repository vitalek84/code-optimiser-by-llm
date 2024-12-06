
"""
My initial analysis of the script shows a potential for optimization by using the collections.Counter class from the collections module 
for counting request types, which has more efficient algorithms for frequency counting than manually incrementing counts in a dictionary. 
Additionally, I will use the with statement for file opening to ensure proper handling of resources.
Introducing itertools for batch reading might help if large chunks of the file can be read to reduce disk I/O operations,
but I will refrain from it now because of the pattern matching dependency for each line. 
This step will include such high-level optimizations which would provide significant performance benefits 
especially for larger datasets.
"""

import re
from collections import Counter

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Utilize Counter to store request types
with open("./data/access.log", "r") as file:
    request_type_count = Counter(
        match.group(1) 
        for line in file 
        if (match := log_pattern.search(line))
    )

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
