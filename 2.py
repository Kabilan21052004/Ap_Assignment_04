import threading
import time
import random

def quick_sort(data):
    if len(data) <= 1:
        return data
    pivot_element = data[len(data) // 2]
    smaller = [item for item in data if item < pivot_element]
    equal = [item for item in data if item == pivot_element]
    greater = [item for item in data if item > pivot_element]
    return quick_sort(smaller) + equal + quick_sort(greater)

class QuicksortThread(threading.Thread):
    def __init__(self, segment):
        super().__init__()
        self.segment = segment
        self.result = []

    def run(self):
        self.result = quick_sort(self.segment)

def parallel_quick_sort(data, threads_limit=2):
    if len(data) <= 1:
        return data
    pivot_value = data[len(data) // 2]
    lower_part = [val for val in data if val < pivot_value]
    upper_part = [val for val in data if val > pivot_value]

    active_threads = []
    if lower_part:
        thread_low = QuicksortThread(lower_part)
        active_threads.append(thread_low)
        thread_low.start()
    else:
        thread_low = None

    if upper_part:
        thread_high = QuicksortThread(upper_part)
        active_threads.append(thread_high)
        thread_high.start()
    else:
        thread_high = None

    for t in active_threads:
        t.join()

    sorted_data = []
    if thread_low:
        sorted_data += thread_low.result
    sorted_data += [pivot_value] * data.count(pivot_value)
    if thread_high:
        sorted_data += thread_high.result

    return sorted_data

def generate_random_data(length):
    return [random.randint(0, 10000) for _ in range(length)]

def test_sorting_methods(length):
    sample_data = generate_random_data(length)

    start = time.time()
    result_single = quick_sort(sample_data)
    time_single = time.time() - start

    start = time.time()
    result_multi = parallel_quick_sort(sample_data)
    time_multi = time.time() - start

    print(f"Single-threaded sort time: {time_single:.4f} seconds")
    print(f"Multi-threaded sort time: {time_multi:.4f} seconds")

test_sorting_methods(100000)
