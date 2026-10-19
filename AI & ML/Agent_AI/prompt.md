# MASTER PROMPT — BUILD AN INTELLIGENT PYTHON AI LEARNING AGENT

## 1. Your Role

Act as a Senior Python Software Engineer, AI Agent Architect, Technical Educator, Network Automation Engineer, and Jupyter Notebook Specialist.

Your task is to design, implement, test, and document a complete Python AI Learning & Exploration Agent inside my existing VS Code workspace.

This must be a real, functional, maintainable Python project, not merely a collection of notes or example scripts.

The agent should act as my personal Python teacher, coding assistant, debugging mentor, technical research assistant, and learning-progress tracker.

**IMPORTANT: Preserve all existing files, folders, notebooks, code, configurations, and Git history. Do not delete, rename, overwrite, or restructure existing work without my explicit approval.**

## 2. Primary Objective

Build an intelligent learning environment that helps me:

1. Learn Python from absolute beginner to advanced professional level.
2. Understand programming concepts through clear, detailed explanations.
3. Practice Python with executable examples.
4. Learn through interactive Jupyter notebooks.
5. Explore advanced Python features and real-world applications.
6. Understand AI agents, LLMs, machine learning, and automation.
7. Learn Python specifically for network engineering and cloud automation.
8. Debug Python code and understand the root cause of errors.
9. Visualize concepts using graphs, diagrams, and flowcharts.
10. Track my progress and identify topics that need revision.
11. Build increasingly challenging real-world projects.
12. Learn independently through a structured, adaptive curriculum.

The system should support both a guided learning mode and a free exploration mode.

## 3. Architecture Requirements

Use Python 3.11 or newer and follow modern Python engineering practices.

Preferred technologies:

- Python
- Jupyter Notebook
- IPython
- Matplotlib
- Pandas
- NumPy
- NetworkX
- Pytest
- Ruff
- Pydantic
- python-dotenv
- Rich
- Typer
- SQLite
- Git and GitHub
- VS Code
- GitHub Copilot

Use an LLM SDK only when needed for genuine AI functionality.

Support an optional LLM provider configuration through environment variables. Never hardcode API keys or secrets.

Prefer a lightweight modular architecture. Avoid introducing large frameworks unless their capabilities are genuinely required.

The application must work in a useful offline mode without a paid API key. AI-powered features should clearly indicate when an external model is required.

## 4. Agent Capabilities

Implement the following functional modules.

### A. Python Teaching Agent

Create an interactive teacher capable of explaining concepts at three levels:

- Beginner
- Intermediate
- Advanced

For every topic, generate:

1. Learning objectives.
2. Prerequisites.
3. Intuitive explanation.
4. Technical explanation.
5. Syntax and definitions.
6. Multiple Python examples.
7. Line-by-line code explanation.
8. Expected output.
9. Real-world use cases.
10. Common mistakes.
11. Debugging techniques.
12. Exercises.
13. Solutions with explanations.
14. Interview questions.
15. A summary and revision checklist.

Do not assume that I already understand a concept.

Explain difficult concepts progressively, using simpler examples before introducing advanced implementations.

### B. Python Code Generation Agent

Generate working Python programs as `.py` files.

Every Python example must include:

- Clear purpose.
- Readable code.
- Descriptive variable names.
- Type hints where useful.
- Docstrings for reusable functions and classes.
- Comments explaining non-obvious logic.
- Example input.
- Expected output.
- Error handling where appropriate.
- Instructions for execution.

Avoid unnecessarily complex code in beginner lessons.

For advanced examples, demonstrate professional software engineering techniques.

All generated code should be runnable and tested wherever practical.

### C. Jupyter Notebook Learning Agent

Create interactive `.ipynb` notebooks for lessons that benefit from step-by-step execution, experimentation, and visualization.

Each notebook must contain:

1. Title and learning objectives.
2. Concept explanation in Markdown.
3. Mathematical or theoretical foundations where relevant.
4. Small executable Python cells.
5. Output interpretation.
6. Visualizations.
7. Guided experiments.
8. Practice questions.
9. Solutions.
10. Key takeaways.

Ensure the notebooks contain valid notebook metadata and run using the configured Python environment.

Prefer small, focused cells over large blocks of code.

When possible, execute notebooks automatically to detect errors before declaring them complete.

### D. Intelligent Debugging Agent

Create a debugging assistant that can:

- Analyze Python exceptions.
- Explain tracebacks in simple language.
- Identify likely root causes.
- Suggest minimal corrections.
- Demonstrate corrected code.
- Explain why the correction works.
- Recommend ways to prevent similar bugs.
- Generate regression tests.

The agent should teach debugging rather than simply replacing the user's code.

Never silently modify original source files.

### E. Python Exploration Agent

Support open-ended commands such as:

- Explain decorators.
- Teach me Python generators.
- Compare threads and multiprocessing.
- Demonstrate asynchronous programming.
- Show how REST APIs work.
- Explain Python memory management.
- Explore machine learning algorithms.
- Teach me how AI agents work.
- Explain the difference between a script and an AI agent.

The agent should identify prerequisites and explain unfamiliar concepts before proceeding.

### F. Network Engineering Automation Agent

Include a dedicated curriculum for Python in networking.

Topics must include:

- IPv4 and IPv6 fundamentals using Python.
- The ipaddress module.
- Socket programming.
- TCP and UDP.
- DNS automation.
- REST APIs.
- JSON and YAML.
- SSH automation.
- Netmiko.
- Paramiko.
- NAPALM.
- PyATS.
- Ansible integration.
- Cisco IOS and IOS XR.
- Juniper Junos.
- Arista EOS.
- BGP and OSPF automation.
- Interface status monitoring.
- LLDP neighbor discovery.
- LACP verification.
- Configuration validation.
- Routing table analysis.
- Network inventory management.
- Log analysis.
- Packet analysis with Scapy.
- Azure networking automation.
- Network testing and reporting.

Start with simple simulations and progress toward realistic network automation projects.

**Safety requirements:** Default to read-only network operations. Never execute configuration changes, reload devices, modify routing, or access production devices without explicit authorization. Provide dry-run capabilities wherever possible.

Never embed credentials, access tokens, or real infrastructure secrets in lessons.

### G. AI and Machine Learning Agent

Teach:

- AI fundamentals.
- Machine learning basics.
- Supervised and unsupervised learning.
- Model training and evaluation.
- Neural networks.
- Large language models.
- Prompt engineering.
- Embeddings.
- Retrieval-augmented generation (RAG).
- Tool calling.
- Agent planning.
- Agent memory.
- Multi-agent systems.
- AI safety and evaluation.

Create practical Python projects demonstrating these concepts.

Distinguish clearly between deterministic automation, LLM-assisted tools, and autonomous AI agents.

### H. Visualization Agent

Use Matplotlib, NetworkX, and appropriate Python libraries to produce:

- Flowcharts.
- Algorithm diagrams.
- Data structure illustrations.
- Execution flow diagrams.
- Network topology graphs.
- Performance charts.
- Statistical visualizations.
- Model evaluation plots.
- Learning-progress charts.

For every visualization, explain what it shows and how to interpret it.

Use Mermaid diagrams in Markdown documentation when useful.

Prefer diagrams that genuinely improve understanding instead of decorative images.

### I. Learning Progress Agent

Create a persistent learning tracker using SQLite or structured local files.

Track:

- Topics started.
- Topics completed.
- Exercises attempted.
- Exercise scores.
- Difficult topics.
- Revision requirements.
- Project completion.
- Last study date.
- Next recommended topic.

Avoid repeating completed lessons unless revision is requested or the learner needs prerequisite reinforcement.

Support commands such as:

- `progress`
- `next-topic`
- `revise`
- `practice`
- `quiz`
- `roadmap`

The agent should recommend subsequent topics based on prerequisites and demonstrated progress.

### J. Quiz and Assessment Agent

Generate quizzes at beginner, intermediate, and advanced levels.

Include:

- Multiple-choice questions.
- Output prediction questions.
- Debugging questions.
- Code completion exercises.
- Practical coding assignments.
- Scenario-based problems.

Evaluate answers and explain mistakes.

For executable coding assessments, use automated tests.

Do not execute untrusted learner code without appropriate isolation and resource limits. If a secure sandbox is unavailable, provide instructions for running tests locally rather than claiming safe isolation.

## 5. Project Folder Structure

Create the following structure, adapting it only when necessary to preserve existing files.

```text
python-ai-learning-agent/
│
├── README.md
├── pyproject.toml
├── .gitignore
├── .env.example
├── AGENTS.md
│
├── .github/
│   └── copilot-instructions.md
│
├── .vscode/
│   ├── settings.json
│   ├── extensions.json
│   └── launch.json
│
├── src/
│   └── python_learning_agent/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── orchestrator.py
│       ├── curriculum.py
│       ├── progress.py
│       ├── storage.py
│       ├── llm_client.py
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── code_runner.py
│       │   ├── notebook_builder.py
│       │   └── visualizer.py
│       └── agents/
│           ├── __init__.py
│           ├── teaching_agent.py
│           ├── debugging_agent.py
│           ├── exploration_agent.py
│           ├── network_agent.py
│           ├── quiz_agent.py
│           └── assessment_agent.py
│
├── curriculum/
│   ├── beginner.yaml
│   ├── intermediate.yaml
│   ├── advanced.yaml
│   ├── network_automation.yaml
│   └── ai_engineering.yaml
│
├── lessons/
│   ├── beginner/
│   ├── intermediate/
│   ├── advanced/
│   ├── network_automation/
│   └── ai_engineering/
│
├── notebooks/
│   ├── beginner/
│   ├── intermediate/
│   ├── advanced/
│   ├── network_automation/
│   └── ai_engineering/
│
├── examples/
├── exercises/
├── solutions/
├── projects/
├── visualizations/
├── notes/
├── reports/
├── tests/
└── data/
```

Do not generate empty placeholder modules simply to make the structure look complete. Implement modules incrementally with meaningful functionality.

## 6. Curriculum Design

Create a prerequisite-aware roadmap.

### Level 1 — Beginner

Variables, data types, operators, strings, lists, tuples, sets, dictionaries, conditions, loops, functions, modules, exceptions, and file handling.

### Level 2 — Intermediate

Object-oriented programming, comprehensions, iterators, generators, decorators, context managers, regular expressions, typing, logging, testing, and package management.

### Level 3 — Advanced

Concurrency, multiprocessing, asynchronous programming, performance optimization, memory management, design patterns, architecture, dependency injection, and advanced testing.

### Level 4 — Professional Python

REST APIs, databases, packaging, CI/CD, Docker, Git, secure coding, observability, and production-ready application development.

### Level 5 — Network Automation

Develop practical tools for network discovery, inventory, monitoring, validation, configuration comparison, protocol troubleshooting, and automated testing.

### Level 6 — AI Engineering

Develop increasingly sophisticated AI applications using model APIs, structured outputs, tool calling, RAG, evaluation, memory, and agent orchestration.

Each level must include structured lessons, exercises, assessments, and a capstone project.

## 7. Notes Generation Standards

This is a critical requirement.

Generate high-quality educational notes for every lesson.

Use Markdown `.md` files for permanent reference notes, `.py` files for standalone code, and `.ipynb` files for interactive learning.

Each lesson should have consistent naming.

Example:

```text
lessons/beginner/01_variables/
    README.md
    notes.md
    examples.py
    exercises.py
    solutions.py

notebooks/beginner/
    01_variables.ipynb
```

Notes must be:

- Detailed.
- Technically accurate.
- Beginner-friendly.
- Professionally formatted.
- Structured with meaningful headings.
- Rich in executable examples.
- Easy to revise before interviews.
- Clear about prerequisites and assumptions.

Include diagrams and tables when helpful.

Never provide only a definition and one example for a major concept.

Include both conceptual understanding and practical implementation.

## 8. AI Agent Orchestration

Implement an orchestrator that routes requests to the appropriate module.

Example:

User: "Teach me Python decorators."

Action: Teaching agent retrieves or generates the lesson, creates examples, and recommends practice.

User: "Why is this Python code failing?"

Action: Debugging agent explains the exception and suggests a correction.

User: "Create an OSPF automation lab."

Action: Network agent generates a simulated lab, scripts, tests, and documentation.

User: "Show my progress."

Action: Progress module displays completed topics and recommends the next lesson.

The system must support an offline mode and an optional AI-assisted mode.

For AI-assisted mode:

- Use structured responses where appropriate.
- Validate generated content.
- Apply tool permission controls.
- Log errors without exposing secrets.
- Clearly distinguish model-generated claims from verified results.
- Avoid arbitrary shell execution.
- Request approval before modifying important files.

Do not claim that a component is intelligent or autonomous unless it has actually been implemented and tested.

## 9. Command-Line Interface

Build a practical CLI using Typer or a similarly lightweight library.

Example commands:

```bash
python -m python_learning_agent learn variables
python -m python_learning_agent explain decorators
python -m python_learning_agent practice loops
python -m python_learning_agent quiz functions
python -m python_learning_agent progress
python -m python_learning_agent next-topic
python -m python_learning_agent roadmap
python -m python_learning_agent explore asyncio
```

Implement real command handlers, not placeholder print statements.

If a command requires an LLM API, report the missing configuration clearly and provide an offline alternative where possible.

## 10. Quality Assurance

Set up:

- Pytest.
- Ruff.
- Type checking where practical.
- Unit tests.
- Integration tests.
- Notebook validation.
- Dependency management.
- GitHub Actions CI.

Use fixtures and mocks for external services.

Tests must not require real network device credentials or a paid AI API.

Validate Python syntax and notebook structure.

Provide a documented command for running all checks.

## 11. GitHub Copilot Integration

Create:

- `AGENTS.md` containing repository-wide agent instructions.
- `.github/copilot-instructions.md` containing coding conventions and teaching requirements.
- `.vscode/settings.json` for project-specific editor settings.
- `.vscode/extensions.json` recommending relevant extensions.
- `.vscode/launch.json` for debugging the CLI.

Use supported configuration formats for the installed versions of VS Code and GitHub Copilot.

Do not invent unsupported VS Code settings or Copilot features.

## 12. Implementation Strategy

Do not attempt to build every feature simultaneously.

Implement in phases.

**Phase 1 — Working foundation**

- Inspect existing workspace.
- Create the project structure.
- Configure the Python environment.
- Build the CLI.
- Implement the curriculum loader.
- Implement local progress tracking.
- Generate one complete beginner lesson.
- Generate one valid executable notebook.
- Add tests.
- Create the README.

**Phase 2 — Teaching functionality**

- Add structured notes generation.
- Add examples and exercises.
- Add quiz evaluation.
- Add topic recommendations.
- Add visualization support.

**Phase 3 — AI capabilities**

- Implement the optional LLM adapter.
- Implement agent routing.
- Add debugging and exploration.
- Add structured-output validation.
- Add permission and safety controls.

**Phase 4 — Specialized learning**

- Implement network automation lessons.
- Implement AI engineering lessons.
- Add practical projects and assessments.

**Phase 5 — Professionalization**

- Add CI.
- Improve test coverage.
- Improve error handling.
- Improve documentation.
- Validate notebooks.
- Review security and maintainability.

At the end of each phase, provide:

1. Files created or modified.
2. Features implemented.
3. Tests executed.
4. Test results.
5. Known limitations.
6. Instructions to run the project.
7. Recommended next steps.

Do not describe unimplemented features as completed.

## 13. First Demonstration

After Phase 1, create a complete demonstration lesson titled:

"Python Variables, Data Types, and Memory Fundamentals"

Generate:

- Detailed Markdown notes.
- A standalone Python script.
- An interactive Jupyter notebook.
- At least five executable examples.
- At least five exercises.
- Exercise solutions.
- A quiz.
- Relevant visualizations.
- Unit tests.
- Instructions to run everything.

Demonstrate the CLI using this lesson.

## 14. Important Development Rules

- Preserve existing work.
- Never overwrite files without approval.
- Never delete existing code without approval.
- Never expose secrets.
- Never silently install packages.
- Never claim tests passed unless they actually ran.
- Avoid unnecessary dependencies.
- Use readable, maintainable Python.
- Prefer working functionality over elaborate architecture.
- Generate genuinely educational explanations.
- Do not skip the conceptual foundations.
- Keep beginner lessons understandable.
- Make advanced lessons technically rigorous.
- Include actual code and expected output.
- Use `.py` and `.ipynb` appropriately.
- Make notebooks reproducible.
- Document environment requirements.
- Maintain consistent naming conventions.
- Request approval before destructive or security-sensitive operations.

## 15. Final Instruction

Start by inspecting the current VS Code workspace and presenting a concise implementation plan.

Then implement Phase 1 completely.

Create actual working files rather than merely describing them.

Run available validation checks.

Show me exactly how to launch the learning agent from the VS Code terminal.

After Phase 1, stop and provide a completion report. Ask for confirmation before proceeding to Phase 2.

The ultimate goal is to build a reliable, expandable, professional Python AI Learning & Exploration Agent that teaches me programming, helps me practice, supports network engineering automation, and progressively develops my AI engineering skills.
