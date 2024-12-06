
import random

def very_inefficient_sort(data):
    """
    Optimized the sorting procedure by removing the artificial delay
    and the inefficient reverse sorting step which does not aid in sorting.
    Instead of shuffling multiple elements, we shuffle just a pair, decreasing unnecessary operations.
    Reduced maximum iteration count to allow the algorithm to terminate faster while maintaining the shuffle strategy.
    Utilized Python's built-in sorted as a final fallback without iteration restraints.
    """

    def is_sorted(lst):
        """Check if a list is sorted."""
        return all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1))

    def shuffle(lst):
        """Randomly shuffle a pair of elements in the list."""
        i, j = random.sample(range(len(lst)), 2)
        lst[i], lst[j] = lst[j], lst[i]
        return lst

    max_iterations = 10  # Reduced number of maximum iterations
    iteration = 0

    while not is_sorted(data) and iteration < max_iterations:
        data = shuffle(data)
        iteration += 1

    return sorted(data)  # Fallback to ensure the result is sorted

# Example list to sort
unsorted_list = [5, 3, 8, 6, 2, 7, 4, 1]
sorted_list = very_inefficient_sort(unsorted_list)
print(f"Sorted list: {sorted_list}")
