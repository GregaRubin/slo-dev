import time
import requests


class RateLimitedRequester:
    def __init__(
        self,
        min_interval_s: float,
        connect_timeout_s: float = 5,
        read_timeout_s: float = 20,
    ):
        self.min_interval_s = min_interval_s
        self.connect_timeout_s = connect_timeout_s
        self.read_timeout_s = read_timeout_s
        self._last_request_time = None

    def get(self, url, **kwargs):
        now = time.monotonic()

        if self._last_request_time is not None:
            elapsed = now - self._last_request_time
            sleep_time = self.min_interval_s - elapsed

            if sleep_time > 0:
                time.sleep(sleep_time)

        if "timeout" not in kwargs:
            kwargs["timeout"] = (self.connect_timeout_s, self.read_timeout_s)

        response = requests.get(url, **kwargs)
        self._last_request_time = time.monotonic()
        return response
