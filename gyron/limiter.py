import asyncio
import time


class Limiter:

    def __init__(self, limit: int, rate : int):

        if limit <= 0:
            raise ValueError("limit must be greater than zero.")

        if rate <= 0:
            raise ValueError("rate must be greater than zero.")
        
        self.capacity = limit
        self.rate = rate

        self.tokens = limit
        self.updated_at = time.monotonic()

        self.lock = asyncio.Lock()


    async def acquire(self):

        while True:

            async with self.lock:

                now = time.monotonic()

                elapsed = now - self.updated_at

                self.tokens = min(
                    self.capacity,
                    self.tokens + elapsed * self.rate
                )

                self.updated_at = now


                if self.tokens >= 1:
                    self.tokens -= 1
                    return


                wait_time = (1 - self.tokens) / self.rate


            await asyncio.sleep(wait_time)