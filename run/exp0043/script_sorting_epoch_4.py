
"""
My aim is to optimize the code by eliminating unnecessary inefficiencies. 
The previous version used a highly inefficient sorting process with artificial delays and redundant operations. 
I'll focus on removing these inefficiencies and replace the sorting mechanism with Python's built-in quick sort through `sorted()`.
This should highly reduce execution time as python's built-in sort is optimized for our use case. Also, since the results with the reference were correct, we will maintain this approach. 
"""

# Optimize imports
import random

def very_efficient_sort(data):
    # Immediately sort the list using Python's highly optimized built-in sort
    return sorted(data)

# Example list to sort
unsorted_list = [5, 3, 8, 6, 2, 7, 4, 1]
sorted_list = very_efficient_sort(unsorted_list)
print(f"Sorted list: {sorted_list}")
