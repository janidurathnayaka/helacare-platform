from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "helacare_http_requests_total",
    "Total HelaCare HTTP requests",
    ["method", "path", "status"],
)
REQUEST_LATENCY = Histogram(
    "helacare_http_request_duration_seconds",
    "HelaCare HTTP request latency",
    ["method", "path"],
)
CHAT_REQUESTS = Counter(
    "helacare_chat_requests_total",
    "Chat requests by language and triage level",
    ["language", "triage"],
)
