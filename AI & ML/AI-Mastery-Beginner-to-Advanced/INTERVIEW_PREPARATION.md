# Interview Preparation

Use these prompts for spaced retrieval. Explain assumptions and tradeoffs rather than memorizing slogans. The first lesson includes complete introductory answers; each later module will add its own tiered questions.

## First lesson: introductory prompts

1. How do AI, machine learning, and deep learning relate?
2. How does a rule-based system differ from a learned model?
3. What is the difference between supervised, unsupervised, and reinforcement learning?
4. Why does a high training score not prove a model is useful?
5. Give one example where a simple non-AI system is preferable to machine learning.

Suggested answer checkpoints: AI is the broad field; ML is a family of data/interaction-driven methods within it; deep learning uses multi-layer neural networks. Explicit rules are authored; learned parameters are fitted from data. Supervised learning uses target labels, unsupervised learning seeks structure without supplied target labels, and reinforcement learning learns from interaction/reward. A training score does not establish generalization, representative data, acceptable error costs, or safe deployment. Prefer simpler deterministic software when requirements are known, stable, and auditable.

## Progressive practice

- **Beginner:** Define input, output, model, training, inference, and label in a concrete example.
- **Intermediate:** Design an evaluation split and metric for an imbalanced alert-classification task.
- **Advanced:** Explain distribution shift and propose monitoring plus a safe fallback for a model-assisted operational decision.

