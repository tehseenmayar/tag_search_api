import requests
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
import torch


BASE_URL = "http://localhost:8000"
UPLOAD_ENDPOINT = f"{BASE_URL}/upload"
SEARCH_ENDPOINT = f"{BASE_URL}/search"
NUM_REQUESTS = 100


def time_request(func):
    start_time = time.time()
    response = func()
    end_time = time.time()
    return end_time - start_time, response.status_code


def upload_request():
    # Simulating file upload with some dummy data
    files = {'file': ('test.csv', b'dummy,data\n1,2\n3,4', 'text/csv')}
    return requests.post(UPLOAD_ENDPOINT, files=files)


def search_request():
    # Simulating search request with a query parameter
    params = {'query': 'test'}
    return requests.get(SEARCH_ENDPOINT, params=params)


def run_benchmark(request_func, num_requests):
    times = []
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_to_request = {executor.submit(time_request, request_func): i for i in range(num_requests)}
        for future in as_completed(future_to_request):
            time_taken, status_code = future.result()
            if status_code == 200:
                times.append(time_taken)
            else:
                print(f"Request failed with status code: {status_code}")

    return times


def print_stats(name, times):
    avg_time = statistics.mean(times)
    min_time = min(times)
    max_time = max(times)
    median_time = statistics.median(times)
    stddev_time = statistics.stdev(times)

    print(f"\n{name} API Call Statistics:")
    print(f"  Average time: {avg_time:.4f} seconds")
    print(f"  Minimum time: {min_time:.4f} seconds")
    print(f"  Maximum time: {max_time:.4f} seconds")
    print(f"  Median time:  {median_time:.4f} seconds")
    print(f"  Std Dev time: {stddev_time:.4f} seconds")


def main():
    print(f"Running benchmark with {NUM_REQUESTS} requests per endpoint...")

    upload_times = run_benchmark(upload_request, NUM_REQUESTS)
    search_times = run_benchmark(search_request, NUM_REQUESTS)

    print_stats("Upload", upload_times)
    print_stats("Search", search_times)


if __name__ == "__main__":
    if torch.cuda.is_available():
        print("API evaluation on GPU is in process")
        print(f"GPU device name: {torch.cuda.get_device_name(0)}")
    main()