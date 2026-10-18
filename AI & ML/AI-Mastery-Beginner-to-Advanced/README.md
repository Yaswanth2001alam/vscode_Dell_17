# AI Mastery: Beginner to Advanced

A structured, practice-first course for progressing from programming and AI foundations to production AI engineering and research. The course combines conceptual lessons, mathematics, runnable code, exercises, projects, testing, and responsible deployment practices.

> **Course status (October 17, 2026):** Curriculum map created. The first lesson, [Introduction to Artificial Intelligence](07_Artificial_Intelligence_Fundamentals/lessons/01_introduction_to_artificial_intelligence.md), is developed; the remaining module lessons are planned, not yet authored.

## Start here

1. Read [00 Getting Started](00_Getting_Started/README.md) and create a Python virtual environment.
2. Review the [roadmap](COURSE_ROADMAP.md) and [complete syllabus](COMPLETE_SYLLABUS.md). Follow prerequisites rather than skipping straight to advanced topics.
3. Study the [first lesson](07_Artificial_Intelligence_Fundamentals/lessons/01_introduction_to_artificial_intelligence.md) and its [executed notebook sequence](07_Artificial_Intelligence_Fundamentals/01_Introduction_to_Artificial_Intelligence/README.md); attempt exercises before opening their separate solutions.
4. Run the examples and tests as described below.
5. Update [learning progress](LEARNING_PROGRESS.md) as you complete work.

## Local setup

Requires Python 3.11 or newer. Plain Python lesson examples use the standard library. To run the introductory notebooks and render their plots, install the notebook extra:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[test,notebooks]"
python -m unittest discover -s tests -v
```

If PowerShell blocks activation, use `.\.venv\Scripts\python.exe` directly. On macOS/Linux, activate with `source .venv/bin/activate`.
Open `.ipynb` files in VS Code and select the `.venv` Python kernel. The introductory notebooks were executed with Python 3.13.14; saved outputs are in the notebook files. Re-execution may update outputs.

Run the demonstrations from this directory:

```powershell
python 07_Artificial_Intelligence_Fundamentals\examples\ai_categories.py
python 07_Artificial_Intelligence_Fundamentals\examples\tiny_classifier.py
```

## Repository map

- `00_Getting_Started` through `40_Research_Papers_and_References`: sequential learning modules and capstone references.
- `datasets`, `notebooks`, `shared_utils`, and `tests`: reusable learning assets and validation.
- `COURSE_ROADMAP.md`: stages, prerequisites, estimates, and suggested schedules.
- `COMPLETE_SYLLABUS.md`: scope and completion state for each module.
- `PROJECT_PORTFOLIO.md`: progressive project track and acceptance criteria.

Each module README describes intended outcomes, prerequisites, and planned lesson inventory. For programming-related lessons, the course standard is a detailed Markdown lesson plus useful executable notebooks for beginner/intermediate/advanced and real-world examples, exercises, separate solution notebooks, and debugging. Notebooks must retain outputs only after actual successful execution; otherwise mark them `NOT EXECUTED` and leave outputs empty. A module is marked complete only after its lessons, notebooks, code, exercises, solutions, and relevant tests are authored and checked; module briefs are not substitutes for those materials.

## Learning approach

For each lesson, read actively, predict example output, run code, change one assumption, debug an intentional fault, complete exercises without peeking, then explain the result in your own words. Record blockers and test evidence in the progress tracker. For any real infrastructure, financial, health, or other consequential application, treat models as decision support and require domain review.

## Environment and privacy

Never place credentials or private customer/network data in notebooks, source files, commits, or prompts. `.env.example` contains non-secret configuration names only. Use synthetic or sanitized data in labs; cloud or paid APIs are explicitly identified before they are introduced.

## Course references

The first lesson includes a short, verified reference list. Additional references will be added as the corresponding modules are developed.
