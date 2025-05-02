1. Multi-threaded Merge Sort

Overview:

The merge sort algorithm is adapted to leverage multi-threading by dividing the input list into two halves. Each half is sorted concurrently using separate threads, and the results are merged once both threads complete execution.

To maintain optimal performance, the number of threads is carefully managed to avoid overhead from excessive thread creation.

Note: Due to Python’s Global Interpreter Lock (GIL), threading may not yield significant performance improvements for CPU-bound tasks.

2. Multi-threaded Quick Sort

Overview:

In this approach, a pivot element is selected to partition the array into three segments: values less than the pivot, equal to the pivot, and greater than the pivot. Two threads are used to sort the left and right partitions in parallel during the early stages of recursion.

After reaching a predefined recursion depth (e.g., level 3), the algorithm switches to a single-threaded version of quicksort to avoid the overhead of managing too many threads.

3. Performance Comparison: Single-threaded vs Multi-threaded Execution

Methodology:

Performance was evaluated by measuring the execution time of both single-threaded and multi-threaded implementations.

For smaller datasets, the single-threaded version typically performs better due to lower overhead.

For larger datasets, multi-threading can offer modest improvements in execution time.

Important note: In Python, real performance gains for CPU-intensive operations are more effectively achieved using the multiprocessing module rather than threading, because of the GIL.
