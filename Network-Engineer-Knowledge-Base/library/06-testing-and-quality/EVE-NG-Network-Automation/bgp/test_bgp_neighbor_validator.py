"""
Tests for BGP Neighbor Validator

Comprehensive test suite for BGP neighbor validation functionality.
"""

import pytest
from bgp_neighbor_validator import (
    BGPNeighborValidator,
    BGPNeighborState,
    BGPValidationResult,
    BGPNeighbor,
)


class TestBGPNeighborState:
    """Test BGPNeighborState enum."""
    
    def test_established_state(self):
        assert BGPNeighborState.ESTABLISHED.value == "Established"
    
    def test_down_state(self):
        assert BGPNeighborState.DOWN.value == "Down"
    
    def test_all_states_exist(self):
        expected_states = [
            "Established", "Active", "Connect", "OpenConfirm",
            "OpenSent", "Idle", "Down", "Unknown"
        ]
        actual_states = [s.value for s in BGPNeighborState]
        assert set(actual_states) == set(expected_states)


class TestBGPNeighbor:
    """Test BGPNeighbor dataclass."""
    
    def test_create_neighbor(self):
        neighbor = BGPNeighbor(
            ip_address="192.168.1.1",
            remote_as=65000,
            state=BGPNeighborState.ESTABLISHED,
            prefixes_received=1024,
        )
        assert neighbor.ip_address == "192.168.1.1"
        assert neighbor.remote_as == 65000
        assert neighbor.state == BGPNeighborState.ESTABLISHED
    
    def test_neighbor_is_healthy_when_established(self):
        neighbor = BGPNeighbor(
            ip_address="192.168.1.1",
            remote_as=65000,
            state=BGPNeighborState.ESTABLISHED,
        )
        assert neighbor.is_healthy() is True
    
    def test_neighbor_not_healthy_when_down(self):
        neighbor = BGPNeighbor(
            ip_address="192.168.1.1",
            remote_as=65000,
            state=BGPNeighborState.DOWN,
        )
        assert neighbor.is_healthy() is False
    
    def test_neighbor_not_healthy_when_idle(self):
        neighbor = BGPNeighbor(
            ip_address="192.168.1.1",
            remote_as=65000,
            state=BGPNeighborState.IDLE,
        )
        assert neighbor.is_healthy() is False


class TestBGPValidationResult:
    """Test BGPValidationResult dataclass."""
    
    def test_create_result(self):
        result = BGPValidationResult(device_name="router1")
        assert result.device_name == "router1"
        assert result.total_neighbors == 0
        assert result.established_count == 0
    
    def test_status_summary(self):
        result = BGPValidationResult(device_name="router1", vrf="default")
        result.total_neighbors = 4
        result.established_count = 3
        result.down_count = 1
        result.error_neighbors = 0
        
        summary = result.get_status_summary()
        assert "router1" in summary
        assert "Total=4" in summary
        assert "Established=3" in summary
        assert "Down=1" in summary
    
    def test_get_unhealthy_neighbors(self):
        result = BGPValidationResult(device_name="router1")
        result.neighbors = [
            BGPNeighbor("192.168.1.1", 65000, BGPNeighborState.ESTABLISHED),
            BGPNeighbor("192.168.1.2", 65001, BGPNeighborState.DOWN),
            BGPNeighbor("192.168.1.3", 65002, BGPNeighborState.IDLE),
        ]
        
        unhealthy = result.get_unhealthy_neighbors()
        assert len(unhealthy) == 2
        assert all(not n.is_healthy() for n in unhealthy)
    
    def test_to_dict(self):
        result = BGPValidationResult(device_name="router1", vrf="default")
        result.neighbors = [
            BGPNeighbor(
                "192.168.1.1", 65000, BGPNeighborState.ESTABLISHED,
                prefixes_received=100, prefixes_advertised=50
            ),
        ]
        result.total_neighbors = 1
        result.established_count = 1
        
        result_dict = result.to_dict()
        assert result_dict["device_name"] == "router1"
        assert result_dict["total_neighbors"] == 1
        assert len(result_dict["neighbors"]) == 1
        assert result_dict["neighbors"][0]["ip_address"] == "192.168.1.1"


class TestBGPNeighborValidator:
    """Test BGPNeighborValidator class."""
    
    def test_validator_initialization(self, mock_device):
        validator = BGPNeighborValidator(mock_device, vrf="default")
        assert validator.device == mock_device
        assert validator.vrf == "default"
    
    def test_parse_state_established(self, validator_with_mock):
        validator, _ = validator_with_mock
        state = validator._parse_state("Established")
        assert state == BGPNeighborState.ESTABLISHED
    
    def test_parse_state_down(self, validator_with_mock):
        validator, _ = validator_with_mock
        state = validator._parse_state("Down")
        assert state == BGPNeighborState.DOWN
    
    def test_parse_state_case_insensitive(self, validator_with_mock):
        validator, _ = validator_with_mock
        state = validator._parse_state("IDLE")
        assert state == BGPNeighborState.IDLE
    
    def test_parse_state_unknown(self, validator_with_mock):
        validator, _ = validator_with_mock
        state = validator._parse_state("InvalidState")
        assert state == BGPNeighborState.UNKNOWN
    
    def test_validate_neighbors_success(self, validator_with_mock, sample_bgp_output_ios_xe):
        validator, mock_device = validator_with_mock
        mock_device.parse.return_value = sample_bgp_output_ios_xe
        
        result = validator.validate_neighbors()
        
        assert result.device_name == "router1"
        assert result.total_neighbors == 4
        assert result.established_count == 2
        assert result.down_count == 1
        assert result.error_neighbors == 1
    
    def test_validate_neighbors_with_multiple_vrfs(self, mock_device, sample_bgp_output_multicast):
        mock_device.parse.return_value = sample_bgp_output_multicast
        
        # Validate default VRF
        validator = BGPNeighborValidator(mock_device, vrf="default")
        result = validator.validate_neighbors()
        
        assert result.total_neighbors == 1
        assert result.vrf == "default"
    
    def test_validate_specific_neighbor_found(self, validator_with_mock, sample_bgp_output_ios_xe):
        validator, mock_device = validator_with_mock
        mock_device.parse.return_value = sample_bgp_output_ios_xe
        
        neighbor = validator.validate_specific_neighbor("192.168.1.1")
        
        assert neighbor is not None
        assert neighbor.ip_address == "192.168.1.1"
        assert neighbor.remote_as == 65000
        assert neighbor.is_healthy()
    
    def test_validate_specific_neighbor_not_found(self, validator_with_mock, sample_bgp_output_ios_xe):
        validator, mock_device = validator_with_mock
        mock_device.parse.return_value = sample_bgp_output_ios_xe
        
        neighbor = validator.validate_specific_neighbor("10.0.0.1")
        assert neighbor is None
    
    def test_validate_neighbors_parse_failure_with_fallback(self, mock_device):
        mock_device.parse.side_effect = Exception("Parse error")
        mock_device.execute.return_value = "show ip bgp summary output"
        
        validator = BGPNeighborValidator(mock_device)
        result = validator.validate_neighbors()
        
        # Should handle gracefully
        assert result.device_name == "router1"
        assert result.total_neighbors == 0
    
    def test_validate_neighbors_full_failure(self, mock_device):
        mock_device.parse.side_effect = Exception("Parse error")
        mock_device.execute.side_effect = Exception("Execute error")
        
        validator = BGPNeighborValidator(mock_device)
        result = validator.validate_neighbors()
        
        assert len(result.errors) > 0
        assert result.total_neighbors == 0
    
    def test_parse_neighbor_data_extraction(self, validator_with_mock):
        validator, _ = validator_with_mock
        
        nbr_info = {
            "remote_as": 65000,
            "session_state": "Established",
            "up_down": "2w1d",
            "prefixes": {
                "received": {"total_entries": 1024},
                "sent": {"total_entries": 512},
            },
        }
        
        neighbor = validator._parse_neighbor_data("192.168.1.1", nbr_info)
        
        assert neighbor.ip_address == "192.168.1.1"
        assert neighbor.remote_as == 65000
        assert neighbor.state == BGPNeighborState.ESTABLISHED
        assert neighbor.prefixes_received == 1024
        assert neighbor.prefixes_advertised == 512
    
    def test_calculate_metrics(self, validator_with_mock):
        validator, _ = validator_with_mock
        
        result = BGPValidationResult(device_name="router1")
        result.neighbors = [
            BGPNeighbor("192.168.1.1", 65000, BGPNeighborState.ESTABLISHED),
            BGPNeighbor("192.168.1.2", 65001, BGPNeighborState.ESTABLISHED),
            BGPNeighbor("192.168.1.3", 65002, BGPNeighborState.DOWN),
            BGPNeighbor("192.168.1.4", 65003, BGPNeighborState.ACTIVE),
        ]
        
        validator._calculate_metrics(result)
        
        assert result.total_neighbors == 4
        assert result.established_count == 2
        assert result.down_count == 1
        assert result.error_neighbors == 1


class TestBGPIntegration:
    """Integration tests."""
    
    def test_full_validation_workflow(self, validator_with_mock, sample_bgp_output_ios_xe):
        validator, mock_device = validator_with_mock
        mock_device.parse.return_value = sample_bgp_output_ios_xe
        
        result = validator.validate_neighbors()
        
        # Verify complete workflow
        assert not result.errors
        assert result.total_neighbors == 4
        assert result.established_count == 2
        
        # Check unhealthy neighbors
        unhealthy = result.get_unhealthy_neighbors()
        assert len(unhealthy) == 2
        
        # Verify dict conversion
        result_dict = result.to_dict()
        assert result_dict["total_neighbors"] == 4
        assert len(result_dict["neighbors"]) == 4
