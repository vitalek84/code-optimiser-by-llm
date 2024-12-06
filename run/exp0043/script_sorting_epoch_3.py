
import random

def very_inefficient_sort(data):
    """
    After analyzing the initial version, I noticed the use of significant artificial delays and inefficient sorting methods.
    To optimize:
    1. I removed the artificial delay (time.sleep(0.5)) as it unnecessarily increases execution time.
    2. I removed the inefficient 'reverse_sort' code since its only purpose is to add computational overhead.
    3. I reduced the maximum number of iterations from 40 to a lower number (e.g., 10) for testing since the implementation
       can fall back to the efficient built-in sorted() function if needed, minimizing overhead.
    4. Since the process is 'inefficient sort', kept the shuffle for the initial attempt to sort.
    """

    def is_sorted(lst):
        for i in range(len(lst) - 1):
            if lst[i] > lst[i + 1]:
                return False
        return True

    def shuffle(lst, intensity=1.0):
        for _ in range(int(len(lst) * intensity)):
            i, j = random.randint(0, len(lst) - 1), random.randint(0, len(lst) - 1)
            lst[i], lst[j] = lst[j], lst[i]
        return lst

    max_iterations = 10  # Reduced iterations count
    iteration = 0
    intensity = 1.0

    while not is_sorted(data) and iteration < max_iterations:
        data = shuffle(data, intensity)
        intensity = max(0.1, intensity * 0.9)
        iteration += 1

    if not is_sorted(data):
        data = sorted(data)

    return data

# Example list to sort
unsorted_list = [5, 3, 8, 6, 2, 7, 4, 1]
sorted_list = very_inefficient_sort(unsorted_list)
print(f"Sorted list: {sorted_list}")
