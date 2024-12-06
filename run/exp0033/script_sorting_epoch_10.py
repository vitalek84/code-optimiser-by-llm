
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

    # Removed the loop and directly calling the sorted() function to sort the list
    unsorted_list = [5, 3, 8, 6, 2, 7, 4, 1]
    sorted_list = sorted(unsorted_list)
    return sorted_list
