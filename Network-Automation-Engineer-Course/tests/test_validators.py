import unittest

from network_course.models import CheckStatus
from network_course.protocol_checks import demo_checks, report
from network_course.validators import (
    adjacency_state,
    all_passed,
    bgp_prefix_count,
    counter_delta,
    exact_neighbor_set,
    lacp_member,
    macsec_health,
    required_and_forbidden_prefixes,
)


class NeighborTests(unittest.TestCase):
    def test_exact_neighbor_set_passes(self):
        result = exact_neighbor_set("ospf", ["r2", "r3"], ["r3", "r2"])
        self.assertTrue(result.passed)

    def test_exact_neighbor_set_reports_missing_and_unexpected(self):
        result = exact_neighbor_set("lldp", ["leaf02"], ["unknown-switch"])
        self.assertEqual(result.status, CheckStatus.FAIL)
        self.assertIn("missing=['leaf02']", result.detail)
        self.assertIn("unexpected=['unknown-switch']", result.detail)

    def test_adjacency_is_case_insensitive(self):
        result = adjacency_state("bgp", "192.0.2.2", "Established", {"ESTABLISHED"})
        self.assertTrue(result.passed)


class BgpPolicyTests(unittest.TestCase):
    def test_prefix_count_boundaries(self):
        for value in (1, 500):
            with self.subTest(value=value):
                self.assertTrue(bgp_prefix_count("peer", value, 1, 500).passed)
        for value in (0, 501):
            with self.subTest(value=value):
                self.assertFalse(bgp_prefix_count("peer", value, 1, 500).passed)

    def test_invalid_threshold_is_rejected(self):
        with self.assertRaises(ValueError):
            bgp_prefix_count("peer", 5, 10, 1)

    def test_required_and_forbidden_routes(self):
        results = required_and_forbidden_prefixes(
            "internet",
            observed=["203.0.113.1/24", "10.0.0.0/8"],
            required=["203.0.113.0/24"],
            forbidden=["10.0.0.0/8"],
        )
        self.assertTrue(results[0].passed)
        self.assertFalse(results[1].passed)
        self.assertEqual(results[1].observed, ["10.0.0.0/8"])


class LinkSecurityTests(unittest.TestCase):
    def test_lacp_requires_forwarding_flags(self):
        result = lacp_member(
            "Ethernet1",
            {
                "synchronized": True,
                "collecting": True,
                "distributing": False,
            },
        )
        self.assertFalse(result.passed)
        self.assertIn("distributing", result.detail)

    def test_macsec_checks_session_traffic_and_integrity(self):
        results = macsec_health(
            "Ethernet1",
            secured=True,
            encrypted_packets=100,
            invalid_icv_packets=1,
            replay_drops=0,
        )
        self.assertEqual(
            [item.status for item in results],
            [CheckStatus.PASS, CheckStatus.PASS, CheckStatus.FAIL],
        )

    def test_counter_decrease_is_collection_error(self):
        result = counter_delta("interface-errors", before=100, after=5)
        self.assertEqual(result.status, CheckStatus.ERROR)


class ReportTests(unittest.TestCase):
    def test_demo_report_passes_and_is_nonempty(self):
        output = report(demo_checks())
        self.assertTrue(output["passed"])
        self.assertGreater(output["summary"]["PASS"], 5)

    def test_all_passed_rejects_empty_results(self):
        self.assertFalse(all_passed([]))


if __name__ == "__main__":
    unittest.main()

