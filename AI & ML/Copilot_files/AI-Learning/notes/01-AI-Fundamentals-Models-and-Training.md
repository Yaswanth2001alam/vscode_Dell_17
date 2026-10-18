# AI Fundamentals — Models, Data, Training, and Inference

> **Continuation of:** `notes/01-AI-Fundamentals.md`  
> **Matching practice:** `notebooks/01-AI-Fundamentals-Models-and-Training.ipynb`  
> **Scope:** Model, algorithm, dataset, feature, label, parameter, weight, bias, training, and inference. This supplemental continuation preserves the original lesson unchanged.

## 1. A model learns a mapping

### Simple explanation

A **model** is a learned or specified way to turn input into an output. For example, a model might take network counters and estimate whether a link is likely to have a fault. A model does not automatically know networking: it only processes inputs according to how it was designed and, when learned, the examples and objective used to fit it.

### Why we need it

We use a model when we want a system to apply a pattern consistently to new inputs. A model can help rank, classify, estimate, or generate. Its output is not automatically correct; we must evaluate it for the task and context.

### Algorithm versus model

- An **algorithm** is a procedure: the recipe used to solve a problem.
- A **model** is the fitted result or representation that the procedure produces, which can then be used to make outputs.

Analogy: a training algorithm is a recipe for fitting a line to example points; the trained model is the particular line that was fitted.

### Input → processing → output

```text
INPUT: measured values for a new case
   ↓
PROCESSING: apply the fitted model's learned parameters
   ↓
OUTPUT: a score, predicted value, class, or generated content
```

## 2. Dataset, features, and labels

A **dataset** is a collection of examples. A **feature** is an input value that describes an example. A **label** is the answer associated with an example when the learning task supplies known answers.

For a simple, synthetic link-health dataset:

| Example | CRC errors per minute (feature) | Interface state (label) |
|---|---:|---|
| 1 | 0 | healthy |
| 2 | 2 | healthy |
| 3 | 80 | investigate |

The feature is evidence provided to the model; the label is the target answer it is asked to learn. The label is not necessarily a proven root cause. If labels are noisy, incomplete, or based on an incorrect assumption, a model can learn that error.

### Important distinction

Features must be available when making a real prediction. If a training dataset includes information that only becomes known after an incident, the model can appear excellent in testing but fail in real use. This is a form of **data leakage**; it will be studied further with machine-learning evaluation.

## 3. Parameters: weights and bias

A **parameter** is a value the fitting process can adjust. In a simple linear model:

```text
prediction = weight × feature + bias
```

- A **weight** controls how much a feature contributes to the model's output.
- A **bias** is an adjustable offset, allowing the output to be shifted even when the input feature is zero.

These terms have multiple meanings in different contexts. In this simple equation, weight and bias are learned parameters. “Bias” can also refer to a different statistical idea—the error from overly simple assumptions—which is not the same as the bias parameter in this equation.

## 4. Training versus inference

**Training** is the process of using examples and an objective to choose model parameters. **Inference** is using the already-fitted model to calculate output for new input.

```text
TRAINING
examples (features + labels)
  → model algorithm compares predictions with labels
  → adjust parameters to reduce a defined error
  → fitted model

INFERENCE
new features
  → fitted model with parameters held fixed
  → prediction
```

Training and inference are not synonyms. A model may be trained once and used for many predictions; production systems may retrain it later as data and requirements change.

## 5. A tiny model we can inspect

Consider this deliberately simple rule-like predictor:

```python
def predict_link_risk(crc_errors_per_minute: float, weight: float, bias: float) -> float:
    return weight * crc_errors_per_minute + bias
```

The function expects one numeric feature and two chosen parameters. It returns a score, not a probability unless a model design and calibration make that interpretation valid. The parameters shown here are supplied directly; this function does not train itself.

The notebook uses a small synthetic dataset to demonstrate fitting a line and then applying it to a held-out example. A tiny demo makes the mechanics visible, but it is **not** a validated operational fault predictor.

## 6. How a simple training loop works

For a linear prediction, choose initial parameters, predict each training value, measure prediction error using a **loss function**, and update the parameters to reduce that loss. A loss function is a numeric measure of how far predictions are from target answers. Later lessons will explain optimization and gradient descent more deeply.

```text
features + labels
      ↓
current parameters → predictions
      ↓                 ↓
      └── compare with target labels
                    ↓
                 loss score
                    ↓
             update parameters
```

Training is iterative because the system usually does not know the best parameters at the start. It changes them, measures the result, and repeats according to a chosen algorithm.

## 7. Network engineering connection

Suppose the goal is to estimate a numeric “investigation score” from a synthetic CRC counter. The input feature might be CRC errors per minute, and the target label might be an engineer-reviewed score from historical, approved examples. Training would use past feature/label pairs; inference would score a new measurement.

This setup does **not** establish a root cause. CRC errors can have multiple explanations, and one feature is not enough to diagnose a live network. Use read-only synthetic data for learning, show evidence, and require engineer review before operational decisions.

## 8. Common mistakes

- Calling training and inference the same operation.
- Treating an algorithm (the fitting procedure) as the fitted model.
- Assuming labels are ground truth just because they are in a table.
- Using features at prediction time that would not actually be available then.
- Calling every numeric score a probability.
- Thinking a model learns automatically just because its prediction function is called.
- Interpreting this tiny synthetic example as a reliable troubleshooting system.

## 9. Key takeaways

1. A dataset contains examples; features describe inputs and labels provide target answers.
2. An algorithm is a procedure; the fitted model is what inference applies.
3. Weights and bias are examples of adjustable parameters.
4. Training uses examples to fit parameters; inference uses the fitted parameters on new inputs.
5. Loss measures a mismatch according to a chosen objective.
6. Data quality and label quality limit what a model can learn.
7. A plausible model score is not automatically a diagnosis or a probability.

## 10. Section quiz

1. In one sentence each, distinguish an algorithm from a trained model.
2. In a table of interface counters and incident categories, which column might be a feature and which might be a label?
3. What is the difference between training and inference?
4. In `y = weight * x + bias`, which values are parameters and which is the input?
5. Why can a high-quality-looking label still be misleading?
6. Why should the synthetic CRC example not be used to declare the cause of a real outage?

### Quiz answers

1. An algorithm is a procedure for fitting or computing; a trained model is the fitted representation used to produce outputs.
2. A counter such as CRC errors can be a feature; an engineer-reviewed category can be a label.
3. Training chooses/fits parameters from examples; inference applies the fixed fitted model to input.
4. `weight` and `bias` are parameters; `x` is the input feature; `y` is the output.
5. Labels can be incomplete, inconsistent, or based on mistaken causal assumptions.
6. It uses synthetic data, one limited feature, and no validated evidence; real counters can have multiple causes and require corroboration.

## What to request next

Continue the fundamentals course with **learning paradigms and task types**: supervised, unsupervised, semi-supervised, self-supervised, and reinforcement learning; classification, regression, clustering; and the train/validation/test split. The matching notebook should visualize these ideas using small synthetic examples.
