# Troubleshooting Runbook

## Incident record

Record the time, reporter, affected service, devices, symptoms, scope, recent
changes, and business impact before changing anything.

## Layered workflow

| Layer | Checks | Useful evidence |
|---|---|---|
| Scope | One host, VLAN, site, path, or all users? | User reports, monitoring timeline |
| Management | DNS, IP reachability, SSH/API port | Ping, TCP connect, console |
| Physical/L1 | Link, module, speed, duplex, errors | Interface detail and counters |
| Layer 2 | VLAN, trunk, MAC, STP, LLDP/CDP | VLAN/trunk tables, neighbors |
| Layer 3 | Address, mask, ARP, route, next hop | IP interface, ARP, route table |
| Routing | OSPF/BGP state and learned prefixes | Neighbor summaries, LSDB/BGP table |
| Transport | TCP handshake, reset, retransmission | Packet capture, socket test |
| Application | DNS, TLS, HTTP response | `nslookup`, TLS/HTTP client output |

## OSPF checklist

- Same subnet and reachable peer address
- Matching area
- Matching hello/dead timers
- Matching authentication
- Compatible network type
- Interface not unintentionally passive
- Unique router IDs
- Neighbor reaches FULL
- Expected LSAs and routes are installed

## BGP checklist

- Correct local/remote AS
- Reachable neighbor address
- Correct source/update-source
- TCP/179 permitted
- Authentication matches
- Address family activated
- Policies allow intended prefixes
- Next hop is reachable
- Session is Established and prefix counts are expected

## Packet-capture decision

Capture only after forming a question and defining:

- interface;
- host/port/protocol filter;
- duration or packet count;
- storage location;
- data-handling requirements.

Stop the capture as soon as sufficient evidence is collected.

## Closure

- State root cause separately from symptoms.
- Record the exact fix and verification evidence.
- Record rollback readiness and monitoring period.
- Convert repeated manual checks into a read-only automated test.
