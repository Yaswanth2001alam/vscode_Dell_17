# EVE-NG Three-Router Automation Lab

This lab automates Cisco IOS 7200 routers in a linear topology:

```text
Management network: 192.168.32.0/24

R1 Lo0 10.255.0.1/32                        R3 Lo0 10.255.0.3/32
       |                                             |
R1 E1/1 10.12.0.1/30 --- 10.12.0.2/30 E1/1 R2
                                      R2 E1/2 10.23.0.1/30
                                             |
                                      10.23.0.2/30 E1/1 R3
                                      R2 Lo0 10.255.0.2/32
```

The inventory uses `192.168.32.144` for R3 because `12.168.32.144` appears to be a typo in a management subnet where R1 and R2 use `192.168.32.0/24`. If `12.168.32.144` is intentional, edit `inventory.json` or set `R3_HOST`.

## Safety and setup

Credentials are never stored in source files. Copy `.env.example` to the
git-ignored `.env` file, then edit `.env` with the lab credentials:

```powershell
Set-Location "C:\Users\v-yaalam\Downloads\vscode_Dell_17-1\1.Python Learning\Network Coding\EVE-NG_3_Router_Automation"
Copy-Item .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

The Python program loads `.env` automatically. PowerShell environment variables
with the same names can still be used and take precedence.

Each router must already have a reachable management IP and SSH enabled. A typical IOS bootstrap configuration is:

```ios
ip domain-name lab.local
crypto key generate rsa modulus 2048
ip ssh version 2
username admin privilege 15 secret <your-secret>
line vty 0 4
 login local
 transport input ssh
```

Confirm the actual IOS interface names with `show ip interface brief`. Change `Ethernet1/1` or `Ethernet1/2` in `inventory.json` if your 7200 image uses different names.

## Safe workflow

```powershell
# 1. Validate TCP/22 reachability without logging in
python .\lab_automation.py precheck

# 2. Preview every command; this does not require Netmiko or credentials
python .\lab_automation.py plan --scenario ospf

# 3. Back up running and startup configurations
python .\lab_automation.py backup

# 4. Apply explicitly, then verify and save the outputs
python .\lab_automation.py apply --scenario ospf --apply
python .\lab_automation.py verify --scenario ospf

# 5. Save configuration only after verification
python .\lab_automation.py apply --scenario ospf --apply --save
```

Every operation writes a timestamped JSON report under `outputs\`, including command output and per-device errors.

## Available routing scenarios

| Scenario | Command | Purpose |
|---|---|---|
| Baseline | `python .\lab_automation.py apply --scenario baseline --apply` | Hostnames, CEF, loopbacks, and transit links |
| OSPF | `python .\lab_automation.py apply --scenario ospf --apply` | Multi-hop R1-to-R3 reachability through OSPF area 0 |
| eBGP | `python .\lab_automation.py apply --scenario ebgp --apply` | AS65001-AS65002-AS65003 route exchange |
| BGP only | `python .\lab_automation.py apply --scenario bgp-only --apply` | Add three-AS eBGP without sending interface or OSPF commands |
| OSPF + eBGP | `python .\lab_automation.py apply --scenario ospf-ebgp --apply` | Compare IGP and BGP routes in one lab |
| iBGP RR | `python .\lab_automation.py apply --scenario ibgp-rr --apply` | OSPF underlay plus R2 as an AS65000 route reflector |

Do not apply eBGP and iBGP route-reflector scenarios on top of one another. Remove old routing processes first:

```powershell
python .\lab_automation.py cleanup --apply
```

Cleanup removes OSPF and the BGP processes but deliberately preserves interface addressing and management access.

The transit Ethernet interfaces use `ip ospf network point-to-point`. This
avoids an unnecessary DR/BDR election and is especially useful with older
Cisco 7200 IOS images that can remain in `2WAY/DROTHER` on two-router links.

To add eBGP to an already working OSPF lab without touching OSPF or interface
configuration:

```powershell
python .\lab_automation.py plan --scenario bgp-only
python .\lab_automation.py apply --scenario bgp-only --apply --save
python .\lab_automation.py verify --scenario bgp-only
```

The BGP-only verification deliberately collects both OSPF and BGP state so the
saved report proves OSPF remained operational while BGP was added.

## Automation exercises and failure tests

Use `--devices R1 R2` to limit any operation. Useful experiments include:

1. **Convergence:** Apply OSPF, shut R2 `Ethernet1/2`, run verification, restore it, and compare reports.
2. **OSPF mismatch:** Change one side to area 1 or alter hello/dead timers; confirm the neighbor does not reach FULL.
3. **Passive interface:** Make a transit interface passive and observe adjacency loss while Loopback0 remains safely passive.
4. **eBGP AS mismatch:** Configure the wrong `remote-as`, inspect `show ip bgp summary`, then correct it through inventory/code.
5. **BGP filtering:** Add prefix lists and route maps to permit only loopback /32 routes.
6. **Route reflector:** Compare iBGP without full mesh to the `ibgp-rr` scenario.
7. **Reachability matrix:** Compare the three loopback pings before baseline, after OSPF, and after BGP.
8. **Idempotency:** Apply the same scenario twice and compare the two output reports.
9. **Configuration drift:** Manually change a description or IP, run `backup`, reapply the intended scenario, and verify.
10. **Operational health:** Run `python .\lab_automation.py health` to collect CPU, memory, interfaces, errors, logs, and CDP.
11. **Partial execution:** Use `--devices R2` for a controlled change, then inspect the effect on both neighbors.
12. **Persistence:** Apply without `--save`, reload to demonstrate loss, then repeat with `--save`.

For destructive tests, first run `backup` and keep the EVE-NG console open so management can be recovered.

## Jupyter notebook

Open `three_router_lab.ipynb`, select the virtual environment kernel, and run
cells individually. The notebook executes the same CLI so output is both visible
in Jupyter and persisted in `outputs\`. Set `APPLY_CHANGES = True` only after
reviewing the generated plan. Each operational cell imports its helper itself,
so cells can be run individually and do not depend on execution order.

Open `network_verification_tests.ipynb` for read-only operational checks. It
contains 20 manual checks covering management reachability, interfaces,
descriptions, errors, OSPF, BGP, routes, pings, CDP, ARP, CPU, memory, logging,
NTP, users, SSH, ACLs, and important running/startup configuration sections.
Each cell saves its raw results under `outputs\verification\`.

## Tests

The unit tests validate generated IOS configuration without contacting routers:

```powershell
python -m unittest -v
```
