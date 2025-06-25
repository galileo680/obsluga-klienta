"""Discrete‑event FCFS queue simulator (M/M/s) BEZ biblioteki SimPy.

Algorytm:
  1. Generuj czasy przyjść klienta wg rozkładu Poissona (inter‑arrival ~ Exp(lambda_rate)).
  2. Dla każdego klienta:
       • wybierz serwer z najwcześniejszym momentem dostępności,
       • start obsługi = max(arrival, next_free[serwer]),
       • czas obsługi ~ Exp(mu),
       • zakończenie = start + service_time,
       • zaktualizuj czas dostępności serwera.
  3. Zapisz statystyki: wait_time, service_time, system_time.
"""
from __future__ import annotations
import random
import heapq
from dataclasses import dataclass, asdict
import pandas as pd

@dataclass
class Record:
    customer_id: int
    arrive: float
    start: float
    depart: float
    wait_time: float
    service_time: float
    system_time: float

    def asdict(self):
        return asdict(self)


class MMSSimulator:
    def __init__(self, lambda_rate: float, mu: float, n_servers: int = 1, seed: int | None = None):
        if lambda_rate <= 0 or mu <= 0:
            raise ValueError("Rates must be positive.")
        self.lambda_rate = lambda_rate
        self.mu = mu
        self.n_servers = n_servers
        self.rng = random.Random(seed)

    def _exp(self, rate: float) -> float:
        return self.rng.expovariate(rate)

    def run(self, sim_time: float) -> pd.DataFrame:
        """Run simulation for `sim_time` (time units) and return DataFrame z rekordami klientów."""
        # Generuj przyjścia
        arrivals: list[float] = []
        t = self._exp(self.lambda_rate)
        while t < sim_time:
            arrivals.append(t)
            t += self._exp(self.lambda_rate)
  

        # Kolejka serwerów: Struktura to krotka -> (next_free_time, server_id)
        servers_heap: list[tuple[float, int]] = [(0.0, i) for i in range(self.n_servers)]
        heapq.heapify(servers_heap)

        records: list[Record] = []

        for cid, arrive_time in enumerate(arrivals):
            next_free_time, server_id = heapq.heappop(servers_heap)
            start_service = max(arrive_time, next_free_time)
            service_time = self._exp(self.mu)
            depart_time = start_service + service_time

            # zaktualizuj serwer
            heapq.heappush(servers_heap, (depart_time, server_id))

            records.append(Record(
                customer_id=cid,
                arrive=arrive_time,
                start=start_service,
                depart=depart_time,
                wait_time=start_service - arrive_time,
                service_time=service_time,
                system_time=depart_time - arrive_time
            ))

        return pd.DataFrame([r.asdict() for r in records])
