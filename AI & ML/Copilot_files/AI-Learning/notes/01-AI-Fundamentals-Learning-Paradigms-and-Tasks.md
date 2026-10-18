# AI Fundamentals — Learning Paradigms, Tasks, and Data Splits

> **Continuation of:** `notes/01-AI-Fundamentals-Models-and-Training.md`  
> **Matching hands-on lesson:** `notebooks/01-AI-Fundamentals-Learning-Paradigms-and-Tasks.ipynb`  
> **Scope:** supervised, unsupervised, semi-supervised, self-supervised, and reinforcement learning; classification, regression, clustering; and train/validation/test data.

## 1. First ask: what kind of answer do we need?

Before choosing a learning method, state the task and what a useful output looks like. Similar input data can support different tasks depending on the question.

| Task | Output | Example question | Typical learning setup |
|---|---|---|---|
| Classification | A category | “Is this log event a link failure or something else?” | Supervised |
| Regression | A number | “How many minutes until utilization crosses a threshold?” | Supervised |
| Clustering | Groups discovered from similarities | “Which unlabeled alarms appear to form recurring patterns?” | Unsupervised |
| Generation | New content or continuation | “Draft a summary from these approved incident notes.” | Often self-supervised pretraining followed by other stages |
| Sequential decision-making | An action chosen over time | “Which safe diagnostic query should be run next?” | Reinforcement learning is one possible approach |

These are common pairings, not strict identities. For example, clustering is usually unsupervised, but clustering output can later be reviewed and labeled.

## 2. Supervised learning

### Simple explanation

**Supervised learning** uses examples where each input has a target answer (a label). The learning algorithm adjusts a model so its outputs match those example answers as well as possible.

```text
feature inputs + known labels
          ↓
      training
          ↓
      fitted model
          ↓
 new features → predicted label/value
```

### Why use it?

Use supervised learning when you have examples of the answer you want to predict and those answers are sufficiently reliable for the task.

- **Classification:** predict one of a set of categories, such as `normal`, `warning`, or `critical`.
- **Regression:** predict a numeric quantity, such as expected traffic volume.

### Network example

Synthetic log messages paired with engineer-reviewed categories could train a classifier. The category represents the training target, not guaranteed root cause. Labels should have clear definitions and a review process.

### Common mistakes

- Treating labels as unquestionable truth.
- Measuring performance on the same examples used for training.
- Using information in training that would not be available at the time of a real prediction.
- Assuming a predicted category proves why an incident happened.

## 3. Unsupervised learning

### Simple explanation

**Unsupervised learning** looks for structure in inputs that do not come with the target answers. It can group similar examples or compress data into a smaller representation.

```text
unlabeled examples → structure-finding algorithm → groups or representation
```

**Clustering** is a task that groups examples according to a measure of similarity. A cluster is a group created by an algorithm; it is not automatically a meaningful incident category.

### Why use it?

It can help explore data when categories are unavailable, expensive to create, or not yet understood. Engineers then inspect and interpret the resulting groups.

### Network example

Clustering synthetic telemetry summaries might reveal a group of samples with similar interface counters. That group may suggest an investigation direction, but it is not itself a diagnosis.

### Common mistakes

- Assuming every discovered group has operational meaning.
- Comparing clustering output without checking feature scales and distance choices.
- Treating cluster identifiers like stable labels; cluster number `0` has no inherent meaning.

## 4. Semi-supervised learning

### Simple explanation

**Semi-supervised learning** uses a smaller set of labeled examples together with a larger set of unlabeled examples. The labeled examples provide target guidance; unlabeled examples can help under particular assumptions about the data structure.

```text
small labeled set ─┐
                   ├→ semi-supervised training
large unlabeled set┘
```

### When useful?

It can be useful when trustworthy labels are expensive but collecting raw examples is easier. Unlabeled data does not magically become correct supervision: the method's assumptions must fit the data.

### Network example

An operations team may have a limited set of reviewed incident logs and many unreviewed logs. A semi-supervised approach might use both, but engineers still need to measure whether it improves results on a separate, reviewed test set.

## 5. Self-supervised learning

### Simple explanation

**Self-supervised learning** creates a learning target from the input data itself. Instead of asking a person to label every example, the system hides, transforms, or shifts part of the input and learns to predict the held-out part.

```text
raw text → hide next token → train model to predict it
```

Language-model pretraining commonly uses this broad idea: text provides its own prediction targets. This does not mean the raw text is free of bias, errors, or sensitive information.

### Network example

A toy exercise can train on a synthetic sequence of event tokens and ask the model to predict the next token. This demonstrates target construction, not a production-quality language model.

## 6. Reinforcement learning

### Simple explanation

**Reinforcement learning (RL)** studies how an **agent** selects actions in an **environment** over time and receives **rewards** or penalties. The goal is to learn a policy—a rule for selecting actions—that accumulates useful reward.

```text
state → agent chooses action → environment returns new state + reward
  ↑                                             |
  └──────────────── next decision ─────────────┘
```

### Why use it?

RL is suited to sequential decisions where actions affect later states and outcomes. It is not the default choice for every automation task; a fixed workflow or supervised model may be simpler and safer.

### Network example and safety boundary

A toy simulation can choose between two simulated, non-operational actions and receive a reward. Do not let a learning agent experiment against production network devices. Real infrastructure requires explicit authorization, constrained tools, human approval, and extensive testing; this course defaults to synthetic or read-only examples.

## 7. Training, validation, and test data

When data is limited, we separate examples by purpose:

- **Training set:** examples used to fit model parameters.
- **Validation set:** examples used during development to compare model settings or make design choices.
- **Test set:** held back until the end for a final, less-biased evaluation of the chosen approach.

```text
all eligible data
   ├── training: learn parameters
   ├── validation: choose among development options
   └── test: final evaluation after choices are finished
```

Random splitting is not always valid. Time-ordered logs, repeated device records, or near-duplicate incidents may require time-based or group-based splits so closely related examples do not leak across sets.

### Common mistakes

- Tuning repeatedly against the test set until it is no longer an independent final check.
- Splitting time-series records randomly when future examples should not inform past predictions.
- Putting duplicate or same-incident records into both training and test sets.
- Ignoring class imbalance or the cost of different error types.

## 8. Choosing a paradigm: practical decision path

```text
Do you have reliable target answers?
  ├─ Yes → Is the answer a category? → classification
  │       Is it a number? → regression
  └─ No  → Want to discover groups? → clustering / unsupervised exploration
          Have few labels plus many unlabeled inputs? → investigate semi-supervised methods
          Can targets be derived from the input itself? → self-supervised learning

Does each action affect later states and rewards?
  └─ Maybe RL, but first compare a fixed workflow or supervised approach.
```

This is a starting point, not an automatic algorithm selector. Define evaluation criteria, safety boundaries, and available data before implementation.

## 9. Python progression in the companion notebook

The notebook uses small synthetic examples and generated graphs to compare:

1. Category prediction with classification.
2. Numeric prediction with regression.
3. Unlabeled group discovery with clustering.
4. Target construction ideas for semi-supervised and self-supervised learning.
5. An isolated toy reward loop for reinforcement learning.
6. Training/validation/test separation, including stratification for imbalanced labels.

All plots are teaching aids. A two-dimensional synthetic example is easier to see than most real operational datasets, and its simplicity is not evidence that real incidents separate so cleanly.

## 10. Key takeaways

1. The task's desired output helps determine the learning setup.
2. Classification predicts categories; regression predicts numbers; clustering finds groups without supplied labels.
3. Supervised learning uses labeled examples.
4. Unsupervised learning seeks structure without target labels.
5. Semi-supervised methods combine labeled and unlabeled data under method-specific assumptions.
6. Self-supervised learning derives training targets from the input.
7. Reinforcement learning studies sequential action and reward; production network experimentation is unsafe without strict controls.
8. Training fits; validation guides development; test data supports the final evaluation.
9. Time, device, and incident relationships can make naive random splits misleading.

## 11. Quiz

1. Predicting `normal`, `warning`, or `critical`: classification or regression?
2. Predicting next-hour traffic volume: classification or regression?
3. Grouping unlabeled telemetry samples: supervised or unsupervised?
4. What distinguishes semi-supervised from self-supervised learning?
5. Why should the test set not be used repeatedly to tune model choices?
6. Why can random splitting be misleading for time-ordered incident logs?
7. Is a cluster automatically a root-cause category?
8. What are state, action, and reward in the RL loop?

### Quiz answers

1. Classification: the output is one category.
2. Regression: the output is numeric.
3. Usually unsupervised clustering, because target labels are not supplied.
4. Semi-supervised learning combines a labeled subset and unlabeled examples; self-supervised learning derives targets from the input itself.
5. Repeated tuning leaks information from the test set into development decisions, weakening its role as an independent final check.
6. Future or closely related examples can inform predictions for earlier or test examples, making evaluation unrealistically optimistic.
7. No. A cluster is an algorithm-produced grouping that requires interpretation and validation.
8. A state describes the current situation, an action is a selected step, and reward is feedback from the environment.

## What to request next

Continue with **evaluation foundations**—overfitting, underfitting, bias and variance, accuracy, precision, recall, F1, and confusion matrices—using synthetic network-event examples and visualizations.
