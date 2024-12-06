
"""
The initial version of the script is intentionally inefficient. It uses a combination of random shuffling and reverse-sorting with bubble sort, which is not a realistic approach to efficiently sort data. Additionally, it includes an artificial delay, which unnecessarily extends the execution time. The first step was to directly adopt the script for future modifications. Since the sorting method largely contributes to inefficiency, replacing it with Python's built-in sorting function provides the most significant improvement. Removing unnecessary methods and delays will further optimize the solution. I will focus on leveraging Python's built-in methods and remove inefficient constructs to significantly reduce the execution time while maintaining the expected results.
"""

import random

def optimized_sort(data):
    return sorted(data)

# Example list to sort
unsorted_list = [5, 3, 8, 6, 2, 7, 4, 1]
sorted_list = optimized_sort(unsorted_list)
print(f"Sorted list: {sorted_list}")
