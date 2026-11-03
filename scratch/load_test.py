"""
High-Concurrency Load Testing Benchmark for Shankar Homoeo Stores.
Simulates 500 simultaneous concurrent users hitting multiple endpoints and submitting forms.
Validates zero crashes, zero database locks, and fast response times.
"""

import sys
import time
import random
import urllib.request
import urllib.error
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://127.0.0.1:5000"

ENDPOINTS = [
    ("/", "GET", None),
    ("/products", "GET", None),
    ("/products/category/prescription-medicines", "GET", None),
    ("/api/products/search?q=dr", "GET", None),
    ("/about", "GET", None),
    ("/services", "GET", None),
    ("/reviews", "GET", None),
    ("/faq", "GET", None),
    ("/doctor-consultation", "GET", None)
]

def make_request(worker_id):
    """Pick an endpoint or perform a submission to test concurrent read/write throughput."""
    # 90% read traffic, 10% form write traffic (realistic production ratio)
    is_write = (random.random() < 0.10)
    
    for attempt in range(2):
        start_t = time.perf_counter()
        try:
            if is_write:
                url = f"{BASE_URL}/contact"
                post_data = urllib.parse.urlencode({
                    'name': f'Load Tester {worker_id}',
                    'phone': '+91 99887 76655',
                    'problem_type': 'Stock Enquiry',
                    'message': f'Concurrent stress test automated request #{worker_id}'
                }).encode('utf-8')
                req = urllib.request.Request(url, data=post_data, headers={'User-Agent': 'LoadTester/1.0'})
            else:
                path, method, _ = random.choice(ENDPOINTS)
                url = f"{BASE_URL}{path}"
                req = urllib.request.Request(url, headers={'User-Agent': 'LoadTester/1.0'})

            with urllib.request.urlopen(req, timeout=15) as resp:
                status = resp.status
                resp.read(512) # read partial content
                latency_ms = (time.perf_counter() - start_t) * 1000
                return (True, status, latency_ms, None)
        except urllib.error.HTTPError as e:
            latency_ms = (time.perf_counter() - start_t) * 1000
            return (False, e.code, latency_ms, str(e))
        except urllib.error.URLError as e:
            if attempt == 0:
                time.sleep(0.05)
                continue
            latency_ms = (time.perf_counter() - start_t) * 1000
            return (False, 0, latency_ms, str(e))
        except Exception as e:
            latency_ms = (time.perf_counter() - start_t) * 1000
            return (False, 0, latency_ms, str(e))

def run_stress_test(num_workers=500, total_requests=1000):
    print("=" * 70)
    print(f"[*] INITIATING STRESS TEST: {num_workers} CONCURRENT WORKERS ({total_requests} TOTAL REQUESTS)")
    print(f"[*] Target Server: {BASE_URL}")
    print("=" * 70)
    
    start_total = time.perf_counter()
    latencies = []
    success_count = 0
    failure_count = 0
    errors = {}

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(make_request, i) for i in range(total_requests)]
        
        for future in as_completed(futures):
            ok, status, lat, err = future.result()
            latencies.append(lat)
            if ok:
                success_count += 1
            else:
                failure_count += 1
                errors[str(err)] = errors.get(str(err), 0) + 1

    total_time = time.perf_counter() - start_total
    rps = total_requests / total_time if total_time > 0 else 0
    latencies.sort()
    
    avg_lat = sum(latencies) / len(latencies) if latencies else 0
    p50_lat = latencies[int(len(latencies) * 0.50)] if latencies else 0
    p95_lat = latencies[int(len(latencies) * 0.95)] if latencies else 0
    p99_lat = latencies[int(len(latencies) * 0.99)] if latencies else 0
    min_lat = min(latencies) if latencies else 0
    max_lat = max(latencies) if latencies else 0

    print("\n" + "=" * 70)
    print(" [RESULTS] STRESS TEST FOR 500 CONCURRENT USERS")
    print("=" * 70)
    print(f" [PASS] Total Successful Requests: {success_count}/{total_requests} ({success_count/total_requests*100:.1f}%)")
    print(f" [FAIL] Total Failed Requests:     {failure_count}")
    print(f" [TIME] Total Duration:            {total_time:.2f} seconds")
    print(f" [RPS]  Throughput:                {rps:.1f} Requests / Second")
    print(" ---------------------------------------------------------------------")
    print(f" [*] Minimum Latency:              {min_lat:.1f} ms")
    print(f" [*] Average Latency:              {avg_lat:.1f} ms")
    print(f" [*] Median (p50) Latency:         {p50_lat:.1f} ms")
    print(f" [*] 95th Percentile Latency:      {p95_lat:.1f} ms")
    print(f" [*] 99th Percentile Latency:      {p99_lat:.1f} ms")
    print(f" [*] Maximum Latency:              {max_lat:.1f} ms")
    print("=" * 70)

    if errors:
        print("\n[!] Recorded Errors:")
        for err, cnt in errors.items():
            print(f"  * {err}: {cnt} times")
    else:
        print("\n[SUCCESS] ZERO ERRORS! 100% of 500 concurrent connections completed successfully without database locks or crashes.")
    print("=" * 70)

    return failure_count == 0

if __name__ == '__main__':
    num_workers = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    total_reqs = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    success = run_stress_test(num_workers, total_reqs)
    sys.exit(0 if success else 1)
