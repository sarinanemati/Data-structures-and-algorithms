import os
import sys
import time


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def draw_line(tick_length, tick_label=''):
    """Draw one line with given tick length (followed by optional label)."""
    line = '-' * tick_length
    if tick_label:
        line += ' ' + tick_label
    print(line)


def draw_interval(center_length):
    """Draw tick interval based upon a central tick length."""
    if center_length > 0:
        draw_interval(center_length - 1)
        draw_line(center_length)
        draw_interval(center_length - 1)


def draw_ruler(num_inches, major_length):
    """Draw English ruler with given number of inches, major tick length."""
    draw_line(major_length, '0')
    for j in range(1, 1 + num_inches):
        draw_interval(major_length - 1)
        draw_line(major_length, str(j))


def binary_search(data, target, low, high):
    """Return True if target is found in indicated portion of a Python list.

    The search only considers the portion from data[low] to data[high] inclusive.
    """
    if low > high:
        return False
    else:
        mid = (low + high) // 2
        if target == data[mid]:
            return True
        elif target < data[mid]:
            return binary_search(data, target, low, mid - 1)
        else:
            return binary_search(data, target, mid + 1, high)


def disk_usage(path):
    """Return the number of bytes used by a file/folder and any descendents."""
    total = os.path.getsize(path)
    if os.path.isdir(path):
        for filename in os.listdir(path):
            childpath = os.path.join(path, filename)
            total += disk_usage(childpath)

    print('{0:<7}'.format(total), path)
    return total


def bad_fibonacci(n):
    """Return the nth Fibonacci number."""
    if n <= 1:
        return n
    else:
        return bad_fibonacci(n - 2) + bad_fibonacci(n - 1)


def good_fibonacci(n):
    """Return pair of Fibonacci numbers, F(n) and F(n-1)."""
    if n <= 1:
        return (n, 0)
    else:
        (a, b) = good_fibonacci(n - 1)
        return (a + b, a)


def linear_sum(S, n):
    """Return the sum of the first n numbers of sequence S."""
    if n == 0:
        return 0
    else:
        return linear_sum(S, n - 1) + S[n - 1]


def reverse(S, start, stop):
    """Reverse elements in implicit slice S[start:stop]."""
    if start < stop - 1:
        S[start], S[stop - 1] = S[stop - 1], S[start]
        reverse(S, start + 1, stop - 1)


def format_time(seconds):
    if seconds < 1e-3:
        return f"{seconds * 1e6:.2f} microseconds"
    if seconds < 1:
        return f"{seconds * 1e3:.3f} milliseconds"
    return f"{seconds:.4f} seconds"


def run_timed(func, *args):
    """Run func(*args) once and return (result, elapsed seconds)."""
    start = time.perf_counter()
    result = func(*args)
    elapsed = time.perf_counter() - start
    return result, elapsed


def measure(func, n, repeats=100):
    """Run func(n) repeats times and return (result, average seconds)."""
    start = time.perf_counter()
    for _ in range(repeats):
        result = func(n)
    elapsed = (time.perf_counter() - start) / repeats
    return result, elapsed


def show_result(result):
    text = str(result)
    if len(text) > 30:
        return f"{text[:15]}...{text[-5:]}  ({len(text)} digits)"
    return text


def read_non_negative_int():
    try:
        n = int(input("Enter a non-negative integer n: "))
    except ValueError:
        print("Please enter a valid integer.")
        return None
    if n < 0:
        print("n must be non-negative.")
        return None
    return n


def factorial_iterative(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def bad_factorial(n):
    return n * bad_factorial(n - 1)


def compare_factorial():
    n = read_non_negative_int()
    if n is None:
        return

    print(f"\nRecursion limit in Python: {sys.getrecursionlimit()}")
    print(f"Computing {n}! (average of 100 runs)\n")

    try:
        res_rec, t_rec = measure(factorial, n)
        print(f"Recursive : {show_result(res_rec)}")
        print(f"            time = {format_time(t_rec)}")
    except RecursionError:
        res_rec, t_rec = None, None
        print("Recursive : RecursionError (n is too large for the recursion limit)")

    res_it, t_it = measure(factorial_iterative, n)
    print(f"Iterative : {show_result(res_it)}")
    print(f"            time = {format_time(t_it)}")

    if t_rec is not None:
        print(f"\nSame result? {res_rec == res_it}")
        if t_it > 0:
            print(f"Recursive is {t_rec / t_it:.2f}x the time of iterative")


def demo_bad_factorial():
    print("\nRunning bad_factorial(5) (no base case)...")
    start = time.perf_counter()
    try:
        bad_factorial(5)
    except RecursionError as e:
        print("RecursionError:", e)
    print(f"Time: {format_time(time.perf_counter() - start)}")


def factorial_menu():
    while True:
        print("\n--- Factorial Lab ---")
        print("1) Compare recursive vs iterative (with timing)")
        print("2) Show what happens with a bad factorial")
        print("0) Back")
        choice = input("Choose: ").strip()
        if choice == '1':
            compare_factorial()
        elif choice == '2':
            demo_bad_factorial()
        elif choice == '0':
            break
        else:
            print("Invalid choice.")


call_counter = 0


def bad_fibonacci_counted(n):
    global call_counter
    call_counter += 1
    if n <= 1:
        return n
    return bad_fibonacci_counted(n - 2) + bad_fibonacci_counted(n - 1)


def count_bad_calls(n):
    global call_counter
    call_counter = 0
    bad_fibonacci_counted(n)
    return call_counter


def good_fibonacci_value(n):
    return good_fibonacci(n)[0]


def compare_fibonacci():
    n = read_non_negative_int()
    if n is None:
        return

    if n > 40:
        ans = input(f"bad_fibonacci({n}) may take a VERY long time. "
                    "Run it anyway? (y/n): ").strip().lower()
        run_bad = (ans == 'y')
    else:
        run_bad = True

    print(f"\nComputing Fibonacci({n})\n")

    try:
        res_good, t_good = measure(good_fibonacci_value, n, repeats=1000)
    except RecursionError:
        print("Good fibonacci: RecursionError (n is too large for the recursion limit)")
        return
    print(f"Good fibonacci: {show_result(res_good)}")
    print(f"                time = {format_time(t_good)}")

    if run_bad:
        res_bad, t_bad = measure(bad_fibonacci, n, repeats=1)
        print(f"Bad fibonacci : {show_result(res_bad)}")
        print(f"                time = {format_time(t_bad)}")

        print(f"\nSame result? {res_good == res_bad}")
        if t_good > 0:
            print(f"Bad version is {t_bad / t_good:,.0f}x slower than good version")

        if n <= 30:
            print(f"Number of calls in bad_fibonacci({n}): {count_bad_calls(n):,}")
    else:
        print("Bad fibonacci: skipped")


def fibonacci_menu():
    while True:
        print("\n--- Fibonacci Lab ---")
        print("1) Compare bad vs good fibonacci (with timing)")
        print("0) Back")
        choice = input("Choose: ").strip()
        if choice == '1':
            compare_fibonacci()
        elif choice == '0':
            break
        else:
            print("Invalid choice.")


def run_book_examples():
    program_start = time.perf_counter()

    print("=== Factorial (Code Fragment 4.1) ===")
    for n in [0, 1, 5, 10]:
        result, t = run_timed(factorial, n)
        print(f"{n}! = {result}    [time: {format_time(t)}]")

    print("\n=== English Ruler (Code Fragment 4.2) ===")
    print("draw_ruler(3, 4):")
    _, t = run_timed(draw_ruler, 3, 4)
    print(f"[time: {format_time(t)}]")

    print("\n=== Binary Search (Code Fragment 4.3) ===")
    data = [2, 4, 5, 7, 8, 9, 12, 14, 17, 19, 22, 25, 27, 28, 33, 37]
    for target in [22, 23]:
        result, t = run_timed(binary_search, data, target, 0, len(data) - 1)
        print(f"search {target}: {result}    [time: {format_time(t)}]")

    print("\n=== Fibonacci (Code Fragments 4.7 and 4.8) ===")
    result, t = run_timed(bad_fibonacci, 10)
    print(f"bad_fibonacci(10)  = {result}    [time: {format_time(t)}]")
    result, t = run_timed(good_fibonacci_value, 10)
    print(f"good_fibonacci(10) = {result}    [time: {format_time(t)}]")

    print("\n=== Linear Sum (Code Fragment 4.9) ===")
    S = [4, 3, 6, 2, 8]
    result, t = run_timed(linear_sum, S, len(S))
    print(f"linear_sum({S}, {len(S)}) = {result}    [time: {format_time(t)}]")

    print("\n=== Reverse a Sequence (Code Fragment 4.10) ===")
    S = [4, 3, 6, 2, 8, 9, 5]
    print("before:", S)
    _, t = run_timed(reverse, S, 0, len(S))
    print("after :", S, f"   [time: {format_time(t)}]")

    total = time.perf_counter() - program_start
    print(f"\nTotal time for all book examples: {format_time(total)}")


def disk_usage_demo():
    path = input("Enter a path (press Enter for current directory): ").strip()
    if not path:
        path = '.'
    if not os.path.exists(path):
        print("Path does not exist.")
        return
    print()
    result, t = run_timed(disk_usage, path)
    print(f"\nTotal disk usage: {result} bytes")
    print(f"[time: {format_time(t)}]")


def main_menu():
    while True:
        print("\n===== Main Menu =====")
        print("1) Book examples (factorial, ruler, binary search, fibonacci, sum, reverse)")
        print("2) Disk usage")
        print("3) Factorial Lab (recursive vs iterative, timing)")
        print("4) Fibonacci Lab (bad vs good, timing)")
        print("0) Exit")
        choice = input("Choose: ").strip()
        if choice == '1':
            run_book_examples()
        elif choice == '2':
            disk_usage_demo()
        elif choice == '3':
            factorial_menu()
        elif choice == '4':
            fibonacci_menu()
        elif choice == '0':
            break
        else:
            print("Invalid choice.")


if __name__ == '__main__':
    main_menu()
