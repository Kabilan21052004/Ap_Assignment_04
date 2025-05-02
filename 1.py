import threading
import time
import random

def merge_lists(list1, list2):
    merged = []
    i = j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            merged.append(list1[i])
            i += 1
        else:
            merged.append(list2[j])
            j += 1
    merged.extend(list1[i:])
    merged.extend(list2[j:])
    return merged

def recursive_merge_sort(data):
    if len(data) <= 1:
        return data
    midpoint = len(data) // 2
    left_half = recursive_merge_sort(data[:midpoint])
    right_half = recursive_merge_sort(data[midpoint:])
    return merge_lists(left_half, right_half)

class MergeSortThread(threading.Thread):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.result = []

    def run(self):
        self.result = recursive_merge_sort(self.data)

def threaded_merge_sort(data, thread_count=4):
    if len(data) <= 1:
        return data
    segment_length = len(data) // thread_count
    threads = []
    sorted_segments = []

    for i in range(thread_count):
        start = i * segment_length
        end = None if i == thread_count - 1 else (i + 1) * segment_length
        thread = MergeSortThread(data[start:end])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
        sorted_segments.append(thread.result)

    merged_result = sorted_segments[0]
    for segment in sorted_segments[1:]:
        merged_result = merge_lists(merged_result, segment)

    return merged_result

def create_random_list(length):
    return [random.randint(0, 10000) for _ in range(length)]

def evaluate_sorting_performance(length):
    sample = create_random_list(length)

    start = time.time()
    single_threaded_result = recursive_merge_sort(sample)
    single_threaded_duration = time.time() - start

    start = time.time()
    multi_threaded_result = threaded_merge_sort(sample)
    multi_threaded_duration = time.time() - start

    print(f"Single-threaded sort time: {single_threaded_duration:.4f} seconds")
    print(f"Multi-threaded sort time: {multi_threaded_duration:.4f} seconds")

evaluate_sorting_performance(100000)
