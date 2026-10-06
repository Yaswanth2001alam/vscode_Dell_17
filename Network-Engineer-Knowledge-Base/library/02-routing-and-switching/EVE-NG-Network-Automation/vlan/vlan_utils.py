def add_vlan(vlan_id: int, vlan_name: str):
    """
    simulates VLAN creation logic
    
    """
    if not isinstance(vlan_id, int):
        raise TypeError("VLAN ID must be an interger")
    
    if vlan_id < 1 or vlan_id > 4094:
        raise ValueError("VLAN ID must be between 1 and 4094")
    
    if not vlan_name or not isinstance(vlan_name, str):
        raise ValueError("VLAN name must be an non-empty string")
    

    return {

        "vlan_id" : vlan_id,
        "vlan_name": vlan_name,
        "Status" : "Created"
    }