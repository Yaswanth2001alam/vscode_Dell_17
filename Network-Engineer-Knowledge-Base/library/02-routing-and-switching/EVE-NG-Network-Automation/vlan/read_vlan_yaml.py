import yaml

with open("vlan.yml" , "r") as f:
    data = yaml.safe_load(f)

for vlan in data["vlan"]:
    print(f"Creating VLAN {vlan['vlan_id']} ({vlan['name']})")
    for intf in vlan["interfaces"]:
        print(f" Assigning interface {intf}")