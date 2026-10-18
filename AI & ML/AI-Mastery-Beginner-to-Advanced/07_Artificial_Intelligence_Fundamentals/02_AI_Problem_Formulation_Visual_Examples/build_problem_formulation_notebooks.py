"""Create and execute new problem-formulation notebooks without overwriting."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import nbformat
from nbclient import NotebookClient

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
IMPLEMENTATION = HERE / "05_problem_formulation.py"


def markdown(source: str):
    return nbformat.v4.new_markdown_cell(source.strip())


def code(source: str):
    return nbformat.v4.new_code_cell(source.strip())


def load_implementation():
    spec = importlib.util.spec_from_file_location("problem_formulation", IMPLEMENTATION)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load implementation: {IMPLEMENTATION}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


implementation = load_implementation()
task, sample_actions = implementation.build_network_example()

visual_cells = [
    markdown("""# AI Problem Formulation — Visual Examples

**Execution status:** this notebook is executed by its builder; actual cell outputs are saved. Examples are synthetic and perform no network operations.

## 1. Introduction and learning objectives

Problem formulation turns a vague request into a task with a goal, observations, candidate actions, hard constraints, costs, and evaluation. You will translate an everyday request into a simple specification, rank options, add a safety boundary, and visualize how cost assumptions affect choices.

**Prerequisites:** Python basics and the course's AI introduction. **Objectives:** distinguish constraints from preferences; calculate a weighted score; identify when an option must be excluded; explain the chart and its units.

## 2. Beginner explanation

“Help with a slow network” could mean diagnose latency, find packet loss, or recommend a configuration change. We first define the intended output. In this lab the system only ranks evidence for an operator; it never executes commands."""),
    code("""import importlib.util
import sys
from pathlib import Path
import matplotlib

implementation_path = Path("07_Artificial_Intelligence_Fundamentals/02_AI_Problem_Formulation_Visual_Examples/05_problem_formulation.py")
spec = importlib.util.spec_from_file_location("problem_formulation", implementation_path)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load reusable implementation: {implementation_path}")
implementation = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = implementation
spec.loader.exec_module(implementation)
task, sample_actions = implementation.build_network_example()
print(f"Python {sys.version.split()[0]} | Matplotlib {matplotlib.__version__}")
print("Reusable implementation loaded; no device connection created.")"""),
    markdown("""## 3. Mathematical background

For a candidate \(a\), this lesson uses \(J(a)=\\alpha t(a)+\\beta r(a)-\\gamma i(a)\). Here \(t\) is estimated time units, \(r\) normalized risk (0–1), \(i\) illustrative information value (0–1), and the nonnegative coefficients express preference weights. A lower score is preferred only among candidates allowed by hard constraints.

Worked example: counter inspection with \(t=2,r=0,i=0.6\), weights \((1,10,2)\), has \(J=2+0-1.2=0.8\). This score is a teaching calculation, not a measured probability or operational risk estimate."""),
    markdown("""## 4. Example 1 — Absolute beginner

A goal says what we want; a constraint states what is allowed. The following plain dictionary makes both visible. Each variable is a text description, not a command."""),
    code("""task_card = {
    "goal": "show the operator useful evidence",
    "observation": "synthetic latency is elevated",
    "allowed": "read-only inspection",
    "prohibited": "device configuration change",
}
print(task_card["goal"])
print("Hard constraint:", task_card["prohibited"])"""),
    markdown("""**Walkthrough:** `task_card` is a dictionary mapping field names to descriptions. The two `print` calls retrieve values using keys. The output repeats the goal and prohibition because those strings were assigned above. This is useful because it makes scope explicit before selecting a model."""),
    markdown("""## 5. Example 2 — Beginner practical formulation

A latency conversion has a measurable goal and input constraint. It is ordinary deterministic software; AI is unnecessary for this exact task."""),
    code("""def latency_ms(seconds: float) -> float:
    if seconds < 0:
        raise ValueError("latency seconds must be non-negative")
    return seconds * 1000

print(f"Latency: {latency_ms(0.125):.1f} ms")"""),
    markdown("""The function accepts seconds, checks a domain constraint, converts by multiplying by 1000, and returns milliseconds. The formatted output displays one decimal place. If the input is negative, the function rejects it instead of reporting an invalid latency."""),
    markdown("""## 6. Example 3 — Intermediate candidate ranking

The reusable module stores candidate descriptions, hard constraints, and soft preferences. It only ranks options; it has no device API."""),
    code("""print("Goal:", task.goal)
for action, score in task.rank_candidates(sample_actions):
    print(f"{action.name}: cost={score:.2f}; changes_state={action.changes_state}")
print("A state-changing candidate is filtered without approval.")"""),
    markdown("""The counter inspection scores \(2-2(0.6)=0.8\); routing inspection scores \(3-2(0.9)=1.2\). The interface reset is excluded by the no-write constraint before ranking. Candidate scores depend on the illustrative weights and estimates."""),
    markdown("""## 7. Example 4 — Advanced weight sensitivity and approval

Preferences may vary, but hard constraints remain distinct. The first ranking changes the risk weight for permitted actions. An explicit approval flag shows a boundary in this toy policy; it is not production authentication."""),
    code("""for risk_weight in (2.0, 10.0, 30.0):
    varied = implementation.TaskFormulation(
        goal=task.goal,
        prohibited_actions=task.prohibited_actions,
        risk_weight=risk_weight,
    )
    names = [action.name for action, _ in varied.rank_candidates(sample_actions)]
    print(f"risk_weight={risk_weight:g}: {names}")

approved_view = task.rank_candidates(sample_actions, human_approved=True)
print("With explicit demo approval, descriptions considered:", [a.name for a, _ in approved_view])
print("No action is executed.")"""),
    markdown("""Changing soft weights can reorder permitted options. The reset remains excluded unless the caller explicitly sets the demonstration approval argument. Real systems must enforce identity, scope, policy, audit, and change approval independently of an AI model."""),
    markdown("""## 8. Example 5 — Real-world read-only network scenario

The following synthetic fields describe a possible troubleshooting snapshot. The task is to gather evidence for a human, not to assert a cause or alter routing."""),
    code("""snapshot = {
    "site": "synthetic-site-01",
    "latency_ms": 118.0,
    "packet_loss_pct": 2.0,
    "bgp_state": "Established",
    "data_is_synthetic": True,
}
evidence = [key for key in ("latency_ms", "packet_loss_pct", "bgp_state") if key in snapshot]
print("Evidence fields:", evidence)
print("Observation:", snapshot)
print("Recommendation scope: inspect evidence; do not change device state.")"""),
    markdown("""The list comprehension collects available evidence keys. The BGP state and latency are separate observations; an established neighbor alone does not prove end-to-end service health. Real use requires timestamps, units, provenance, missing-data handling, and domain review."""),
    markdown("""## 9. Visualization — candidate time, risk, and information

Each point is one synthetic candidate. **X-axis:** estimated investigation time (arbitrary units). **Y-axis:** normalized illustrative risk from 0 to 1. Bubble area encodes illustrative information value, not statistical confidence. The state-changing reset is marked separately and is prohibited by this lab's hard constraint."""),
    code("""import matplotlib.pyplot as plt

permitted, excluded = [], []
for candidate in sample_actions:
    (excluded if candidate.changes_state else permitted).append(candidate)

fig, ax = plt.subplots(figsize=(8, 5))
for group, color, label in ((permitted, "steelblue", "Read-only candidate"),
                            (excluded, "crimson", "State-changing / excluded")):
    if group:
        ax.scatter(
            [item.time_units for item in group],
            [item.risk for item in group],
            s=[100 + 300 * item.information_value for item in group],
            color=color,
            label=label,
            alpha=0.8,
        )
        for item in group:
            ax.annotate(item.name.replace("_", "\\n"),
                        (item.time_units, item.risk), xytext=(6, 7),
                        textcoords="offset points", fontsize=8)
ax.set(title="Synthetic troubleshooting candidates: time vs risk",
       xlabel="Estimated investigation time (arbitrary units)",
       ylabel="Illustrative risk (0 = low, 1 = high)")
ax.set_ylim(-0.08, 1.0)
ax.legend()
ax.grid(alpha=0.25)
plt.show()"""),
    markdown("""**Interpretation:** read-only candidates appear at risk 0; the reset is at risk 0.8 and marked excluded. Larger bubbles correspond to higher assumed information value. If time/risk estimates or inputs change, positions and preferred ranking change. The chart explains assumptions; it is not operational telemetry or empirical evidence."""),
    markdown("""## 10. Debugging and common mistakes

The invalid example is caught and printed. A hard constraint should not be replaced by a large score penalty, and malformed measurements must not silently pass."""),
    code("""try:
    latency_ms(-0.5)
except ValueError as error:
    print(f"Rejected invalid measurement: {error}")

try:
    invalid_action = implementation.CandidateAction("bad", 1.0, 1.5, 0.2)
    invalid_action.validate()
except ValueError as error:
    print(f"Rejected invalid risk: {error}")"""),
    markdown("""## 11. Practice and experiment

Change `risk_weight` and rerun the advanced cell. Add a new read-only candidate with an estimated duration and information value, then describe why those estimates are uncertain. Attempt the separate [exercise notebook](03_AI_Problem_Formulation_Exercises.ipynb) before opening its solutions.

## 12. Summary and next topic

A good formulation states the goal, observations, candidate outputs, hard constraints, soft costs, and evaluation. Ranking never grants execution authority. Next: search and planning over explicit states and action sequences."""),
]

exercise_cells = [
    markdown("""# AI Problem Formulation — Exercises

**Objectives:** translate requests into explicit tasks, calculate simple costs, and design safe network triage. Inputs here are synthetic. Try before opening `04_AI_Problem_Formulation_Solutions.ipynb`.

## Prerequisites and beginner explanation

Goal = desired outcome; observation = available data; candidate = possible recommendation; hard constraint = must-not/must-do rule; metric = measured evaluation. A lower weighted cost only ranks options that constraints permit."""),
    code("""import sys
print(f"Python {sys.version.split()[0]} | standard-library exercises")"""),
    markdown("""## Beginner exercise 1 — Make a vague request testable

“Make our application faster.” Specify a user, measurable goal, observation, time window, constraint, and evaluation metric. State one thing that should not be optimized in isolation."""),
    code("""request = "Make our application faster"
print("Vague request to reformulate:", request)
print("Write your specification in a Markdown cell or a separate note.")"""),
    markdown("""## Beginner exercise 2 — Identify hard versus soft requirements

For a network helper, classify each as a hard constraint or a soft preference and justify: (a) never expose credentials, (b) prefer shorter investigation time, (c) do not change a device without approval."""),
    markdown("""## Intermediate exercise 3 — Compute a weighted cost

Use \(J=t+10r-2i\). Candidate A: \(t=2,r=0,i=0.6\). Candidate B: \(t=3,r=0,i=0.9\). Compute both, choose the lower-cost candidate, and state why this does not prove it is the correct diagnosis."""),
    code("""candidates = {
    "A": {"time": 2.0, "risk": 0.0, "information": 0.6},
    "B": {"time": 3.0, "risk": 0.0, "information": 0.9},
}
print("Candidate inputs:", candidates)
print("Add a cell to calculate J = time + 10*risk - 2*information.")"""),
    markdown("""## Intermediate exercise 4 — Metrics for rare incidents

Incidents occur in 1 of 500 windows. Give a baseline that may appear accurate but is useless. Propose two metrics that expose its failure and explain why evaluation should be time-aware."""),
    markdown("""## Advanced exercise 5 — Hard-constraint check

Add a state-changing candidate to `05_problem_formulation.py`'s conceptual action list. Describe a test that proves it is excluded without approval. Do not connect to a device or implement execution."""),
    markdown("""## Advanced exercise 6 — Network triage mini-design

Specify a synthetic read-only assistant: goal, observations, missing/stale-data behavior, allowed recommendations, prohibited actions, test split, metrics, evidence shown, abstention rule, and human approval. Include false-positive and false-negative consequences."""),
    markdown("""## Knowledge check

1. What is the difference between a hard constraint and a soft cost?
2. Why can optimizing mean latency harm another user goal?
3. What must be independent of a model's natural-language claim before any network change?

Solutions are deliberately separated in `04_AI_Problem_Formulation_Solutions.ipynb`."""),
]

solution_cells = [
    markdown("""# AI Problem Formulation — Exercise Solutions

Use after attempting `03_AI_Problem_Formulation_Exercises.ipynb`. More than one formulation can be correct when assumptions are stated."""),
    code("""import importlib.util
import sys
from pathlib import Path
import matplotlib

implementation_path = Path("07_Artificial_Intelligence_Fundamentals/02_AI_Problem_Formulation_Visual_Examples/05_problem_formulation.py")
spec = importlib.util.spec_from_file_location("problem_formulation", implementation_path)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load reusable implementation: {implementation_path}")
implementation = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = implementation
spec.loader.exec_module(implementation)
print(f"Python {sys.version.split()[0]} | Matplotlib {matplotlib.__version__}")"""),
    markdown("""## Solution 1 — Make a vague request testable

Example: For users of service X, reduce p95 request latency over a specified weekday peak window while maintaining error rate and availability within agreed bounds. Observe timestamped request durations, errors, and deployment events. Evaluate on a later time period. Do not optimize average latency alone because tail latency and errors can worsen."""),
    markdown("""## Solution 2 — Hard versus soft

(a) Never expose credentials: hard security constraint. (b) Prefer shorter investigation time: soft preference/cost. (c) No device change without approval: hard authorization constraint. A score penalty is not a substitute for enforcing (a) or (c)."""),
    markdown("""## Solution 3 — Weighted cost

\(J_A=2+10(0)-2(0.6)=0.8\). \(J_B=3+10(0)-2(0.9)=1.2\). A ranks lower for these assumed weights. The estimates may be wrong, omitted evidence may matter, and neither ranking demonstrates causation or diagnostic correctness."""),
    code("""def cost(time, risk, information):
    return time + 10 * risk - 2 * information

for name, data in {"A": (2.0, 0.0, 0.6), "B": (3.0, 0.0, 0.9)}.items():
    print(f"{name}: J={cost(*data):.1f}")"""),
    markdown("""The function's positional arguments are time, risk, and information. It implements the equation exactly. The outputs match the manual arithmetic; agreement validates this arithmetic example, not the assumptions."""),
    markdown("""## Solution 4 — Rare-event metrics

A model that predicts “no incident” for every window gets about 99.8% accuracy but zero incident recall. Precision/recall or a precision-recall curve show detection versus alert quality; alerts per review period measures operational burden. A time-aware split better approximates future use and avoids adjacent or future-derived information contaminating evaluation."""),
    markdown("""## Solution 5 — Constraint test

Construct one read-only and one `changes_state=True` candidate. Call `rank_candidates` without approval and assert the mutating candidate is absent. Then call with explicit approval in the toy policy and assert it appears only as a description. There must be no device execution method in the test."""),
    markdown("""## Solution 6 — Network triage design

One acceptable design uses generated latency, loss, interface-counter, and routing-neighbor observations. It returns evidence-linked investigation suggestions only. Missing or stale fields lower confidence or trigger abstention. Split by time/incident. Measure incident recall, precision, and alerts per review shift; inspect missed incidents. Prohibit configuration writes and secret exposure. An authenticated engineer reviews any subsequent action through existing change controls."""),
    code("""task, options = implementation.build_network_example()
ranked = task.rank_candidates(options)
print("ranked read-only:", [action.name for action, _ in ranked])
assert all(not action.changes_state for action, _ in ranked)
print("state-changing option excluded: test passed")"""),
    markdown("""This test checks the declared boundary. It does not prove a real deployment's external tools, identities, or authorization policies are secure."""),
    markdown("""## Knowledge check answers

1. A hard constraint excludes an option; a soft cost ranks allowed options. 2. Average latency can hide tail delays, errors, fairness, or availability. 3. Authenticated identity, authorization policy, validation, approval, audit, and rollback controls must exist independently of model text."""),
]

notebooks = {
    "02_AI_Problem_Formulation_Visual_Examples.ipynb": visual_cells,
    "03_AI_Problem_Formulation_Exercises.ipynb": exercise_cells,
    "04_AI_Problem_Formulation_Solutions.ipynb": solution_cells,
}

for filename, cells in notebooks.items():
    destination = HERE / filename
    if destination.exists():
        raise FileExistsError(
            f"Refusing to overwrite existing notebook: {destination}"
        )
    notebook = nbformat.v4.new_notebook(
        cells=cells,
        metadata={
            "kernelspec": {
                "display_name": "Python 3 (AI Mastery)",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.13.14"},
        },
    )
    nbformat.validate(notebook)
    NotebookClient(
        notebook,
        timeout=120,
        kernel_name="python3",
        resources={"metadata": {"path": str(ROOT)}},
    ).execute()
    nbformat.write(notebook, destination)
    print(f"EXECUTED {destination.name}; saved outputs for {len(notebook.cells)} cells")
