
"""
Chain of thought:
1. The previous version of the script used a regular expression to extract request type and User-Agent from each log line, which is computationally expensive.
2. Instead of using regex for extraction, we can use string splitting and slicing to achieve similar results more efficiently.
3. We will read the file in binary mode to avoid encoding issues and decode it within the loop.
4. By using defaultdict, we can simplify the counting process.
5. The script should be faster due to these changes.

Results should match the reference results.
"""

from collections import defaultdict

# Initialize dictionary to store counts
request_type_count = defaultdict(int)

# Open the access.log file in binary mode
with open("./data/access.log", "rb") as file:
    for line in file:
        decoded_line = line.decode('utf-8').strip()
        parts = decoded_line.split('"')
        
        if len(parts) >= 3:
            request_type = parts[1].split()[0]
            request_type_count[request_type] += 1

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
