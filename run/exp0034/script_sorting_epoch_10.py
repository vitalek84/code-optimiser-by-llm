"""
In this optimization attempt, I'll focus on several key improvements:
1. Remove the artificial time.sleep delay which adds unnecessary 0.5s per iteration
2. Replace the inefficient bubble sort with Python's built-in sorted function
3. Remove unnecessary shuffling and reverse sorting operations
4. Simplify the is_sorted check using all() function
5. Since the goal is just to sort the list efficiently, we can skip all the randomization and just use sorted()

The above changes should dramatically reduce execution time while maintaining the same output.
"""

def very_inefficient_sort(data):
    return sorted(data)

# Example list to sort
unsorted_list = [5, 3, 8, 6, 2, 7, 4, 1]
sorted_list = very_inefficient_sort(unsorted_list)
print(f"Sorted list: {sorted_list}")