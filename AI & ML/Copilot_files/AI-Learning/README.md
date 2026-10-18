# AI Learning Workspace

A beginner-to-production AI curriculum combining Markdown lessons with executable Jupyter practice. Lessons and notebooks are created in sequence rather than generating the entire course at once.

## Start here

1. Read [`notes/00-Roadmap.md`](notes/00-Roadmap.md).
2. Open and run [`notebooks/00-Environment-Setup.ipynb`](notebooks/00-Environment-Setup.ipynb) from top to bottom.
3. Continue with `notes/01-AI-Fundamentals.md`; its matching hands-on notebook will be added in the next lesson installment.

Use **Restart Kernel and Run All** when checking a notebook. The environment notebook uses synthetic/local examples and does not need API credentials, internet access, cloud resources, or a GPU. PyTorch is optional for the setup check.

## Workspace structure

```text
AI-Learning/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── notes/
│   ├── 00-Roadmap.md
│   ├── 01-AI-Fundamentals.md
│   ├── 02-Python-for-AI.md
│   ├── 03-Math-for-AI.md
│   ├── 04-Machine-Learning.md
│   ├── 05-Deep-Learning.md
│   ├── 06-NLP.md
│   ├── 07-Transformers.md
│   ├── 08-LLMs.md
│   ├── 09-Prompt-Engineering.md
│   ├── 10-Embeddings.md
│   ├── 11-Vector-Databases.md
│   ├── 12-RAG.md
│   ├── 13-AI-Agents.md
│   ├── 14-MCP-and-Tools.md
│   ├── 15-Agent-Orchestration.md
│   ├── 16-Context-Engineering.md
│   ├── 17-Multimodal-AI.md
│   ├── 18-Fine-Tuning.md
│   ├── 19-AI-Evaluation.md
│   ├── 20-AI-Security.md
│   ├── 21-MLOps-LLMOps.md
│   ├── 22-Cloud-AI.md
│   ├── 23-Network-Engineering-AI.md
│   ├── 24-AI-System-Design.md
│   ├── 25-Projects.md
│   └── 26-Interview-Preparation.md
├── notebooks/
│   ├── 00-Environment-Setup.ipynb
│   ├── 01-Python-Fundamentals.ipynb
│   ├── 02-NumPy-Fundamentals.ipynb
│   ├── 03-Pandas-Fundamentals.ipynb
│   ├── 04-Data-Visualization.ipynb
│   ├── 05-Math-for-AI.ipynb
│   ├── 06-Machine-Learning-Basics.ipynb
│   ├── 07-Regression.ipynb
│   ├── 08-Classification.ipynb
│   ├── 09-Clustering.ipynb
│   ├── 10-Neural-Networks.ipynb
│   ├── 11-PyTorch-Fundamentals.ipynb
│   ├── 12-NLP-Fundamentals.ipynb
│   ├── 13-Tokenization.ipynb
│   ├── 14-Transformers.ipynb
│   ├── 15-LLM-API-Fundamentals.ipynb
│   ├── 16-Prompt-Engineering.ipynb
│   ├── 17-Structured-Outputs.ipynb
│   ├── 18-Embeddings.ipynb
│   ├── 19-Vector-Search.ipynb
│   ├── 20-RAG-Basics.ipynb
│   ├── 21-Advanced-RAG.ipynb
│   ├── 22-Tool-Calling.ipynb
│   ├── 23-AI-Agents.ipynb
│   ├── 24-Agent-Memory-and-State.ipynb
│   ├── 25-MCP-Concepts.ipynb
│   ├── 26-AI-Evaluation.ipynb
│   ├── 27-AI-Security.ipynb
│   ├── 28-FastAPI-AI-Service.ipynb
│   ├── 29-Network-Command-Explainer.ipynb
│   ├── 30-Syslog-Analysis-Assistant.ipynb
│   ├── 31-Network-Configuration-Analyzer.ipynb
│   ├── 32-Network-RAG-Assistant.ipynb
│   ├── 33-Network-Troubleshooting-Agent.ipynb
│   └── 34-End-to-End-AI-Project.ipynb
├── data/
│   ├── sample-syslogs/
│   ├── sample-configurations/
│   ├── sample-runbooks/
│   ├── sample-incidents/
│   └── sample-telemetry/
└── projects/
    ├── network-command-explainer/
    ├── syslog-analysis-assistant/
    ├── network-configuration-analyzer/
    ├── network-rag-assistant/
    └── network-troubleshooting-agent/
```

The data and project directories are prepared for synthetic learning artifacts. Empty directories are retained with `.gitkeep` files. Future lesson files are documented in this map and are created with real lesson content in sequence, rather than as empty or non-executable placeholders.

## Safety and secrets

- Network examples use synthetic input and are read-only by default.
- Never commit `.env`, credentials, production logs, or private configuration. `.env.example` contains placeholders only.
- Do not let a model apply network changes. Require explicit authorization and human approval in any future real integration.
- Product and cloud APIs change; verify current official documentation when implementing time-sensitive integrations.

## Notebook environment

The setup notebook reports the active Python interpreter, kernel support, package availability, and a small local smoke test. It does not install packages automatically or display environment-variable values. If a required library is missing, install the listed dependencies into the same environment used by the selected Jupyter kernel, then restart the kernel.
