from __future__ import annotations

import argparse
import http.client
import json
import socket
import ssl
import time
from dataclasses import asdict, dataclass
from typing import Any, Callable, TypeVar


@dataclass(frozen=True)
class DiagnosticResult:
    layer: int
    check: str
    status: str
    duration_ms: float
    observed: Any = None
    error: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


T = TypeVar("T")


def _timed(layer: int, check: str, operation: Callable[[], T]) -> DiagnosticResult:
    started = time.perf_counter()
    try:
        observed = operation()
    except (OSError, ssl.SSLError, http.client.HTTPException) as error:
        return DiagnosticResult(
            layer=layer,
            check=check,
            status="ERROR",
            duration_ms=round((time.perf_counter() - started) * 1000, 2),
            error=f"{type(error).__name__}: {error}",
        )
    return DiagnosticResult(
        layer=layer,
        check=check,
        status="PASS",
        duration_ms=round((time.perf_counter() - started) * 1000, 2),
        observed=observed,
    )


def resolve_dns(host: str) -> DiagnosticResult:
    def operation() -> list[str]:
        records = socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
        return sorted({record[4][0] for record in records})

    return _timed(7, "dns-resolution", operation)


def check_tcp(host: str, port: int, timeout: float = 3.0) -> DiagnosticResult:
    if not 1 <= port <= 65535:
        raise ValueError("Port must be between 1 and 65535")
    if timeout <= 0:
        raise ValueError("Timeout must be greater than zero")

    def operation() -> dict[str, object]:
        with socket.create_connection((host, port), timeout=timeout) as connection:
            return {
                "peer": connection.getpeername(),
                "local": connection.getsockname(),
            }

    return _timed(4, f"tcp-connect-{port}", operation)


def inspect_tls(
    host: str,
    port: int = 443,
    timeout: float = 5.0,
    ca_file: str | None = None,
) -> DiagnosticResult:
    if not 1 <= port <= 65535:
        raise ValueError("Port must be between 1 and 65535")
    if timeout <= 0:
        raise ValueError("Timeout must be greater than zero")

    def operation() -> dict[str, object]:
        context = ssl.create_default_context(cafile=ca_file)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        with socket.create_connection((host, port), timeout=timeout) as raw_socket:
            with context.wrap_socket(raw_socket, server_hostname=host) as tls_socket:
                certificate = tls_socket.getpeercert()
                return {
                    "version": tls_socket.version(),
                    "cipher": tls_socket.cipher(),
                    "alpn": tls_socket.selected_alpn_protocol(),
                    "not_after": certificate.get("notAfter"),
                    "subject_alt_names": certificate.get("subjectAltName", ()),
                }

    return _timed(6, f"tls-handshake-{port}", operation)


def check_https(
    host: str,
    path: str = "/",
    timeout: float = 5.0,
    ca_file: str | None = None,
) -> DiagnosticResult:
    if not path.startswith("/"):
        raise ValueError("HTTP path must start with '/'")
    if timeout <= 0:
        raise ValueError("Timeout must be greater than zero")

    def operation() -> dict[str, object]:
        context = ssl.create_default_context(cafile=ca_file)
        connection = http.client.HTTPSConnection(
            host=host,
            timeout=timeout,
            context=context,
        )
        try:
            connection.request(
                "HEAD",
                path,
                headers={"User-Agent": "network-course-diagnostic/1.0"},
            )
            response = connection.getresponse()
            response.read()
            return {
                "status": response.status,
                "reason": response.reason,
                "content_type": response.getheader("Content-Type"),
                "server": response.getheader("Server"),
            }
        finally:
            connection.close()

    result = _timed(7, "https-head", operation)
    if result.status == "PASS" and result.observed["status"] >= 500:
        return DiagnosticResult(
            layer=result.layer,
            check=result.check,
            status="FAIL",
            duration_ms=result.duration_ms,
            observed=result.observed,
            error="Server returned a 5xx response",
        )
    return result


def diagnose_https(host: str, port: int = 443, path: str = "/") -> list[DiagnosticResult]:
    results = [resolve_dns(host), check_tcp(host, port)]
    if results[-1].status != "PASS":
        return results
    results.append(inspect_tls(host, port))
    if results[-1].status != "PASS":
        return results
    if port == 443:
        results.append(check_https(host, path))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run bounded DNS, TCP, TLS, and HTTPS diagnostics"
    )
    parser.add_argument("host", help="One authorized hostname to test")
    parser.add_argument("--port", type=int, default=443)
    parser.add_argument("--path", default="/")
    args = parser.parse_args()

    results = diagnose_https(args.host, args.port, args.path)
    print(json.dumps([result.to_dict() for result in results], indent=2))
    return 0 if results and all(result.status == "PASS" for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
