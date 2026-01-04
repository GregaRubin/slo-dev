import time
import requests

class RateLimitedRequester:
    def __init__(self, min_interval_s: float):
        self.min_interval_s = min_interval_s
        self._last_request_time = None

    def get(self, url, **kwargs):
        now = time.monotonic()

        if self._last_request_time is not None:
            elapsed = now - self._last_request_time
            sleep_time = self.min_interval_s - elapsed

            if sleep_time > 0:
                time.sleep(sleep_time)

        response = requests.get(url, **kwargs)
        self._last_request_time = time.monotonic()
        return response
