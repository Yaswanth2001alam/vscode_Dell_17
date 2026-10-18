"""
Agents, workflows, and bounded tool use.

Level: Advanced.
Run this file with the course virtual environment's Python.
Examples are offline, CPU-sized, and use local synthetic data.
See the matching notebook for full explanations, assumptions, and exercises.
"""

# %% Worked example: A bounded mock planner with a read-only tool
# Prove budget and allowlist behavior.
# Step 1: Keep the planner's proposals separate from execution.
# Step 2: Allow only a read-only local tool.
# Step 3: Pass observed results back to the planner.
# Step 4: Raise if the budget is exhausted instead of fabricating completion.
if __name__ == "__main__":
    def inventory_status(hostname):
        known = {"edge-01": "up"}
        return {"hostname": hostname, "state": known[hostname]}

    def mock_plan(observations):
        if not observations:
            return {"tool": "inventory_status", "arguments": {"hostname": "edge-01"}}
        return {"final": f"edge-01 is {observations[-1]['state']}"}

    tools = {"inventory_status": inventory_status}
    observations, final = [], None
    for step in range(3):
        proposal = mock_plan(observations)
        if "final" in proposal:
            final = proposal["final"]
            break
        name = proposal["tool"]
        if name not in tools:
            raise PermissionError("tool not allowed")
        arguments = proposal["arguments"]
        if set(arguments) != {"hostname"} or arguments["hostname"] != "edge-01":
            raise PermissionError("target not authorized")
        observations.append(tools[name](**arguments))
    else:
        raise RuntimeError("step budget exhausted")
    assert final == "edge-01 is up" and len(observations) == 1
    print(final, "tool calls:", len(observations))
