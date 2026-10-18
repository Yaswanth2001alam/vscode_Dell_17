# Complete Syllabus and Delivery Status

The curriculum below is the planned scope. A listed topic is not considered taught until a detailed lesson and its practice materials are written and validated. Current completion is tracked in [LEARNING_PROGRESS.md](LEARNING_PROGRESS.md).

| # | Module | Planned coverage | Prerequisites | State |
|---:|---|---|---|---|
| 00 | Getting Started | VS Code, terminal, Python, Git, environments, testing, course workflow | None | Scaffold |
| 01 | Computer Science Fundamentals | Algorithms, complexity, data structures, operating systems, networking, HTTP, Git | 00 | Planned |
| 02 | Python Beginner | Values, types, expressions, control flow, functions, collections, files, exceptions | 00-01 | Planned |
| 03 | Python Intermediate | Modules, typing, iterators, comprehensions, OOP, testing, logging, JSON/CSV | 02 | Planned |
| 04 | Python Advanced | Data model, decorators, generators, async/concurrency, profiling, packaging, design | 03 | Planned |
| 05 | Mathematics for AI | Algebra, vectors/matrices, calculus, probability, statistics, optimization, information theory | 01-02 | Planned |
| 06 | Data Science | Data lifecycle, NumPy/Pandas, visualization, cleaning, leakage, feature engineering, reproducibility | 02-05 | Planned |
| 07 | AI Fundamentals | Definitions, history, categories, symbolic/learning systems, applications, limitations | 00-02 | In progress; lesson 01 authored |
| 08 | ML Fundamentals | Tasks, data, baselines, loss, splits, generalization, evaluation, leakage | 05-07 | Planned |
| 09 | Supervised Learning | Regression, classification, trees, ensembles, SVM, neighbors, metrics, calibration | 08 | Planned |
| 10 | Unsupervised Learning | Clustering, PCA, anomaly detection, association, evaluation, representation | 08 | Planned |
| 11 | Advanced ML | Ensembles, feature selection, imbalance, interpretability, uncertainty, causal caution | 09-10 | Planned |
| 12 | Deep Learning Fundamentals | Tensors, perceptrons, activations, losses, backprop, optimization, regularization | 05, 08 | Planned |
| 13 | Neural Network Architectures | MLPs, CNNs, sequence models, normalization, residuals, attention, generative architectures | 12 | Planned |
| 14 | PyTorch and TensorFlow | Tensors, autodiff, data pipelines, training loops, checkpoints, deployment | 12-13 | Planned |
| 15 | Natural Language Processing | Text normalization, tokenization, vectorization, classification, sequence tasks, evaluation | 08, 12-14 | Planned |
| 16 | Attention and Transformers | Attention derivation, positional signals, encoder/decoder, masking, computation | 05, 15 | Planned |
| 17 | Large Language Models | Tokenization, embeddings, pretraining, inference, sampling, context, evaluation, alignment, limits | 16 | Planned |
| 18 | Generative AI | Autoregressive models, VAE/GAN/diffusion concepts, generation evaluation, provenance | 12, 16-17 | Planned |
| 19 | Prompt Engineering | Instruction design, structured output, examples, tool use, testing, injection awareness | 17 | Planned |
| 20 | Embeddings and Vector Databases | Similarity, indexing, vector stores, filtering, hybrid search, retrieval metrics | 15-17 | Planned |
| 21 | RAG Systems | Ingestion, parsing, chunking, retrieval, reranking, grounded answers, citations, evaluation | 20 | Planned |
| 22 | AI Agents | Tools, planning, state, memory, orchestration, approvals, tracing, evaluation, boundaries | 17, 21, 30 | Planned |
| 23 | MCP and Tool Integration | Protocol concepts, schemas, clients/servers, authorization, safe tool integration | 22 | Planned |
| 24 | Fine Tuning and Optimization | Data design, fine-tuning, adapters, quantization, distillation, inference optimization | 14, 17 | Planned |
| 25 | Multimodal AI | Vision-language, audio/text, alignment, modality encoders, evaluation, risks | 13-17 | Planned |
| 26 | Computer Vision | Image representation, CNNs, classification, detection, segmentation, robustness | 12-14 | Planned |
| 27 | Speech and Audio AI | Signals, features, ASR, speech synthesis, audio classification, metrics | 12-17 | Planned |
| 28 | Reinforcement Learning | MDPs, returns, Bellman equations, value/policy methods, exploration, safety | 05, 08, 12 | Planned |
| 29 | Graph AI | Graph fundamentals, network measures, embeddings, message passing, GNNs | 05, 08, 12 | Planned |
| 30 | AI Application Engineering | APIs, UX, validation, auth, persistence, testing, error handling, safe integration | 03, 08 | Planned |
| 31 | MLOps and LLMOps | Data/model versions, CI/CD, evaluation, deployment, monitoring, drift, rollback, cost | 14, 30 | Planned |
| 32 | Cloud AI and Infrastructure | Cloud primitives, containers, orchestration, identity, storage, networking, cost controls | 30-31 | Planned |
| 33 | AI Security and Governance | Threat models, privacy, injection, data/model supply chain, evaluation, governance | 17, 21-23, 30 | Planned |
| 34 | Distributed AI and Advanced Training | Parallelism, accelerators, distributed optimization, communication, checkpointing, scaling | 14, 31 | Planned |
| 35 | Advanced AI Research | Literature, hypotheses, experimental design, reproducibility, ablation, critique, writing | Specialization-dependent | Planned |
| 36 | AI for Network Engineering | Routing, telemetry, logs, anomaly detection, forecasting, RAG, agents, Azure, change safety | 06, 08-11, 21-23, 30-33 | Planned |
| 37 | Real-World Projects | Staged beginner-to-expert capstones with architecture, source, tests, data, evaluation, limits | Varies | Planned |
| 38 | Interview Questions | Foundations through systems/design; explained answers and practice prompts | Relevant modules | Planned |
| 39 | Cheat Sheets | Math, Python, ML, deep learning, LLM, RAG, operations quick references | Relevant modules | Planned |
| 40 | Research Papers and References | Verified sources, reading notes, reproducibility guidance, topic maps | 35 or specialization | Planned |

## Cross-cutting requirements

Every authored concept lesson follows the A-X format in the master prompt where applicable: objectives, prerequisites, gradual explanation, mechanism, diagrams, mathematical treatment, runnable implementation, examples, pitfalls, comparisons, applications, performance, security/limits, interview questions, exercises with separate solutions, project, checks, summary, and verified references. For topics that do not require code, worked demonstrations replace code rather than leaving a gap.

All code should state its runtime/dependency assumptions, use synthetic or reproducible data, avoid secrets, explain CPU/GPU requirements, and distinguish local/free work from paid/cloud services. Potentially disruptive network actions remain read-only by default and require explicit human approval.
