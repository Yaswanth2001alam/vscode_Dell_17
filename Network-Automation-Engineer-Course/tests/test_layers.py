import socket
import ssl
import unittest
from unittest.mock import MagicMock, patch

from network_course.layer_diagnostics import (
    check_https,
    check_tcp,
    diagnose_https,
    inspect_tls,
    resolve_dns,
)
from network_course.protocol_catalog import (
    PROTOCOLS,
    Protocol,
    find_protocol,
    protocols_for_layer,
    validate_unique_names,
)


class ProtocolCatalogTests(unittest.TestCase):
    def test_every_layer_has_protocols(self):
        for layer in range(1, 8):
            with self.subTest(layer=layer):
                self.assertGreater(len(protocols_for_layer(layer)), 0)

    def test_catalog_names_are_unique(self):
        validate_unique_names()

    def test_find_protocol_is_case_insensitive(self):
        self.assertEqual(find_protocol("bgp").default_ports, (179,))

    def test_unknown_protocol_raises(self):
        with self.assertRaises(KeyError):
            find_protocol("not-a-protocol")

    def test_invalid_layer_and_port_are_rejected(self):
        with self.assertRaises(ValueError):
            protocols_for_layer(8)
        with self.assertRaises(ValueError):
            Protocol("Broken", (7,), "bad port", default_ports=(70000,))

    def test_catalog_is_comprehensive(self):
        self.assertGreaterEqual(len(PROTOCOLS), 40)


class DiagnosticTests(unittest.TestCase):
    @patch("network_course.layer_diagnostics.socket.getaddrinfo")
    def test_dns_returns_unique_sorted_addresses(self, getaddrinfo):
        getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("192.0.2.2", 0)),
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("192.0.2.1", 0)),
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("192.0.2.2", 0)),
        ]
        result = resolve_dns("example.test")
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.observed, ["192.0.2.1", "192.0.2.2"])

    @patch("network_course.layer_diagnostics.socket.getaddrinfo")
    def test_dns_error_is_not_reported_as_success(self, getaddrinfo):
        getaddrinfo.side_effect = socket.gaierror("not found")
        result = resolve_dns("missing.test")
        self.assertEqual(result.status, "ERROR")
        self.assertIn("gaierror", result.error)

    def test_tcp_rejects_invalid_port_and_timeout(self):
        with self.assertRaises(ValueError):
            check_tcp("example.test", 0)
        with self.assertRaises(ValueError):
            check_tcp("example.test", 443, timeout=0)

    @patch("network_course.layer_diagnostics.socket.create_connection")
    def test_tcp_reports_peer_and_local_endpoint(self, create_connection):
        connection = MagicMock()
        connection.getpeername.return_value = ("192.0.2.10", 443)
        connection.getsockname.return_value = ("192.0.2.20", 50000)
        create_connection.return_value.__enter__.return_value = connection

        result = check_tcp("example.test", 443)

        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.observed["peer"], ("192.0.2.10", 443))

    @patch("network_course.layer_diagnostics.ssl.create_default_context")
    @patch("network_course.layer_diagnostics.socket.create_connection")
    def test_tls_collects_negotiated_properties(self, create_connection, create_context):
        raw_socket = MagicMock()
        create_connection.return_value.__enter__.return_value = raw_socket
        tls_socket = MagicMock()
        tls_socket.version.return_value = "TLSv1.3"
        tls_socket.cipher.return_value = ("TLS_AES_256_GCM_SHA384", "TLSv1.3", 256)
        tls_socket.selected_alpn_protocol.return_value = "h2"
        tls_socket.getpeercert.return_value = {"notAfter": "Jan 1 00:00:00 2030 GMT"}
        context = create_context.return_value
        context.wrap_socket.return_value.__enter__.return_value = tls_socket

        result = inspect_tls("example.test")

        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.observed["version"], "TLSv1.3")
        context.wrap_socket.assert_called_once_with(
            raw_socket, server_hostname="example.test"
        )

    @patch("network_course.layer_diagnostics.http.client.HTTPSConnection")
    def test_https_5xx_is_application_failure(self, connection_class):
        response = MagicMock()
        response.status = 503
        response.reason = "Unavailable"
        response.getheader.return_value = None
        connection_class.return_value.getresponse.return_value = response

        result = check_https("example.test")

        self.assertEqual(result.status, "FAIL")
        self.assertEqual(result.observed["status"], 503)

    @patch("network_course.layer_diagnostics.inspect_tls")
    @patch("network_course.layer_diagnostics.check_tcp")
    @patch("network_course.layer_diagnostics.resolve_dns")
    def test_diagnosis_stops_after_transport_error(self, dns, tcp, tls):
        dns.return_value = MagicMock(status="PASS")
        tcp.return_value = MagicMock(status="ERROR")

        results = diagnose_https("example.test")

        self.assertEqual(len(results), 2)
        tls.assert_not_called()


if __name__ == "__main__":
    unittest.main()
