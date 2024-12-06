"""
First optimization attempt aims to:
1. Remove unnecessary time.sleep() since it artificially adds delay
2. Remove inefficient intermediate operations (shuffle and reverse_sort)
3. Use Python's built-in sorted() function directly since it's implemented in C and highly optimized
4. Remove redundant function definitions and checks
5. Remove unnecessary variables and iterations

The goal is to get the same sorted output but with minimal processing time.
"""

def very_inefficient_sort(data):
    return sorted(data)

# Example list to sort
unsorted_list = [5, 3, 8, 6, 2, 7, 4, 1]
sorted_list = very_inefficient_sort(unsorted_list)
print(f"Sorted list: {sorted_list}")