"""Practical offline CLI. Learner code is displayed, never automatically executed."""

import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Annotated

import typer
import yaml
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

from python_learning_agent.config import Settings
from python_learning_agent.orchestrator import LearningAgent

app = typer.Typer(no_args_is_help=True, help="Offline Python teacher: Phase 1 foundation.")
console = Console()
TopicArgument = Annotated[str, typer.Argument(help="Topic ID from roadmap, e.g. variables.")]


@contextmanager
def session() -> Iterator[LearningAgent]:
    try:
        yield LearningAgent(Settings.from_environment())
    except (ValueError, OSError, sqlite3.Error, yaml.YAMLError, json.JSONDecodeError) as error:
        console.print(f"Error: {error}", style="red", markup=False)
        raise typer.Exit(1) from None


@app.command()
def learn(topic: TopicArgument) -> None:
    """Show a complete local lesson and mark it started (not completed)."""
    with session() as agent:
        content = agent.content(topic)
        selected = agent.curriculum.get(topic)
        missing = set(selected.prerequisites) - agent.progress.completed()
        if missing:
            console.print(f"Recommended prerequisites: {', '.join(sorted(missing))}")
        agent.progress.mark(selected.id)
        console.print(Markdown(content))
        console.print(f"\nPractice: python -m python_learning_agent practice {selected.id}")


@app.command()
def explain(topic: TopicArgument) -> None:
    """Read a local explanation without changing learning progress."""
    with session() as agent:
        console.print(Markdown(agent.content(topic)))


@app.command()
def explore(topic: TopicArgument) -> None:
    """Explore available offline content; planned lessons report their status."""
    explain(topic)


@app.command()
def practice(topic: TopicArgument, solutions: bool = False) -> None:
    """Display practice or explained solutions; never execute learner code."""
    with session() as agent:
        filename = "solutions.py" if solutions else "exercises.py"
        console.print(agent.content(topic, filename), markup=False, highlight=False)
        console.print("Run only your reviewed local code. This application provides no sandbox.")


@app.command()
def quiz(topic: TopicArgument) -> None:
    """Take the demonstration quiz and persist an explained score."""
    with session() as agent:
        questions = agent.quiz(topic)
        correct = 0
        for question in questions:
            console.print(question["prompt"], markup=False)
            for label, value in question["options"].items():
                console.print(f"  {label}: {value}", markup=False)
            while True:
                answer = typer.prompt("Answer").strip().lower()
                if answer in question["options"]:
                    break
                console.print("Choose one of the displayed answer labels.")
            success = answer == question["answer"]
            correct += int(success)
            console.print("Correct." if success else f"Correct answer: {question['answer']}")
            console.print(question["explanation"], markup=False)
        score = 100 * correct / len(questions)
        agent.progress.record_quiz(topic, score)
        console.print(f"Score: {score:.0f}% ({correct}/{len(questions)})")
        topic_id = agent.curriculum.get(topic).id
        console.print(f"Completion is explicit: use progress --complete {topic_id} when ready.")


@app.command()
def progress(
    complete: Annotated[str | None, typer.Option(help="Mark a lesson completed.")] = None,
    difficult: Annotated[str | None, typer.Option(help="Flag a lesson for revision.")] = None,
) -> None:
    """Show persisted learning status, or explicitly update a lesson."""
    with session() as agent:
        tracker = agent.progress
        if complete is not None and difficult is not None:
            raise ValueError("Use --complete or --difficult separately.")
        if complete is not None:
            tracker.mark(complete, complete=True)
        if difficult is not None:
            tracker.mark(difficult, difficult=True)
        rows = tracker.records()
        if not rows:
            console.print("No progress yet. Start with: learn variables")
            return
        table = Table("Topic", "Status", "Best quiz", "Difficult", "Revise", "Last study (UTC)")
        for row in rows:
            table.add_row(
                row["topic_id"],
                row["status"],
                "-" if row["best_score"] is None else f"{row['best_score']:.0f}%",
                "yes" if row["difficult"] else "no",
                "yes" if row["revision_required"] else "no",
                row["last_study"],
            )
        console.print(table)


@app.command("next-topic")
def next_topic() -> None:
    """Recommend prerequisite-ready content without repeating completed lessons."""
    with session() as agent:
        topic, reason = agent.progress.next_topic()
        console.print(f"{reason}: {topic.id} - {topic.title}" if topic else reason)


@app.command()
def revise(topic: Annotated[str | None, typer.Argument()] = None) -> None:
    """Read a revision lesson, or list lessons flagged by difficulty or low quiz scores."""
    with session() as agent:
        if topic is not None:
            console.print(Markdown(agent.content(topic)))
            console.print("When confident, clear the revision flag with progress --complete TOPIC.")
            return
        rows = [row for row in agent.progress.records() if row["revision_required"]]
        console.print(
            "\n".join(row["topic_id"] for row in rows)
            if rows
            else "No revision currently required."
        )


@app.command()
def roadmap() -> None:
    """Show all six tracks, prerequisites, lesson availability, and planned capstones."""
    with session() as agent:
        table = Table("Topic ID", "Track", "Prerequisites", "Content")
        for topic in agent.curriculum.ordered():
            table.add_row(
                topic.id,
                topic.level,
                ", ".join(topic.prerequisites) or "none",
                "available" if topic.lesson else "planned",
            )
        console.print(table)
        capstones = {topic.level: topic.capstone for topic in agent.curriculum.ordered()}
        for level, capstone in capstones.items():
            console.print(f"{level} capstone (planned): {capstone}")
