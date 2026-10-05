import unittest

from network_course.models import CheckResult, CheckStatus, Device, load_devices


class DeviceTests(unittest.TestCase):
    def test_device_accepts_ipv4_and_ipv6(self):
        ipv4 = Device("r1", "192.0.2.1", "ios", "edge", "lab")
        ipv6 = Device("r2", "2001:db8::2", "junos", "core", "lab", port=830)
        self.assertEqual(ipv4.port, 22)
        self.assertEqual(ipv6.port, 830)

    def test_device_rejects_invalid_address(self):
        with self.assertRaisesRegex(ValueError, "invalid host"):
            Device("r1", "999.2.3.4", "ios", "edge", "lab")

    def test_device_rejects_invalid_port(self):
        with self.assertRaisesRegex(ValueError, "invalid TCP port"):
            Device("r1", "192.0.2.1", "ios", "edge", "lab", port=0)

    def test_load_devices_rejects_duplicate_endpoint(self):
        data = {
            "schema_version": 1,
            "devices": {
                "r1": {
                    "host": "192.0.2.1",
                    "platform": "ios",
                    "role": "edge",
                    "site": "lab",
                },
                "r2": {
                    "host": "192.0.2.1",
                    "platform": "ios",
                    "role": "edge",
                    "site": "lab",
                },
            },
        }
        with self.assertRaisesRegex(ValueError, "share endpoint"):
            load_devices(data)

    def test_load_devices_rejects_unknown_field(self):
        data = {
            "schema_version": 1,
            "devices": {
                "r1": {
                    "host": "192.0.2.1",
                    "platform": "ios",
                    "role": "edge",
                    "site": "lab",
                    "password": "must-not-be-here",
                }
            },
        }
        with self.assertRaisesRegex(ValueError, "unknown fields"):
            load_devices(data)


class ResultTests(unittest.TestCase):
    def test_result_serializes_enum_value(self):
        result = CheckResult("example", CheckStatus.PASS, True, True)
        self.assertTrue(result.passed)
        self.assertEqual(result.to_dict()["status"], "PASS")


if __name__ == "__main__":
    unittest.main()

