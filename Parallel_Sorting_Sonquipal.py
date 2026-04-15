import random
import time
from multiprocessing import Process, Queue

def generate_data(n):
    return [random.randint(1, 1000000) for _ in range(n)]

# Merge
def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Sequential merge sort
def merge_sort(data):
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left = merge_sort(data[:mid])
    right = merge_sort(data[mid:])

    return merge(left, right)

# Worker
def worker(sub_data, q):
    sorted_sub = merge_sort(sub_data)
    q.put(sorted_sub)

# Parallel sorting
def parallel_sort(data):
    processes = []
    q = Queue()

    chunk_size = len(data) // 4
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    for chunk in chunks:
        p = Process(target=worker, args=(chunk, q))
        processes.append(p)
        p.start()

    # Results
    sorted_chunks = []
    for _ in processes:
        sorted_chunks.append(q.get())

    for p in processes:
        p.join()

    # Merge all sorted chunks
    while len(sorted_chunks) > 1:
        left = sorted_chunks.pop(0)
        right = sorted_chunks.pop(0)
        sorted_chunks.append(merge(left, right))

    return sorted_chunks[0]

# Test
def test_parallel(size):
    data = generate_data(size)

    print(f"\nParallel sorting {size} elements...")

    start = time.time()
    sorted_data = parallel_sort(data)
    end = time.time()

    print(f"Time taken: {end - start:.4f} seconds")
    print("Sorted correctly:", sorted_data == sorted(data))


if __name__ == "__main__":
    test_parallel(1000)        # Small
    test_parallel(100000)      # Medium