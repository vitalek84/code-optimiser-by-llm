
import random
import time

def very_inefficient_sort(data):
    def is_sorted(lst):
        """Check if a list is sorted."""
        for i in range(len(lst) - 1):
            if lst[i] > lst[i + 1]:
                return False
        return True

    def shuffle(lst, intensity=1.0):
        """Randomly shuffle a list with decreasing intensity."""
        for _ in range(int(len(lst) * intensity)):
            i, j = random.randint(0, len(lst) - 1), random.randint(0, len(lst) - 1)
            lst[i], lst[j] = lst[j], lst[i]
        return lst

    def reverse_sort(lst):
        """Sort the list in reverse order using bubble sort for inefficiency."""
        n = len(lst)
        for i in range(n):
            for j in range(n - i - 1):
                if lst[j] < lst[j + 1]:
                    lst[j], lst[j + 1] = lst[j + 1], lst[j]
        return lst

    def fuzzy_shuffle(lst):
        """Shuffle the list with a random intensity in the range [0.1, 1.0]."""
        rand = random.uniform(0.1, 1.0)
        shuffle(lst, rand)

    def fuzzy_reverse_sort(lst):
        """Reverse-sort the list with a random number of passes in the range [1, n]."""
        n = len(lst)
        rand = random.randint(1, n)
        reverse_sort(lst, rand)

    max_iterations = 40  # Maximum number of iterations to avoid infinite loops
    iteration = 0
    intensity = 1.0  # Start with full shuffle intensity

    while not is_sorted(data) and iteration < max_iterations:
        # Randomly shuffle the list with varying intensity
        # print(f"Iteration {iteration + 1}: Fuzzy shuffling")
        fuzzy_shuffle(data)

        # Waste time by reverse-sorting the list (which we will shuffle anyway)
        # print(f"Iteration {iteration + 1}: Fuzzy reverse sorting: {data}")
        fuzzy_reverse_sort(data)

        # Add an artificial delay for fun
        time.sleep(0.5)

        iteration += 1

    if is_sorted(data):
        pass
        # print("Successfully sorted!")
    else:
        # print("Max iterations reached. Final attempt to sort...")
        data = sorted(data)  # Fallback to ensure the result is sorted

    return data


# Example list to sort
unsorted_list = [5, 3, 8, 6, 2, 7, 4, 1]
sorted_list = very_inefficient_sort(unsorted_list)
print(f"Sorted list: {sorted_list}")
