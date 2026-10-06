from __future__ import annotations

import socket
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class TcpProbe:
    host: str
    port: int
    latency_ms: float
    peer: tuple[str, int]


def tcp_connect(host: str, port: int, timeout: float = 3.0) -> TcpProbe:
    if not 1 <= port <= 65535:
        raise ValueError("Port must be between 1 and 65535")
    if timeout <= 0:
        raise ValueError("Timeout must be greater than zero")
    started = time.perf_counter()
    with socket.create_connection((host, port), timeout=timeout) as connection:
        peer = connection.getpeername()
    return TcpProbe(host, port, (time.perf_counter() - started) * 1000, peer)
