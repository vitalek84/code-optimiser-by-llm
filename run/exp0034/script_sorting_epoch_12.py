"""
This is the first optimization attempt. Here's my thought process:
1. The main performance bottleneck is the intentional time.sleep(0.5) which adds unnecessary delay
2. The shuffle and reverse_sort operations are also inefficient and unnecessary
3. Since the goal is to sort the list, we can directly use Python's built-in sorted() function
4. We'll remove all the inefficient parts while maintaining the same output

Main optimizations:
- Remove time.sleep()
- Remove unnecessary shuffle and reverse_sort operations
- Replace the entire algorithm with a direct sorted() call
- Remove unused imports
"""

def very_inefficient_sort(data):
    return sorted(data)

# Example list to sort
unsorted_list = [5, 3, 8, 6, 2, 7, 4, 1]
sorted_list = very_inefficient_sort(unsorted_list)
print(f"Sorted list: {sorted_list}")