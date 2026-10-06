"""
pytest fixtures for BGP neighbor validation testing.

Provides mock device objects and sample BGP data for testing.
"""

import pytest
from unittest.mock import Mock, MagicMock
from bgp_neighbor_validator import BGPNeighborValidator, BGPNeighborState


@pytest.fixture
def mock_device():
    """Create a mock Genie device."""
    device = Mock()
    device.name = "router1"
    device.connect = MagicMock()
    device.disconnect = MagicMock()
    device.parse = MagicMock()
    device.execute = MagicMock()
    return device


@pytest.fixture
def sample_bgp_output_ios_xe():
    """Sample parsed BGP output for Cisco IOS-XE."""
    return {
        "instance": {
            "default": {
                "vrf": {
                    "default": {
                        "neighbor": {
                            "192.168.1.1": {
                                "remote_as": 65000,
                                "session_state": "Established",
                                "up_down": "2w1d",
                                "prefixes": {
                                    "received": {"total_entries": 1024},
                                    "sent": {"total_entries": 512},
                                },
                            },
                            "192.168.1.2": {
                                "remote_as": 65001,
                                "session_state": "Established",
                                "up_down": "1w5d",
                                "prefixes": {
                                    "received": {"total_entries": 2048},
                                    "sent": {"total_entries": 256},
                                },
                            },
                            "192.168.1.3": {
                                "remote_as": 65002,
                                "session_state": "Down",
                                "up_down": "00:00:15",
                                "prefixes": {
                                    "received": {"total_entries": 0},
                                    "sent": {"total_entries": 0},
                                },
                            },
                            "192.168.1.4": {
                                "remote_as": 65003,
                                "session_state": "Active",
                                "up_down": "00:00:02",
                                "prefixes": {
                                    "received": {"total_entries": 0},
                                    "sent": {"total_entries": 0},
                                },
                            },
                        }
                    }
                }
            }
        }
    }


@pytest.fixture
def sample_bgp_output_multicast():
    """Sample parsed BGP output with multiple VRFs."""
    return {
        "instance": {
            "default": {
                "vrf": {
                    "default": {
                        "neighbor": {
                            "192.168.1.1": {
                                "remote_as": 65000,
                                "session_state": "Established",
                                "up_down": "2w1d",
                                "prefixes": {
                                    "received": {"total_entries": 100},
                                    "sent": {"total_entries": 50},
                                },
                            },
                        }
                    },
                    "management": {
                        "neighbor": {
                            "10.0.0.1": {
                                "remote_as": 65100,
                                "session_state": "Established",
                                "up_down": "1d2h",
                                "prefixes": {
                                    "received": {"total_entries": 10},
                                    "sent": {"total_entries": 5},
                                },
                            },
                        }
                    },
                }
            }
        }
    }


@pytest.fixture
def validator_with_mock(mock_device, sample_bgp_output_ios_xe):
    """Create a validator with mocked device."""
    mock_device.parse.return_value = sample_bgp_output_ios_xe
    validator = BGPNeighborValidator(mock_device)
    return validator, mock_device


@pytest.fixture
def mock_device_connection_failure():
    """Create a mock device that fails to connect."""
    device = Mock()
    device.name = "unreachable"
    device.connect = MagicMock(side_effect=Exception("Connection timeout"))
    return device


@pytest.fixture
def mock_device_parse_failure():
    """Create a mock device that fails to parse."""
    device = Mock()
    device.name = "router_parse_fail"
    device.connect = MagicMock()
    device.disconnect = MagicMock()
    device.parse = MagicMock(side_effect=Exception("Parse error"))
    device.execute = MagicMock(return_value="")
    return device
