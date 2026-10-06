import json
import os
import tempfile
import unittest
from pathlib import Path

import lab_automation


class LabAutomationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.devices = lab_automation.load_inventory()

    def test_inventory_has_expected_topology(self):
        self.assertEqual(set(self.devices), {"R1", "R2", "R3"})
        self.assertEqual([link["peer"] for link in self.devices["R2"]["links"]], ["R1", "R3"])

    def test_ospf_plan_enables_only_transit_interfaces(self):
        config = lab_automation.scenario_config("ospf", self.devices["R2"], self.devices)
        self.assertIn(" passive-interface default", config)
        self.assertIn(" no passive-interface Ethernet1/1", config)
        self.assertIn(" no passive-interface Ethernet1/2", config)
        self.assertEqual(config.count(" ip ospf network point-to-point"), 2)

    def test_ebgp_uses_peer_as_numbers(self):
        config = lab_automation.ebgp_config(self.devices["R2"], self.devices)
        self.assertIn(" neighbor 10.12.0.1 remote-as 65001", config)
        self.assertIn(" neighbor 10.23.0.2 remote-as 65003", config)

    def test_bgp_only_does_not_touch_interfaces_or_ospf(self):
        config = lab_automation.scenario_config(
            "bgp-only", self.devices["R2"], self.devices
        )
        self.assertTrue(config[0].startswith("router bgp "))
        self.assertFalse(any(command.startswith("interface ") for command in config))
        self.assertFalse(any("router ospf" in command for command in config))

    def test_ibgp_r2_is_route_reflector(self):
        config = lab_automation.ibgp_rr_config(self.devices["R2"], self.devices)
        self.assertIn(" neighbor 10.255.0.1 route-reflector-client", config)
        self.assertIn(" neighbor 10.255.0.3 route-reflector-client", config)

    def test_plan_runs_without_netmiko_or_credentials(self):
        with tempfile.TemporaryDirectory() as directory:
            exit_code = lab_automation.main(
                ["plan", "--scenario", "ospf-ebgp", "--output-dir", directory]
            )
            self.assertEqual(exit_code, 0)
            reports = list(Path(directory).glob("*.json"))
            self.assertEqual(len(reports), 1)
            self.assertEqual(len(json.loads(reports[0].read_text())), 3)

    def test_load_env_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".env"
            path.write_text("TEST_LAB_VALUE='loaded'\n", encoding="utf-8")
            os.environ.pop("TEST_LAB_VALUE", None)
            lab_automation.load_env_file(path)
            self.assertEqual(os.environ.pop("TEST_LAB_VALUE"), "loaded")


if __name__ == "__main__":
    unittest.main()
