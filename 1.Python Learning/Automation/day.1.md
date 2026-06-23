🛠️ Network Automation — Day 1: Imperative vs. Declarative & Idempotency
1) Concept
Two fundamentally different ways to automate network changes:
Imperative — you specify the exact steps ("how"). Example: log in, enter config mode, type these commands in this order. You own the sequencing and the error handling. Like turn-by-turn driving directions.
Declarative — you specify the desired end state ("what"). Example: "VLAN 10 named USERS should exist on this switch." The tool figures out the steps needed to reach that state. Like giving a destination to a GPS.
Idempotency is the property that makes declarative automation safe: running the same operation once or many times produces the same result. If VLAN 10 already exists, re-running the playbook changes nothing — it doesn't error, duplicate, or disrupt. This is what lets you run automation repeatedly with confidence.
Why it matters: declarative + idempotent tooling (Ansible, Terraform, vendor intent APIs) lets you re-apply your source of truth at scale without fear of breaking devices that are already correct.
2) Practice Examples
Imperative (raw CLI pushed in sequence):
configure terminal
vlan 10
 name USERS
end

Run this twice and the device re-processes the commands each time — and a script that "adds" config can create duplicates or errors if it doesn't check current state first.
Declarative (Ansible, desired state):
- name: Ensure VLAN 10 exists
  cisco.ios.ios_vlans:
    config:
      - vlan_id: 10
        name: USERS
    state: merged

First run output: changed: [switch01] — VLAN 10 created.
Second run output: ok: [switch01] — nothing to do; already in desired state. That "ok" instead of "changed" is idempotency in action.
3) Practice Question
Q: You run an Ansible playbook that ensures an interface description is set to "UPLINK". The first run reports changed. You run it again immediately with no other changes. What should the second run report, and what does that tell you?
A: The second run should report ok (not changed). The module compared the desired state ("UPLINK") to the running state, found them identical, and made no modification. This confirms the task is idempotent — safe to run repeatedly. If instead it reported changed every single time on identical input, that task is not truly idempotent and warrants investigation (often a sign the module is blindly pushing config rather than comparing state).
4) Microsoft Internal WAN Automation Notes
Microsoft's internal WAN operates on a declarative, intent-driven model rather than engineers typing CLI on individual routers. The network's desired state lives in a centralized source of truth; automation continuously reconciles each device toward that intent. Key practices that mirror today's concept:
Intent over commands — operators express what the WAN should look like (roles, peers, capacities); the platform derives and applies the how across a multi-vendor fleet.
Idempotent reconciliation — config is re-applied safely and repeatedly; devices already matching intent are left untouched, which is essential when managing thousands of WAN nodes.
Drift detection — because the desired state is declared, the system can continuously compare running state to intent and flag/auto-remediate drift before it causes an outage.
Next scheduled lesson — Day 2 (Mon, June 22, 8 AM PST): YAML/JSON inventories — structuring your source-of-truth data.
