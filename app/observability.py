import logging
import time
from prometheus_client import Counter, Histogram

REQUESTS = Counter("agent_requests_total", "Total agent requests", ["route"])
LATENCY = Histogram("agent_request_latency_seconds", "Agent request latency", ["route"])

logger = logging.getLogger("agentic_ai")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")


class Timer:
    def __init__(self, route: str):
        self.route = route

    def __enter__(self):
        self.started = time.perf_counter()
        return self

    def __exit__(self, *_):
        elapsed = time.perf_counter() - self.started
        LATENCY.labels(self.route).observe(elapsed)
        logger.info("agent_request route=%s latency=%.3fs", self.route, elapsed)
