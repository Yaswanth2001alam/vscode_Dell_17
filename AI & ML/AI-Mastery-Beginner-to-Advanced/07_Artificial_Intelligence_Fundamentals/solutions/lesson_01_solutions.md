# Lesson 01 Exercise Solutions

Attempt the questions in `../exercises/lesson_01_exercises.md` first. Alternatives are acceptable when assumptions are explicit and reasoning is sound.

## Beginner

### 1. Identify the mechanism

1. Explicit rule-based software: a human-authored condition checks whether a field is absent.
2. Supervised learning: examples have known ticket-category labels used as targets.
3. Unsupervised learning: the system groups examples without supplied incident labels. The groups still need domain interpretation.
4. Generative AI: the system generates new text conditioned on an incident record. Its fluency does not establish factual correctness.

### 2. Calculate a nearest-centroid prediction

Class 0 mean: \((10+14)/2=12\). Class 1 mean: \((70+90)/2=80\). For value 60, distances are \(|60-12|=48\) and \(|60-80|=20\), so the nearest-centroid prediction is class 1. It may be unsuitable operationally because the training data are tiny and synthetic, and the model ignores other signals, costs, uncertainty, and current network context.

### 3. Critique a score

Useful questions include: Is the test set separate from training and model selection? Does it represent deployment conditions? How many positive incidents are present? What are precision and recall for incidents? What are the costs of false alarms and missed incidents? Is there leakage? Does performance vary by device, site, or time? Accuracy by itself answers none of these.

## Intermediate

### 4. Choose a baseline

For example, flag an interface when its error-counter increase exceeds an agreed threshold or when link state is down. Inputs are counter deltas and link state; output is a flag for operator review. A limitation is that fixed thresholds can trigger on benign maintenance or miss a fault whose symptoms are gradual or contextual.

### 5. Evaluate rare incidents

If every window is predicted “no incident,” accuracy is about 99.8% while recall is zero. Precision measures how many alerts correspond to incidents; recall measures the fraction of incidents detected. A precision-recall curve or threshold-specific confusion matrix shows tradeoffs. Domain review of sampled alerts and missed cases is also important; metrics do not decide acceptable operational risk by themselves.

### 6. Plan for deployment change

Monitor input-feature distributions and outcome/error rates when labels become available; also monitor alert volume, latency, and operator overrides. If degradation is detected, revert to a known safe baseline or disable recommendations, notify the owner, and investigate before retraining or changing thresholds. Do not silently let a degraded model take stronger actions.

## Advanced

### 7. Design a safe network triage assistant

A good answer scopes the goal to ranking synthetic telemetry windows for analyst review. Inputs might include timestamped latency, packet loss, and interface counters; output includes a ranking, evidence, and uncertainty—not a configuration command. Split by time or incident group to avoid leakage. Measure incident recall and precision at a review-capacity threshold, plus false alarms per day. Show contributing measurements and source timestamps. Prohibit device writes and secret exposure. Require human review before any ticket escalation or operational change; keep an audit trail and disable path.

### 8. Challenge an AI proposal

Missing issues include: what “95% accurate” means; the test population and split; incident prevalence; class-specific precision/recall; label quality; log coverage; device/vendor variation; evidence for each recommendation; permission boundaries; prompt/log injection; secrets in logs; action validation; rollback; audit trail; human responsibility; and what happens when the model is uncertain or unavailable.

A safer first experiment: run a local/offline model on sanitized or synthetic logs; have it produce cited summaries and candidate troubleshooting checks only; evaluate a versioned set of incidents against a simple baseline; measure class-specific errors and unsupported claims; log outputs without secrets; use mock read-only tools; and require an engineer to validate every recommendation. Do not connect write-capable credentials.
