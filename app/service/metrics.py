from prometheus_client import Counter, Histogram

""" 
    Purpose: Counts every HTTP request handled by the service.
    Returns: Labels that allow slicing by HTTP method, endpoint, and response status for traffic analysis, error rate monitoring, and alerting.
    
"""

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests processed by the service",
    ["method", "endpoint", "status"]
)

""" 
    Purpose: Measures end-to-end request latency.
    Returns: A Histogram that enables percentile calculations (p50, p95, p99) which are critical for SLOs and performance metrics..
    
"""

REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds",
    "End-to-end latency of HTTP requests in seconds",
    ["endpoint"]
)

""" 
    Purpose: Tracks the number of Roman numeral conversions performed.
    Returns: The 'type' of label and allows for single-value requests and range-based batch conversions.
    
"""

CONVERSION_COUNT = Counter(
    "roman_conversions_total",
    "Total number of Roman numeral conversions performed",
    ["type"]  # Expected values: "single" | "range"
)
