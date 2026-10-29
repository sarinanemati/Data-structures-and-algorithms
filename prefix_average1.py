import time

def prefix_average1(S):
    n = len(S)
    A = [0] * n
    for j in range(n):
        A[j] = sum(S[0:j+1]) / (j + 1)
    return A

test_data = list(range(1000))

start_time = time.perf_counter()

result = prefix_average1(test_data)

end_time = time.perf_counter()

elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} s")
