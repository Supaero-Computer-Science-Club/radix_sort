import numpy as np
from tqdm import trange


def count_all_radix(array):
    counts = [[0 for _ in range(10)] for _ in range(len(str(np.max(array))))]
    for el in array:
        radix = 1
        i = 0
        while el != 0:
            digit = el % 10
            counts[i][digit] += 1
            el = (el // 10)
            radix *= 10
            i += 1

    return counts


def count_radix(array, radix):
    counts = [0 for _ in range(10)]
    for el in array:
        counts[(el // radix) % 10] += 1
    return counts


def rebuild_array(array, indices, radix):
    rebuilt_array = [0] * len(array)
    for i in range(len(array))[::-1]:
        digit = (array[i] // radix) % 10
        indices[digit] -= 1
        rebuilt_array[indices[digit]] = array[i]
    return rebuilt_array


def radix_sort(array):
    nb_rounds = len(str(np.max(array)))
    sorted_array = array.copy()
    radix = 1
    for i in range(nb_rounds):
        indices = np.cumsum(count_radix(sorted_array, radix=radix))
        sorted_array = rebuild_array(sorted_array, indices, radix=radix)
        radix *= 10
    return sorted_array


array = np.random.randint(low=0, high=10 ** 3, size=10)
print(list(array))
sorted_array = radix_sort(array)
print(sorted_array)
print("errors?:", list(map(int, [sorted_array[i] > sorted_array[i + 1] for i in range(len(sorted_array) - 1)])))

tot_errors = 0
bar = trange(1000)
for i in bar:
    array = np.random.randint(low=0, high=10 ** 6, size=10000)
    sorted_array = radix_sort(array)
    errors = sum(map(int, [sorted_array[i] > sorted_array[i + 1] for i in range(len(sorted_array) - 1)]))
    tot_errors += errors
    bar.set_description(f"errors -> {tot_errors}")
