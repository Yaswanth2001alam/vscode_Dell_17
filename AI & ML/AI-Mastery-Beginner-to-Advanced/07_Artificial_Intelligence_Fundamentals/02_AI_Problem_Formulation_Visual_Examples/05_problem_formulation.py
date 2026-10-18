"""Reusable, read-only task formulation and candidate-action ranking demo."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Sequence


@dataclass(frozen=True)
class CandidateAction:
    """Descriptive candidate step; this class never executes an action."""

    name: str
    time_units: float
    risk: float
    information_value: float
    changes_state: bool = False

    def validate(self) -> None:
        if not self.name.strip():
            raise ValueError("candidate action must have a name")
        if not isfinite(self.time_units) or self.time_units < 0:
            raise ValueError("time_units must be finite and non-negative")
        if not isfinite(self.risk) or not 0 <= self.risk <= 1:
            raise ValueError("risk must be between 0 and 1")
        if not isfinite(self.information_value) or not 0 <= self.information_value <= 1:
            raise ValueError("information_value must be between 0 and 1")


@dataclass(frozen=True)
class TaskFormulation:
    """Goals, hard constraints, and soft-cost weights for a bounded task."""

    goal: str
    prohibited_actions: frozenset[str]
    time_weight: float = 1.0
    risk_weight: float = 10.0
    information_weight: float = 2.0

    def validate(self) -> None:
        if not self.goal.strip():
            raise ValueError("goal must not be empty")
        weights = (self.time_weight, self.risk_weight, self.information_weight)
        if any(not isfinite(weight) or weight < 0 for weight in weights):
            raise ValueError("cost weights must be finite and non-negative")

    def score(self, action: CandidateAction) -> float:
        """Compute J = alpha*time + beta*risk - gamma*information."""
        self.validate()
        action.validate()
        return (
            self.time_weight * action.time_units
            + self.risk_weight * action.risk
            - self.information_weight * action.information_value
        )

    def rank_candidates(
        self,
        actions: Sequence[CandidateAction],
        *,
        human_approved: bool = False,
    ) -> list[tuple[CandidateAction, float]]:
        """Rank permitted descriptions; no candidate is ever executed."""
        self.validate()
        ranked: list[tuple[CandidateAction, float]] = []
        for action in actions:
            action.validate()
            is_prohibited = (
                action.name in self.prohibited_actions or action.changes_state
            )
            if is_prohibited and not human_approved:
                continue
            ranked.append((action, self.score(action)))
        return sorted(ranked, key=lambda item: (item[1], item[0].name))


def build_network_example() -> tuple[TaskFormulation, list[CandidateAction]]:
    """Create an entirely synthetic network-troubleshooting scenario."""
    task = TaskFormulation(
        goal="Rank useful diagnostic evidence for an operator without changing devices.",
        prohibited_actions=frozenset({"reset_interface"}),
    )
    actions = [
        CandidateAction("collect_read_only_counters", 2.0, 0.0, 0.6),
        CandidateAction("inspect_routing_neighbor", 3.0, 0.0, 0.9),
        CandidateAction(
            "reset_interface",
            1.0,
            0.8,
            0.2,
            changes_state=True,
        ),
    ]
    return task, actions


def main() -> None:
    task, actions = build_network_example()
    ranked = task.rank_candidates(actions)
    print("Goal:", task.goal)
    print("Permitted candidate scores (lower is preferred):")
    for action, score in ranked:
        print(f"  {action.name}: J={score:.2f}")
    blocked = [
        action.name
        for action in actions
        if action.name in task.prohibited_actions or action.changes_state
    ]
    print("Blocked without separate human approval:", ", ".join(blocked))
    print("This program ranks descriptions only; it performs no network operations.")


if __name__ == "__main__":
    main()
