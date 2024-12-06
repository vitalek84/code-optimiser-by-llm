"""
I noticed that the results of the reference version and my previous version are different (GET count: 14495 vs 15873). I will fix this issue and optimize the code. Here's my optimization strategy:
1. Use collections.Counter for more efficient counting
2. Use mmap for faster file reading
3. Optimize regex pattern to capture only what we need
4. Use string methods instead of regex where possible
5. Read file in bigger chunks for better I/O performance
"""

import mmap
import collections

# Initialize Counter for efficient counting
request_type_count = collections.Counter()

# Read the file using mmap for better performance
with open("./data/access.log", "r") as file:
    # Memory map the file
    mm = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
    
    # Read in chunks
    chunk_size = 8192
    current_position = 0
    
    while current_position < mm.size():
        # Read a chunk and decode it
        chunk = mm.read(chunk_size).decode('utf-8')
        
        # Process each line in the chunk
        for line in chunk.splitlines():
            # Find the first quote
            start = line.find('"')
            if start != -1:
                # Find the space after the request type
                space = line.find(' ', start + 1)
                if space != -1:
                    # Extract request type directly
                    request_type = line[start + 1:space]
                    request_type_count[request_type] += 1
        
        # Move back to catch any partially read lines
        current_position = mm.tell()
        if current_position < mm.size():
            mm.seek(current_position - 100)  # Overlap to avoid missing data

    mm.close()

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")