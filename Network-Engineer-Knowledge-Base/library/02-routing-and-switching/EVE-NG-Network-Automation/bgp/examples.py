#!/usr/bin/env python3
"""
BGP Automation - Usage Examples

Demonstrates various ways to use the BGP neighbor validation workflow.
"""

# ============================================================================
# EXAMPLE 1: Simple Validation Script
# ============================================================================

def example_1_simple_validation():
    """Basic BGP neighbor validation."""
    from genie.testbed import load
    from bgp.bgp_neighbor_validator import BGPNeighborValidator
    
    # Load testbed
    testbed = load("testbed.yaml")
    device = testbed.devices["router1"]
    device.connect()
    
    try:
        # Create validator and validate
        validator = BGPNeighborValidator(device, vrf="default")
        result = validator.validate_neighbors()
        
        # Print summary
        print(result.get_status_summary())
        
    finally:
        device.disconnect()


# ============================================================================
# EXAMPLE 2: Error Detection and Alerting
# ============================================================================

def example_2_error_detection():
    """Detect and alert on BGP issues."""
    from genie.testbed import load
    from bgp.bgp_neighbor_validator import BGPNeighborValidator, BGPNeighborState
    
    testbed = load("testbed.yaml")
    device = testbed.devices["router1"]
    device.connect()
    
    try:
        validator = BGPNeighborValidator(device)
        result = validator.validate_neighbors()
        
        # Alert on down neighbors
        if result.down_count > 0:
            print("⚠ ALERT: BGP neighbors are down!")
            for neighbor in result.get_unhealthy_neighbors():
                print(f"  - {neighbor.ip_address}: {neighbor.state.value}")
        
        # Check for incomplete connections
        for neighbor in result.neighbors:
            if neighbor.state in [BGPNeighborState.ACTIVE, BGPNeighborState.IDLE]:
                print(f"⚠ WARNING: {neighbor.ip_address} not established")
        
        # Verify expected neighbors exist
        expected_neighbors = {"192.168.1.1", "192.168.1.2"}
        found_neighbors = {n.ip_address for n in result.neighbors}
        missing = expected_neighbors - found_neighbors
        if missing:
            print(f"⚠ WARNING: Expected neighbors missing: {missing}")
        
    finally:
        device.disconnect()


# ============================================================================
# EXAMPLE 3: Multi-Device Validation with JSON Report
# ============================================================================

def example_3_multi_device_report():
    """Validate multiple devices and generate JSON report."""
    import json
    from datetime import datetime
    from genie.testbed import load
    from bgp.bgp_neighbor_validator import BGPNeighborValidator
    
    testbed = load("testbed.yaml")
    
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "devices": []
    }
    
    for device_name, device in testbed.devices.items():
        device.connect()
        try:
            validator = BGPNeighborValidator(device)
            result = validator.validate_neighbors()
            report["devices"].append(result.to_dict())
        finally:
            device.disconnect()
    
    # Save report
    with open("bgp_validation_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"Report saved to bgp_validation_report.json")


# ============================================================================
# EXAMPLE 4: Specific Neighbor Validation
# ============================================================================

def example_4_specific_neighbor():
    """Validate a specific neighbor."""
    from genie.testbed import load
    from bgp.bgp_neighbor_validator import BGPNeighborValidator
    
    testbed = load("testbed.yaml")
    device = testbed.devices["router1"]
    device.connect()
    
    try:
        validator = BGPNeighborValidator(device)
        
        # Check specific neighbor
        neighbor_ip = "192.168.1.1"
        neighbor = validator.validate_specific_neighbor(neighbor_ip)
        
        if neighbor is None:
            print(f"Neighbor {neighbor_ip} not found")
        elif neighbor.is_healthy():
            print(f"✓ {neighbor_ip} is healthy")
            print(f"  AS: {neighbor.remote_as}")
            print(f"  Uptime: {neighbor.uptime}")
            print(f"  Prefixes RX: {neighbor.prefixes_received}")
            print(f"  Prefixes TX: {neighbor.prefixes_advertised}")
        else:
            print(f"✗ {neighbor_ip} is unhealthy: {neighbor.state.value}")
        
    finally:
        device.disconnect()


# ============================================================================
# EXAMPLE 5: VRF-Specific Validation
# ============================================================================

def example_5_vrf_validation():
    """Validate BGP in specific VRF."""
    from genie.testbed import load
    from bgp.bgp_neighbor_validator import BGPNeighborValidator
    
    testbed = load("testbed.yaml")
    device = testbed.devices["router1"]
    device.connect()
    
    try:
        # Validate different VRFs
        vrfs = ["default", "management", "customer"]
        
        for vrf in vrfs:
            print(f"\nValidating VRF: {vrf}")
            validator = BGPNeighborValidator(device, vrf=vrf)
            result = validator.validate_neighbors()
            
            if result.total_neighbors == 0:
                print(f"  No BGP neighbors in {vrf}")
            else:
                print(f"  {result.get_status_summary()}")
        
    finally:
        device.disconnect()


# ============================================================================
# EXAMPLE 6: Continuous Monitoring Loop
# ============================================================================

def example_6_continuous_monitoring():
    """Monitor BGP neighbors continuously."""
    import time
    from genie.testbed import load
    from bgp.bgp_neighbor_validator import BGPNeighborValidator
    
    testbed = load("testbed.yaml")
    device = testbed.devices["router1"]
    device.connect()
    
    try:
        previous_state = {}
        
        while True:
            validator = BGPNeighborValidator(device)
            result = validator.validate_neighbors()
            
            # Track state changes
            current_state = {
                n.ip_address: n.state.value
                for n in result.neighbors
            }
            
            # Detect changes
            for neighbor_ip, state in current_state.items():
                if neighbor_ip in previous_state:
                    if previous_state[neighbor_ip] != state:
                        print(f"⚠ STATE CHANGE: {neighbor_ip} "
                              f"{previous_state[neighbor_ip]} -> {state}")
            
            previous_state = current_state
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] "
                  f"Established: {result.established_count}, "
                  f"Down: {result.down_count}")
            
            # Check interval
            time.sleep(60)
        
    except KeyboardInterrupt:
        print("Monitoring stopped")
    finally:
        device.disconnect()


# ============================================================================
# EXAMPLE 7: Integration with External Monitoring System
# ============================================================================

def example_7_monitoring_integration():
    """Send metrics to external monitoring system."""
    from genie.testbed import load
    from bgp.bgp_neighbor_validator import BGPNeighborValidator
    
    def send_metrics_to_prometheus(device_name, metrics):
        """Send metrics to Prometheus-compatible endpoint."""
        # Example: Could use python-prometheus or similar
        print(f"Sending metrics for {device_name}: {metrics}")
    
    testbed = load("testbed.yaml")
    
    for device_name, device in testbed.devices.items():
        device.connect()
        try:
            validator = BGPNeighborValidator(device)
            result = validator.validate_neighbors()
            
            # Prepare metrics
            metrics = {
                "bgp_neighbors_total": result.total_neighbors,
                "bgp_neighbors_established": result.established_count,
                "bgp_neighbors_down": result.down_count,
                "bgp_neighbors_error": result.error_neighbors,
            }
            
            # Send to monitoring system
            send_metrics_to_prometheus(device_name, metrics)
        
        finally:
            device.disconnect()


# ============================================================================
# EXAMPLE 8: Validation with Custom Assertions
# ============================================================================

def example_8_assertions():
    """Validate BGP with custom assertions."""
    from genie.testbed import load
    from bgp.bgp_neighbor_validator import BGPNeighborValidator
    
    testbed = load("testbed.yaml")
    device = testbed.devices["router1"]
    device.connect()
    
    try:
        validator = BGPNeighborValidator(device)
        result = validator.validate_neighbors()
        
        # Define assertions
        assert result.total_neighbors >= 2, "Expected at least 2 neighbors"
        assert result.established_count == result.total_neighbors, \
            f"Not all neighbors established: {result.established_count}/{result.total_neighbors}"
        
        # Check specific neighbors
        neighbor_ips = {n.ip_address for n in result.neighbors}
        required_neighbors = {"192.168.1.1", "192.168.1.2"}
        assert required_neighbors.issubset(neighbor_ips), \
            f"Missing required neighbors: {required_neighbors - neighbor_ips}"
        
        # Check prefix exchange
        for neighbor in result.neighbors:
            assert neighbor.prefixes_received > 0, \
                f"{neighbor.ip_address} not receiving prefixes"
        
        print("✓ All assertions passed!")
        
    finally:
        device.disconnect()


# ============================================================================
# EXAMPLE 9: Bulk Operations Script
# ============================================================================

def example_9_bulk_operations():
    """Run bulk validation across multiple devices and VRFs."""
    from genie.testbed import load
    from bgp.bgp_neighbor_validator import BGPNeighborValidator
    
    testbed = load("testbed.yaml")
    devices = ["router1", "router2", "router3"]
    vrfs = ["default", "management"]
    
    results = {}
    
    for device_name in devices:
        results[device_name] = {}
        device = testbed.devices[device_name]
        device.connect()
        
        try:
            for vrf in vrfs:
                validator = BGPNeighborValidator(device, vrf=vrf)
                result = validator.validate_neighbors()
                results[device_name][vrf] = {
                    "total": result.total_neighbors,
                    "established": result.established_count,
                    "down": result.down_count,
                }
        finally:
            device.disconnect()
    
    # Print summary
    for device_name, vrf_results in results.items():
        print(f"\n{device_name}:")
        for vrf, metrics in vrf_results.items():
            print(f"  {vrf}: {metrics}")


# ============================================================================
# EXAMPLE 10: Error Handling and Recovery
# ============================================================================

def example_10_error_handling():
    """Comprehensive error handling."""
    from genie.testbed import load
    from bgp.bgp_neighbor_validator import BGPNeighborValidator
    
    testbed = load("testbed.yaml")
    
    for device_name in ["router1", "unreachable", "router2"]:
        try:
            device = testbed.devices[device_name]
            device.connect(connection_timeout=10)
            
            try:
                validator = BGPNeighborValidator(device)
                result = validator.validate_neighbors()
                
                if result.errors:
                    print(f"⚠ {device_name}: {result.errors[0]}")
                else:
                    print(f"✓ {device_name}: {result.get_status_summary()}")
            
            finally:
                device.disconnect()
        
        except Exception as e:
            print(f"✗ {device_name}: Connection failed - {e}")
            continue


if __name__ == "__main__":
    print("BGP Neighbor Validation - Usage Examples\n")
    print("Run individual examples:")
    print("  python examples.py")
    print("\nOr import and call specific functions:")
    print("  from examples import example_1_simple_validation")
    print("  example_1_simple_validation()")
