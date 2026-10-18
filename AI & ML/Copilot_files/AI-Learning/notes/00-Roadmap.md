# Complete AI Learning Roadmap

> This roadmap lives in `notes/`. The practical notebook sequence and workspace structure are documented in the workspace `README.md`.

This roadmap is ordered by prerequisites, not by popularity. Each stage builds the vocabulary and practical skills needed by the next one. The course will be developed one logical section at a time; the checklist shows what is written so far, not a requirement to finish every file now.

## How to use this roadmap

1. Follow the stages in order, but revisit earlier material when a project exposes a gap.
2. For each topic, learn the plain-English idea first, then the technical details, then implement a small example.
3. Keep a small Git repository for exercises. Use synthetic or approved data; do not place credentials, production secrets, or sensitive logs in it.
4. For network automation, begin with read-only data collection and require human approval before any change.
5. Product names, cloud features, APIs, model availability, and framework syntax change. Treat those lessons as time-sensitive and check the relevant official documentation before building against them.

## Progress checklist

- [x] Completed — `00-Roadmap.md`
- [x] Completed — `notebooks/00-Environment-Setup.ipynb` (executed; readiness checks passed)
- [ ] In Progress — `01-AI-Fundamentals.md` (first section: AI landscape and capability levels)
- [ ] Not Started — Matching notebook for `01-AI-Fundamentals.md`
- [ ] Not Started — `02-Python-for-AI.md`
- [ ] Not Started — `03-Math-for-AI.md`
- [ ] Not Started — `04-Machine-Learning.md`
- [ ] Not Started — `05-Deep-Learning.md`
- [ ] Not Started — `06-NLP.md`
- [ ] Not Started — `07-Transformers.md`
- [ ] Not Started — `08-LLMs.md`
- [ ] Not Started — `09-Prompt-Engineering.md`
- [ ] Not Started — `10-Embeddings.md`
- [ ] Not Started — `11-Vector-Databases.md`
- [ ] Not Started — `12-RAG.md`
- [ ] Not Started — `13-AI-Agents.md`
- [ ] Not Started — `14-MCP-and-Tools.md`
- [ ] Not Started — `15-Agent-Orchestration.md`
- [ ] Not Started — `16-Context-Engineering.md`
- [ ] Not Started — `17-Multimodal-AI.md`
- [ ] Not Started — `18-Fine-Tuning.md`
- [ ] Not Started — `19-AI-Evaluation.md`
- [ ] Not Started — `20-AI-Security.md`
- [ ] Not Started — `21-MLOps-LLMOps.md`
- [ ] Not Started — `22-Cloud-AI.md`
- [ ] Not Started — `23-Network-Engineering-AI.md`
- [ ] Not Started — `24-AI-System-Design.md`
- [ ] Not Started — `25-Projects.md`
- [ ] Not Started — `26-Interview-Preparation.md`

## Learning stages and prerequisite order

### Stage 1 — Beginner: build the foundation

**Goal:** Understand the basic vocabulary, work comfortably with the Python and data used in AI examples, and recognize what a model can and cannot do.

**Prerequisites:** Basic computer use. Basic Python is helpful, but the Python track starts with fundamentals and does not assume data-science experience.

1. **AI landscape and vocabulary** — AI, machine learning, deep learning, generative AI, narrow AI, models, algorithms, training, and inference. (`01-AI-Fundamentals.md`)
2. **Python foundations for practical work** — data types, collections, conditions, loops, functions, modules, exceptions, files, JSON/YAML, regular expressions, environments, packages, HTTP/REST, authentication, environment variables, async, type hints, dataclasses, Pydantic, and FastAPI. (`02-Python-for-AI.md`)
3. **Useful mathematics** — scalars, vectors, matrices, tensors, matrix operations, dot products, similarity, descriptive statistics, probability, distributions, correlation, derivatives, gradients, and gradient descent. Learn each idea visually before its notation. (`03-Math-for-AI.md`)
4. **First machine-learning workflow** — datasets, features, labels, cleaning, exploratory analysis, preprocessing, train/validation/test splits, overfitting, underfitting, metrics, and a first scikit-learn model. (`04-Machine-Learning.md`)

**Beginner checkpoint:** Explain, in your own words, how examples become a trained model and how a trained model makes a prediction on new input.

### Stage 2 — Intermediate: build and compare models

**Goal:** Select a reasonable model for a task, build repeatable experiments, and interpret the results rather than relying on a single score.

**Prerequisites:** Stage 1; comfortable Python functions, data structures, basic statistics, and train/test separation.

1. **Classical machine-learning algorithms** — linear and logistic regression, decision trees, random forests, K-nearest neighbors, support vector machines, Naive Bayes, K-means, DBSCAN, and PCA. Compare assumptions, strengths, weaknesses, and failure cases. (`04-Machine-Learning.md`)
2. **Evaluation and generalization** — confusion matrices, accuracy, precision, recall, F1, cross-validation, class imbalance, bias/variance, leakage, and baseline comparisons. (`04-Machine-Learning.md`, then `19-AI-Evaluation.md`)
3. **Neural-network foundations** — neurons, layers, weights, bias, activations, forward propagation, loss, backpropagation, optimizers, epochs, batches, learning rate, dropout, and regularization. (`05-Deep-Learning.md`)
4. **Sequence and image model families** — CNNs, RNNs, LSTMs, and GRUs; what problems motivated each family and where their limitations appear. (`05-Deep-Learning.md`)
5. **Natural-language processing progression** — text preprocessing, tokenization, n-grams, bag of words, TF-IDF, embeddings, Word2Vec, classification, entity extraction, and sentiment. Relate the progression from traditional NLP through RNNs and attention to Transformers. (`06-NLP.md`)

**Intermediate checkpoint:** Build a small, reproducible classifier, compare it with a simple baseline, select suitable metrics, and explain likely sources of error.

### Stage 3 — Advanced: understand and build LLM applications

**Goal:** Understand the mechanics of modern language models and build applications that retrieve useful context and produce measurable outputs.

**Prerequisites:** Stage 2; Python APIs and JSON; vectors and cosine similarity; basic neural-network and NLP vocabulary.

1. **Transformers** — tokens, tokenization, embeddings, positional information, queries/keys/values, self-attention, scaled dot-product attention, multi-head attention, feed-forward layers, residual connections, normalization, encoder/decoder families, context windows, and next-token prediction. (`07-Transformers.md`)
2. **Large language models** — pretraining, fine-tuning, instruction tuning, alignment, inference, sampling controls, structured output, tool calling, model families, and hallucinations. (`08-LLMs.md`)
3. **Prompt engineering** — instructions, context, examples, constraints, zero/one/few-shot prompting, templates, structured outputs, prompt injection, context management, and prompt evaluation. (`09-Prompt-Engineering.md`)
4. **Embeddings and retrieval foundations** — vector representations, embedding models, dimensions, semantic similarity, nearest neighbors, and distance measures. (`10-Embeddings.md`)
5. **Search systems** — keyword search, BM25, vector indexes, metadata filters, approximate nearest neighbors, hybrid search, and reranking. Learn the concepts before comparing FAISS, pgvector, Azure AI Search, Pinecone, Qdrant, and Weaviate. (`11-Vector-Databases.md`)
6. **Retrieval-Augmented Generation (RAG)** — ingestion, parsing, chunking, retrieval, reranking, context construction, citations, grounding, query rewriting, and retrieval/generation evaluation. (`12-RAG.md`)
7. **Multimodal systems** — text, images, audio, video, PDFs, OCR, speech, vision-language models, and multimodal prompts. (`17-Multimodal-AI.md`)
8. **Model customization choices** — prompting vs. RAG vs. fine-tuning; supervised fine-tuning, LoRA/QLoRA, PEFT, quantization, adapters, and distillation, including when not to fine-tune. (`18-Fine-Tuning.md`)

**Advanced checkpoint:** Build a small RAG prototype over approved documents, return source references, and evaluate retrieval and answer quality separately.

### Stage 4 — Expert / Production: operate reliable, safe AI systems

**Goal:** Design and operate AI applications and agents with explicit permissions, evaluation, observability, failure handling, and human oversight.

**Prerequisites:** Stage 3; API design, Git, testing, basic deployment concepts, and comfort tracing a request across components.

1. **Agents and tools** — agent vs. chatbot/workflow/RAG, tool/function calling, observe–decide–act loops, state, memory, retries, guardrails, human approval, and evaluation. (`13-AI-Agents.md`)
2. **Model Context Protocol (MCP)** — clients, servers, tools, resources, prompts, discovery, access control, authentication, sandboxing, and approval boundaries. (`14-MCP-and-Tools.md`)
3. **Orchestration and context engineering** — workflows, graphs, single/multi-agent patterns, handoffs, routing, state, memory, context selection/compression, token budgets, and observability. Compare frameworks by concepts and verify current product syntax in official docs. (`15-Agent-Orchestration.md`, `16-Context-Engineering.md`)
4. **Evaluation and security** — golden datasets, groundedness, relevance, correctness, retrieval precision/recall, tool success, regression tests, human review, judge limitations, prompt injection, data leakage, least privilege, privacy, fairness, audit logs, and safe tool design. (`19-AI-Evaluation.md`, `20-AI-Security.md`)
5. **MLOps / LLMOps** — versioning data/models/prompts, CI/CD, containers, serving, logging, tracing, monitoring, caching, scaling, cost, reliability, and deployment lifecycle. (`21-MLOps-LLMOps.md`)
6. **Cloud AI** — deployment and managed services using Azure AI services, Azure OpenAI where appropriate, Azure AI Search, Azure Machine Learning, and Microsoft Foundry/current Microsoft AI tooling. Cloud names and capabilities are time-sensitive; verify official documentation at implementation time. (`22-Cloud-AI.md`)
7. **AI system design** — model selection, RAG/agent architecture, APIs, queues and events, latency, rate limits, token economics, caching, failure handling, security, evaluation, and human-in-the-loop design. (`24-AI-System-Design.md`)
8. **Network engineering applications** — read-only troubleshooting, logs, configuration analysis, routing protocols, telemetry, incident correlation, and controlled automation. (`23-Network-Engineering-AI.md`)
9. **Portfolio and interview preparation** — complete projects with tests, evaluations, threat considerations, architecture diagrams, and clear tradeoff explanations. (`25-Projects.md`, `26-Interview-Preparation.md`)

**Production checkpoint:** Demonstrate an AI service that is testable, observable, permission-limited, evaluated against representative cases, and explicit about uncertainty and evidence.

## Recommended hands-on project sequence

Projects are deliberately ordered from simple and low-risk to integrated systems. Use synthetic examples or approved, sanitized data.

1. **Python network-data analyzer (Beginner):** Parse a small sample of interface or routing data from JSON/CSV and summarize status. No device connection.
2. **Network command explainer (Beginner):** Explain a supplied, read-only command and its output; distinguish observed facts from hypotheses.
3. **Syslog classifier (Intermediate):** Label synthetic log lines into a few incident categories; establish a baseline and evaluate precision/recall.
4. **Configuration analyzer (Intermediate):** Compare two sanitized configurations and flag differences for human review; do not generate or apply changes automatically.
5. **ML incident classifier (Intermediate):** Train a baseline model on a small, clearly documented dataset; prevent data leakage and report limitations.
6. **Network troubleshooting RAG assistant (Advanced):** Index approved runbooks, RCA notes, and device documentation; retrieve evidence, cite sources, and measure retrieval and answer quality.
7. **Multi-vendor assistant (Advanced):** Normalize Cisco IOS-XR, Juniper Junos, and Arista EOS examples into a common read-only explanation flow; keep vendor-specific claims traceable to source material.
8. **Read-only troubleshooting agent (Expert):** Route a question to approved monitoring/API tools, collect explicitly allowed evidence, retrieve runbooks, correlate results, and propose next steps without configuration changes.
9. **Production-style capstone (Expert):** Add identity and least privilege, human approval gates, audit trails, timeouts/retries, evaluation gates in CI, telemetry, cost controls, and a failure/runbook plan.

For every project, include: a README, sample inputs, expected outputs, tests, a short evaluation set, known limitations, and a security note. Never include real credentials or sensitive production data in the learning repository.

## Course file map

| File | Scope | Stage |
|---|---|---|
| `00-Roadmap.md` | Learning order, prerequisites, progress, and projects | All |
| `01-AI-Fundamentals.md` | AI/ML vocabulary, learning paradigms, datasets, and metrics | Beginner |
| `02-Python-for-AI.md` | Python, APIs, and AI/data libraries | Beginner |
| `03-Math-for-AI.md` | Practical linear algebra, statistics, and optimization | Beginner |
| `04-Machine-Learning.md` | Workflow, preprocessing, classical algorithms, and evaluation | Beginner–Intermediate |
| `05-Deep-Learning.md` | Neural networks, optimization, CNNs, and sequence models | Intermediate |
| `06-NLP.md` | Text processing through embeddings and modern NLP foundations | Intermediate |
| `07-Transformers.md` | Transformer architecture and attention | Advanced |
| `08-LLMs.md` | LLM training, inference, outputs, tools, and limitations | Advanced |
| `09-Prompt-Engineering.md` | Prompt design, structured outputs, and prompt evaluation | Advanced |
| `10-Embeddings.md` | Vector representations and semantic similarity | Advanced |
| `11-Vector-Databases.md` | Indexes and keyword/vector/hybrid retrieval | Advanced |
| `12-RAG.md` | End-to-end grounded retrieval and generation | Advanced |
| `13-AI-Agents.md` | Agent loops, tools, state, memory, and safeguards | Expert |
| `14-MCP-and-Tools.md` | MCP concepts and safe tool integration | Expert |
| `15-Agent-Orchestration.md` | Workflow/graph orchestration and framework concepts | Expert |
| `16-Context-Engineering.md` | Context, memory, retrieval, state, and token budgets | Advanced–Expert |
| `17-Multimodal-AI.md` | Text, image, audio, video, and document inputs/outputs | Advanced |
| `18-Fine-Tuning.md` | Fine-tuning and model adaptation options | Advanced |
| `19-AI-Evaluation.md` | Model, RAG, and agent evaluation | Expert |
| `20-AI-Security.md` | Security, privacy, safety, and responsible AI | Expert |
| `21-MLOps-LLMOps.md` | Delivery, serving, observability, and operations | Expert |
| `22-Cloud-AI.md` | Cloud AI concepts and time-sensitive Azure examples | Expert |
| `23-Network-Engineering-AI.md` | Networking use cases and safe architecture patterns | Expert |
| `24-AI-System-Design.md` | Production architecture, tradeoffs, and failure handling | Expert |
| `25-Projects.md` | Guided project specifications and extensions | All |
| `26-Interview-Preparation.md` | Progressive questions, explanations, and practice | All |

## Practical notebook sequence

Each notebook is created with its corresponding lesson, except the environment setup notebook, which comes first. A listed but not-yet-created notebook is a planned lesson, not an empty or prewritten placeholder. The full workspace map is maintained in the top-level `README.md`.

1. `00-Environment-Setup.ipynb`
2. `01-Python-Fundamentals.ipynb`
3. `02-NumPy-Fundamentals.ipynb`
4. `03-Pandas-Fundamentals.ipynb`
5. `04-Data-Visualization.ipynb`
6. `05-Math-for-AI.ipynb`
7. `06-Machine-Learning-Basics.ipynb`
8. `07-Regression.ipynb`
9. `08-Classification.ipynb`
10. `09-Clustering.ipynb`
11. `10-Neural-Networks.ipynb`
12. `11-PyTorch-Fundamentals.ipynb`
13. `12-NLP-Fundamentals.ipynb`
14. `13-Tokenization.ipynb`
15. `14-Transformers.ipynb`
16. `15-LLM-API-Fundamentals.ipynb`
17. `16-Prompt-Engineering.ipynb`
18. `17-Structured-Outputs.ipynb`
19. `18-Embeddings.ipynb`
20. `19-Vector-Search.ipynb`
21. `20-RAG-Basics.ipynb`
22. `21-Advanced-RAG.ipynb`
23. `22-Tool-Calling.ipynb`
24. `23-AI-Agents.ipynb`
25. `24-Agent-Memory-and-State.ipynb`
26. `25-MCP-Concepts.ipynb`
27. `26-AI-Evaluation.ipynb`
28. `27-AI-Security.ipynb`
29. `28-FastAPI-AI-Service.ipynb`
30. `29-Network-Command-Explainer.ipynb`
31. `30-Syslog-Analysis-Assistant.ipynb`
32. `31-Network-Configuration-Analyzer.ipynb`
33. `32-Network-RAG-Assistant.ipynb`
34. `33-Network-Troubleshooting-Agent.ipynb`
35. `34-End-to-End-AI-Project.ipynb`

## Prerequisite map at a glance

```text
AI vocabulary
    ↓
Python + practical math
    ↓
Data handling + classical machine learning
    ↓
Neural networks + NLP
    ↓
Transformers + LLMs + prompt design
    ↓
Embeddings + search + RAG + multimodal AI
    ↓
Agents + tools/MCP + orchestration + context engineering
    ↓
Evaluation + security + MLOps/LLMOps + cloud
    ↓
Network AI systems + production system design + capstone
```

Some topics can be revisited in parallel once their foundations are in place. For example, security and evaluation should not be postponed until after deployment: introduce them early and deepen them throughout the course.
