"""
My chain of thought for optimizing this script:
1. The main performance bottleneck is the artificial time.sleep(0.5) which adds unnecessary delay
2. The complex shuffling and reverse sorting operations are inefficient and unnecessary
3. Since the goal is to sort the list, we can directly use Python's built-in sorted() function
4. We'll remove all the unnecessary helper functions and operations
5. This should reduce execution time from ~20 seconds to microseconds
"""

def very_inefficient_sort(data):
    return sorted(data)

# Example list to sort
unsorted_list = [5, 3, 8, 6, 2, 7, 4, 1]
sorted_list = very_inefficient_sort(unsorted_list)
print(f"Sorted list: {sorted_list}")