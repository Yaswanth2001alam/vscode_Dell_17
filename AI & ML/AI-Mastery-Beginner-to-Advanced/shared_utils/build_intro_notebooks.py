"""Build and execute the introductory AI lesson notebooks reproducibly."""

from pathlib import Path

import nbformat
from nbclient import NotebookClient

OUTPUT = Path("07_Artificial_Intelligence_Fundamentals/01_Introduction_to_Artificial_Intelligence")
OUTPUT.mkdir(parents=True, exist_ok=True)

LESSONS = {
    "02_Beginner_Examples.ipynb": {
        "title": "Beginner Examples",
        "focus": "Compare an explicit threshold rule with a tiny model whose class means are computed from examples.",
        "beginner": "A rule is an instruction a programmer writes. A model is a rule or learned representation that maps inputs to outputs. Inference means applying it to a new input.",
        "first": '''def needs_review(measurement: float, threshold: float = 75.0) -> bool:
    if threshold < 0:
        raise ValueError("threshold must be non-negative")
    return measurement >= threshold

sample = 80.0
print(f"measurement={sample:.1f}; needs_review={needs_review(sample)}")''',
        "linewise": "The function accepts a measurement and default threshold. Type hints describe input and output. The guard rejects invalid settings; `>=` includes the boundary; the call supplies 80 and prints the Boolean.",
        "intermediate": '''from collections import defaultdict
training = [(10.0, "normal"), (12.0, "normal"), (80.0, "review"), (90.0, "review")]
sums, counts = defaultdict(float), defaultdict(int)
for value, label in training:
    sums[label] += value
    counts[label] += 1
centers = {label: sums[label] / counts[label] for label in sums}
query = 70.0
predicted = min(centers, key=lambda label: abs(query - centers[label]))
print("class means:", dict(centers))
print("prediction:", predicted)''',
        "advanced": '''distances = {label: abs(query - center) for label, center in centers.items()}
minimum = min(distances.values())
winners = [label for label, distance in distances.items() if distance == minimum]
prediction = winners[0] if len(winners) == 1 else "uncertain"
print("distances:", distances, "=>", prediction)''',
        "real": '''synthetic_latency_ms = [12, 15, 14, 120, 13]
review = [i for i, value in enumerate(synthetic_latency_ms) if value >= 80]
print("synthetic review-window indices:", review)
print("No network device is contacted or changed.")''',
        "plot": '''import matplotlib.pyplot as plt
plt.bar(list(centers), list(centers.values()), color=["steelblue", "darkorange"])
plt.axhline(query, color="black", linestyle="--", label="query")
plt.ylabel("Synthetic measurement")
plt.title("Nearest-centroid example")
plt.legend()
plt.show()''',
        "debug": '''try:
    needs_review(80, threshold=-1)
except ValueError as error:
    print(f"Handled invalid input: {error}")
print("Corrected:", needs_review(80, threshold=75))''',
        "exercises": "1. Predict the threshold boundary before running. 2. Add an example and recompute its class mean. 3. Explain why a synthetic latency alert is not fault diagnosis.",
        "summary": "A rule is explicit; centroids are computed from labeled examples. Both demonstrations use synthetic data. State one limitation of each approach.",
    },
    "03_Intermediate_Examples.ipynb": {
        "title": "Intermediate Examples",
        "focus": "Fit class means and inspect evaluation, error counts, and time-aware splits.",
        "beginner": "A label is a known answer paired with an example. A centroid is the mean value for one class. A nearest-centroid prediction chooses the closest mean.",
        "first": '''training = [(10.0, "normal"), (12.0, "normal"), (80.0, "review"), (90.0, "review")]
centers = {label: sum(x for x, y in training if y == label) / sum(y == label for _, y in training)
           for _, label in training}
query = 70.0
guess = min(centers, key=lambda label: abs(query - centers[label]))
print("centers:", centers, "| query:", query, "| prediction:", guess)''',
        "linewise": "The comprehension visits labels, filters examples for each label, computes the mean, and stores it in a dictionary. The final `min` compares absolute distances. The dataset is intentionally tiny.",
        "intermediate": '''evaluation = [(11.0, "normal"), (85.0, "review"), (70.0, "review")]
rows = [(x, y, min(centers, key=lambda c: abs(x-centers[c]))) for x, y in evaluation]
correct = sum(actual == predicted for _, actual, predicted in rows)
print("(value, actual, predicted):", rows)
print(f"toy accuracy={correct}/{len(rows)}={correct/len(rows):.1%}")''',
        "advanced": '''actual, predicted = [1, 1, 0, 0, 0], [1, 0, 0, 0, 0]
tp = sum(a == p == 1 for a, p in zip(actual, predicted))
fn = sum(a == 1 and p == 0 for a, p in zip(actual, predicted))
tn = sum(a == p == 0 for a, p in zip(actual, predicted))
print({"TP": tp, "FN": fn, "TN": tn, "recall": tp/(tp+fn), "accuracy": (tp+tn)/len(actual)})''',
        "real": '''ordered = [(10, "normal"), (12, "normal"), (14, "normal"), (80, "review"), (90, "review")]
train, future = ordered[:3], ordered[3:]
baseline = max(x for x, _ in train)
print("earlier baseline:", baseline, "| future observations:", future)
print("Use a time split when it matches how the system will be used.")''',
        "plot": '''import matplotlib.pyplot as plt
for label, center in centers.items():
    plt.scatter(center, label, s=100, label=f"{label} mean")
plt.axvline(query, color="black", linestyle="--", label="query")
plt.xlabel("Synthetic measurement")
plt.title("Class means and query")
plt.legend()
plt.show()''',
        "debug": '''try:
    min(centers, key=lambda label: abs(70 - centers[label])) if centers else (_ for _ in ()).throw(ValueError("model is empty"))
except ValueError as error:
    print("Rejected invalid model:", error)
print("Valid fitted-model prediction:", guess)''',
        "exercises": "1. Add a misclassified held-out example and calculate recall. 2. Explain leakage from adjacent time windows. 3. Propose a non-ML baseline.",
        "summary": "A held-out score estimates behavior only under the chosen split. Explain what evidence is missing before real deployment.",
    },
    "04_Advanced_Examples.ipynb": {
        "title": "Advanced Examples",
        "focus": "Examine score thresholds, error costs, uncertainty, and human authorization boundaries.",
        "beginner": "A prediction is an output, not an action. A threshold converts a score into a decision. A score is not automatically a calibrated probability.",
        "first": '''scores = {"window_A": 0.12, "window_B": 0.83, "window_C": 0.56}
threshold = 0.60
for window, score in scores.items():
    decision = "review" if score >= threshold else "no alert"
    print(f"{window}: score={score:.2f}, decision={decision}")''',
        "linewise": "The dictionary stores illustrative scores by ID. The cutoff defines the operating rule. The loop formats each decision. Values are hand-set and are not model probabilities.",
        "intermediate": '''actual, predicted = [1, 1, 0, 0, 0], [1, 0, 0, 0, 0]
tp = sum(a == p == 1 for a, p in zip(actual, predicted))
fn = sum(a == 1 and p == 0 for a, p in zip(actual, predicted))
fp = sum(a == 0 and p == 1 for a, p in zip(actual, predicted))
tn = sum(a == p == 0 for a, p in zip(actual, predicted))
print({"TP": tp, "FN": fn, "FP": fp, "TN": tn})
print(f"recall={tp/(tp+fn):.1%}; accuracy={(tp+tn)/len(actual):.1%}")''',
        "advanced": '''def recommend(score, threshold, approved=False):
    if not 0 <= score <= 1:
        raise ValueError("score must be between 0 and 1")
    if score < threshold:
        return "no recommendation"
    return "approved next step" if approved else "human review required"

print(recommend(0.9, 0.6))
print(recommend(0.9, 0.6, approved=True))''',
        "real": '''observed = [10, 11, 12, 13, 14, 50]  # synthetic time series
baseline = max(observed[:4])
print("baseline from earlier data:", baseline)
print("future deviations:", [value - baseline for value in observed[4:]])''',
        "plot": '''import matplotlib.pyplot as plt
plt.bar(list(scores), list(scores.values()), color=["steelblue" if s < threshold else "darkorange" for s in scores.values()])
plt.axhline(threshold, color="black", linestyle="--", label=f"threshold={threshold}")
plt.ylim(0, 1)
plt.ylabel("Illustrative score (not calibrated probability)")
plt.title("Threshold affects review volume")
plt.legend()
plt.show()''',
        "debug": '''try:
    recommend(1.2, 0.6)
except ValueError as error:
    print("Caught invalid score:", error)
print("Valid score:", recommend(0.9, 0.6))''',
        "exercises": "1. Vary the cutoff and record review volume. 2. Create a rare-event case with high accuracy but zero recall. 3. Design an approval gate the model cannot override.",
        "summary": "Thresholds encode tradeoffs; safe actions require controls beyond a classifier. Explain how you would set a threshold without tuning on the test set.",
    },
    "05_Real_World_Applications.ipynb": {
        "title": "Real-World Applications",
        "focus": "Use synthetic network telemetry to build evidence-bearing, read-only triage examples.",
        "beginner": "Telemetry is measured data such as latency and packet loss. An alert can prioritize investigation; it does not establish root cause.",
        "first": '''telemetry = [
    {"window": "w1", "latency_ms": 12.0, "loss_pct": 0.0},
    {"window": "w2", "latency_ms": 118.0, "loss_pct": 2.0},
]
for row in telemetry:
    print(row["window"], "latency=", row["latency_ms"], "ms; loss=", row["loss_pct"], "%")''',
        "linewise": "Each dictionary is a synthetic measurement window. Named keys describe fields. The loop reads and prints those fields; no network connection is made.",
        "intermediate": '''def triage(row, latency_limit=80.0, loss_limit=1.0):
    required = {"window", "latency_ms", "loss_pct"}
    if not required.issubset(row):
        raise ValueError("telemetry row is missing required fields")
    reasons = []
    if row["latency_ms"] >= latency_limit:
        reasons.append("high latency")
    if row["loss_pct"] >= loss_limit:
        reasons.append("packet loss")
    return {"window": row["window"], "review": bool(reasons), "evidence": reasons}

print([triage(row) for row in telemetry])''',
        "advanced": '''def summary(rows):
    if not rows:
        raise ValueError("at least one telemetry row is required")
    return {"count": len(rows),
            "mean_latency_ms": round(sum(r["latency_ms"] for r in rows)/len(rows), 2),
            "max_loss_pct": max(r["loss_pct"] for r in rows)}

print("summary:", summary(telemetry))
print("No configuration action is performed.")''',
        "real": '''for row in telemetry:
    result = triage(row)
    if result["review"]:
        print(f"{result['window']}: review; evidence={result['evidence']}; action=none")''',
        "plot": '''import matplotlib.pyplot as plt
plt.plot([r["window"] for r in telemetry], [r["latency_ms"] for r in telemetry], marker="o", label="synthetic latency")
plt.axhline(80, color="darkorange", linestyle="--", label="review threshold")
plt.ylabel("Latency (ms)")
plt.title("Synthetic read-only network triage")
plt.legend()
plt.show()''',
        "debug": '''malformed = {"window": "bad", "latency_ms": 90.0}
try:
    triage(malformed)
except ValueError as error:
    print("Rejected malformed telemetry:", error)
print("Valid record:", triage(telemetry[1]))''',
        "exercises": "1. Add a synthetic error-counter field. 2. Explain how maintenance can trigger a false alert. 3. Propose a time split, missed-incident metric, and alert-burden measure.",
        "summary": "Synthetic analytics can teach pipeline design but cannot validate operational quality. Explain which evidence an operator should see and why device writes are out of scope.",
    },
    "06_Practice_Exercises.ipynb": {
        "title": "Practice Exercises",
        "focus": "Practice classifying mechanisms, implementing baselines, and designing safe evaluations. Attempt these before opening solutions.",
        "beginner": "Predict output before running. Write your own cells below the starter examples; explanations and solutions are kept in another notebook.",
        "first": '''fixture = [(20.0, "normal"), (80.0, "review")]
print("Exercise examples:", fixture)
print("Write your prediction and reasoning before continuing.")''',
        "linewise": "The fixture is a list of value/label pairs. `print` shows the input to reason about. No answer is computed in this first cell.",
        "intermediate": '''def threshold_review(value, threshold):
    # TODO: replace this line with a Boolean expression.
    raise NotImplementedError("complete the exercise before calling this function")

print("Starter loaded; implement and test it in a new cell.")''',
        "advanced": '''requirements = ["time-based split", "precision and recall", "evidence shown",
                "human approval", "no device writes"]
print("Design checklist:", "; ".join(requirements))''',
        "real": '''network_fixture = [
    {"minute": 0, "latency_ms": 15, "incident": 0},
    {"minute": 1, "latency_ms": 18, "incident": 0},
    {"minute": 2, "latency_ms": 95, "incident": 1},
]
print("synthetic records:", len(network_fixture), "; no real network data used")''',
        "plot": '''import matplotlib.pyplot as plt
plt.plot([r["minute"] for r in network_fixture], [r["latency_ms"] for r in network_fixture], marker="o")
plt.xlabel("Synthetic minute")
plt.ylabel("Latency (ms)")
plt.title("Small exercise fixture; not operational telemetry")
plt.show()''',
        "debug": '''try:
    threshold_review(80, 75)
except NotImplementedError as error:
    print("Expected starter state:", error)
print("Replace the TODO before using this function.")''',
        "exercises": "Beginner: classify four mechanisms and calculate a centroid. Intermediate: build a confusion matrix for a rare event. Advanced: design read-only telemetry evaluation with uncertainty and approval.",
        "summary": "Predict first, implement second, test edge cases, then explain limitations. Do not consult `07_Exercise_Solutions.ipynb` until you have attempted each prompt.",
    },
    "07_Exercise_Solutions.ipynb": {
        "title": "Exercise Solutions",
        "focus": "Worked solutions to the separate practice notebook. Try the exercises first; alternate answers are valid when assumptions are clear.",
        "beginner": "A complete solution includes reasoning and limitations, not merely code that runs.",
        "first": '''def fit_centroids(rows):
    if not rows:
        raise ValueError("training examples are required")
    sums, counts = {}, {}
    for value, label in rows:
        sums[label] = sums.get(label, 0.0) + value
        counts[label] = counts.get(label, 0) + 1
    return {label: sums[label] / counts[label] for label in sums}

centers = fit_centroids([(10, "normal"), (14, "normal"), (70, "review"), (90, "review")])
prediction = min(centers, key=lambda label: abs(60-centers[label]))
print("means:", centers, "| prediction for 60:", prediction)''',
        "linewise": "Reject empty data, accumulate sums/counts by label, compute means, then choose the nearest mean to 60. This tiny deterministic result does not establish operational performance.",
        "intermediate": '''def threshold_review(value, threshold=75.0):
    if threshold < 0:
        raise ValueError("threshold must be non-negative")
    return value >= threshold

print([threshold_review(v) for v in (74.9, 75.0, 75.1)])''',
        "advanced": '''actual, predicted = [1, 1, 0, 0, 0], [1, 0, 0, 0, 0]
tp = sum(a == p == 1 for a, p in zip(actual, predicted))
fn = sum(a == 1 and p == 0 for a, p in zip(actual, predicted))
tn = sum(a == p == 0 for a, p in zip(actual, predicted))
print(f"TP={tp}, FN={fn}, TN={tn}; recall={tp/(tp+fn):.1%}; accuracy={(tp+tn)/len(actual):.1%}")''',
        "real": '''recommendation = {"text": "inspect interface counters",
                 "evidence": ["synthetic latency elevated"],
                 "device_write": False, "approval_required": True}
print(recommendation)''',
        "plot": '''import matplotlib.pyplot as plt
plt.bar(["recall", "accuracy"], [0.5, 0.8], color=["darkorange", "steelblue"])
plt.ylim(0, 1)
plt.ylabel("Illustrative score")
plt.title("Different metrics reveal different behavior")
plt.show()''',
        "debug": '''def validate_training(rows):
    if not rows:
        raise ValueError("training data must not be empty")

try:
    validate_training([])
except ValueError as error:
    print("Correctly rejected:", error)
print("Valid fit:", fit_centroids([(1, "a"), (3, "a")]))''',
        "exercises": "Compare your answers with `../solutions/lesson_01_solutions.md`. Add tests for invalid input and explain why model recommendations cannot grant themselves authorization.",
        "summary": "Check assumptions, use appropriate held-out data, and keep permission controls outside the model. Explain one risk that remains in this design.",
    },
    "08_Common_Errors_and_Debugging.ipynb": {
        "title": "Common Errors and Debugging",
        "focus": "Diagnose invalid model state, bad inputs, and misleading evaluation. Robust systems fail clearly instead of returning invented predictions.",
        "beginner": "An exception signals an operation could not proceed. Validation checks assumptions before use. The examples catch expected errors so the notebook has no unhandled failure.",
        "first": '''def safe_predict(value, centers):
    if not centers:
        raise ValueError("model has no fitted centroids")
    return min(centers, key=lambda label: abs(value-centers[label]))

centers = {"normal": 11.0, "review": 85.0}
print("valid prediction:", safe_predict(70.0, centers))''',
        "linewise": "The function takes a value and centroid mapping, checks model state, calculates absolute distances, and returns the nearest label. The final call uses a valid toy model.",
        "intermediate": '''for value, model in [(70, centers), (3, {}), (None, centers)]:
    try:
        print("prediction:", safe_predict(value, model))
    except (ValueError, TypeError) as error:
        print(f"rejected {value!r}: {type(error).__name__}: {error}")''',
        "advanced": '''import math
def robust_predict(value, model):
    if not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError("value must be finite numeric data")
    if not model or any(not math.isfinite(center) for center in model.values()):
        raise ValueError("model must contain finite fitted centroids")
    return min(model, key=lambda label: abs(value-model[label]))

for value in (70.0, float("nan")):
    try:
        print("result:", robust_predict(value, centers))
    except ValueError as error:
        print("validation:", error)''',
        "real": '''training = [(10, 0), (12, 0), (80, 1), (90, 1)]
print("training examples:", len(training))
print("Correct interpretation: fitting data are not an independent future-performance estimate.")''',
        "plot": '''import matplotlib.pyplot as plt
values, labels = [10, 12, 80, 90], ["class 0", "class 0", "class 1", "class 1"]
plt.scatter(values, [0]*len(values), c=["steelblue" if x == "class 0" else "darkorange" for x in labels], s=90)
plt.yticks([])
plt.xlabel("Toy measurement")
plt.title("Separated toy classes can hide real-world complexity")
plt.show()''',
        "debug": '''def validate_training(rows):
    if not rows:
        raise ValueError("training data must not be empty")

try:
    validate_training([])
except ValueError as error:
    print("Caught expected data error:", error)
print("Fix: verify ingestion and label counts before fitting.")''',
        "exercises": "1. Add finite-number checks. 2. Test equal-distance centroids and document ambiguity. 3. Identify a time-series leakage example and design a safer split.",
        "summary": "Validate inputs and fitted state, do not invent defaults, and do not call a training score a generalization estimate. Which failure should disable a recommendation service?",
    },
}


def markdown(text):
    return nbformat.v4.new_markdown_cell(text.strip())


def code(text):
    return nbformat.v4.new_code_cell(text.strip())


for filename, lesson in LESSONS.items():
    cells = [
        markdown(f"""# Introduction to AI — {lesson['title']}

**Notebook status:** execution below is saved from a local run. Python 3.13.14; deterministic, synthetic examples; no API credentials or external services.

## Section A — Introduction

{lesson['focus']}

**Prerequisites:** Python 3.11+, basic values and function calls. Install notebook support with `python -m pip install -e ".[notebooks]"`. **Objectives:** trace the code, explain its output, identify limitations, and suggest a real-world safety boundary. Full theory: [lesson notes](../lessons/01_introduction_to_artificial_intelligence.md)."""),
        code("""import sys
import matplotlib

print(f"Python {sys.version.split()[0]} | matplotlib {matplotlib.__version__}")"""),
        markdown("This environment cell records the actual interpreter and plotting-library versions used for this notebook execution. Minimum compatible dependency versions are documented in the course `pyproject.toml`."),
        markdown(f"""## Section B — Beginner explanation

{lesson['beginner']}

The code cells are runnable Python. Explanations before and after each cell distinguish the expected behavior from the actual output saved by this execution."""),
        markdown("## Section C — First Python example\n\nRead the inputs and operations before running. The output below is captured from actual execution."),
        code(lesson["first"]),
        markdown(f"""**Line-by-line walkthrough:** {lesson['linewise']}

The output immediately above is actual saved execution output. It occurs because the code uses the displayed deterministic input."""),
        markdown("## Section D — Intermediate examples\n\nThis example adds a more realistic data structure or evaluation step. Inputs are documented in the code."),
        code(lesson["intermediate"]),
        markdown("This cell's output is the result of the displayed computation. New Python operations are explained in the code and can be inspected interactively."),
        markdown("## Section E — Advanced examples\n\nThis example adds an edge case, metric, or validation concern. Consider both computational behavior and decision consequences."),
        code(lesson["advanced"]),
        markdown("Interpret each result in the context of the toy data; do not generalize the score to real deployments."),
        markdown("## Section F — Real-world applications\n\nExample application: synthetic network engineering telemetry and read-only triage. The same principles apply to AI, data science, cloud monitoring, automation, and production software."),
        code(lesson["real"]),
        markdown("No live network is contacted. Any production system needs data provenance, permissions, observability, human review, and a rollback/disable plan."),
        markdown("## Section G — Visualization\n\nThe chart below is rendered and embedded in this notebook's saved outputs. It uses the small synthetic demonstration data."),
        code(lesson["plot"]),
        markdown("The figure supports visual intuition only; it is not validation evidence."),
        markdown("## Section H — Debugging and common mistakes\n\nThe following code intentionally reaches an invalid-input path but catches the exception, leaving an inspectable message rather than an unhandled notebook error."),
        code(lesson["debug"]),
        markdown("Reject malformed input explicitly; never substitute a success-shaped prediction or silently perform an operational action."),
        markdown("## Section I — Exercises\n\n" + lesson["exercises"] + "\n\nAttempt these before using the separate `07_Exercise_Solutions.ipynb`."),
        markdown("## Section J — Summary and knowledge check\n\n" + lesson["summary"] + "\n\n**Review:** What are the input, output, assumptions, failure mode, and safe fallback? Continue with the full theory notes and then AI problem formulation: goals, state, actions, constraints, costs, and success criteria."),
    ]
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
        resources={"metadata": {"path": str(Path.cwd())}},
    ).execute()
    nbformat.write(notebook, OUTPUT / filename)
    print(f"EXECUTED {filename}: {len(notebook.cells)} cells, saved outputs")
