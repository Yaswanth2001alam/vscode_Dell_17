# Lesson 01 Exercises — Introduction to AI

Try each exercise before opening the [separate solutions](../solutions/lesson_01_solutions.md). Use your own words and show calculations where requested.

## Beginner

### 1. Identify the mechanism

For each system, classify its primary mechanism as explicit rule-based software, supervised learning, unsupervised learning, reinforcement learning, or generative AI. More than one label may apply; explain your choice.

1. A script reports an error when a required configuration field is absent.
2. A model learns from past labeled support tickets to predict a ticket category.
3. A program groups telemetry windows by similarity without incident labels.
4. A text model drafts a plain-language summary of an incident record.

### 2. Calculate a nearest-centroid prediction

Class 0 has measurements 10 and 14. Class 1 has measurements 70 and 90.

1. Calculate both class means.
2. Predict the class for a new measurement of 60 using nearest-centroid distance.
3. State one reason this prediction might be unsuitable for a real operational decision.

### 3. Critique a score

A system reports 98% accuracy on 1,000 observations. List at least three questions you would ask before deciding whether it is useful.

## Intermediate

### 4. Choose a baseline

You need to identify potentially faulty network interfaces from a daily table containing interface counters. Propose one simple baseline that does not require machine learning. State its input, output, and one limitation.

### 5. Evaluate rare incidents

Only 1 in 500 telemetry windows contains a labeled incident. Explain why accuracy alone is risky. Name two more useful evaluation measures or review methods and explain what each reveals.

### 6. Plan for deployment change

A model was evaluated using winter traffic. In summer, network usage patterns change. Describe two monitoring signals and one safe response if the model's behavior degrades.

## Advanced

### 7. Design a safe network triage assistant

Write a short design with: objective, inputs, outputs, evaluation split, at least two metrics, evidence shown to the operator, prohibited actions, and a human approval gate. Use synthetic or sanitized data.

### 8. Challenge an AI proposal

A proposal says: “Use a large language model to read router logs and automatically apply the configuration it recommends. The model is 95% accurate, so approval is unnecessary.” Identify at least six missing facts, risks, or controls. Rewrite the proposal as a safer first experiment.
