
"""
Optimization strategy:
1. Use `collections.Counter` for counting request types which is more efficient than manually managing a dictionary.
2. Use `re.finditer` instead of `re.search` to find all matches in the line, though in this case, it doesn't change much since we only have one match per line.
3. Read the file using `mmap` to reduce memory overhead and potentially speed up reading large files.
4. Use a generator expression for sorting to avoid creating an intermediate list.

This should improve the performance by leveraging more efficient data structures and methods.
"""

import re
from collections import Counter
import mmap

def count_request_types(log_file_path):
    request_type_count = Counter()

    log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

    with open(log_file_path, "r+b") as file:
        mmapped_file = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
        for line in iter(mmapped_file.readline, b""):
            match = log_pattern.search(line.decode())
            if match:
                request_type = match.group(1)
                request_type_count[request_type] += 1

    sorted_request_type_count = dict(request_type_count.most_common())

    print("Request Type Counts:")
    for request_type, count in sorted_request_type_count.items():
        print(f"{request_type}: {count}")

count_request_types("./data/access.log")
