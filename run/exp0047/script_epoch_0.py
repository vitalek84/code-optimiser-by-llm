
"""
Chain of thought:
1. The previous code uses a regular expression to extract the request type and User-Agent, which is computationally expensive.
2. Instead of using regex for each line, we can use the `split` method to parse the log lines more efficiently.
3. We will also use the `collections.Counter` to count occurrences of request types, as it provides a faster way to count items compared to manually managing a dictionary.
4. The sorted operation is already efficient (O(n log n)), so no changes are needed there.
5. By avoiding regex and using more efficient string parsing and counting methods, we should see an improvement in execution time.
"""

from collections import Counter

# Initialize a counter to store counts
request_type_count = Counter()

# Read the access.log file line by line
with open("./data/access.log", "r") as file:
    for line in file:
        parts = line.split()
        if len(parts) > 5:
            # Extract request type
            request_type = parts[5].strip('"').split('/')[0]
            
            # Count request types
            request_type_count[request_type] += 1

# Sort the counts in descending order
sorted_request_type_count = dict(request_type_count.most_common())

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
