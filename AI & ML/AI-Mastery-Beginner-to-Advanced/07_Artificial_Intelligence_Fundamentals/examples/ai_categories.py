"""Small, deterministic demonstrations of rule-based and learned behavior."""

from collections import defaultdict
from collections.abc import Sequence

TrainingExample = tuple[float, str]


def needs_review(measurement: float, threshold: float = 75.0) -> bool:
    """Apply an explicit human-chosen threshold rule."""
    if threshold < 0:
        raise ValueError("threshold must be non-negative")
    return measurement >= threshold


def fit_centroids(examples: Sequence[TrainingExample]) -> dict[str, float]:
    """Learn one mean measurement per label from a non-empty example set."""
    if not examples:
        raise ValueError("at least one training example is required")

    totals: dict[str, float] = defaultdict(float)
    counts: dict[str, int] = defaultdict(int)
    for measurement, label in examples:
        if not label:
            raise ValueError("training labels must not be empty")
        totals[label] += measurement
        counts[label] += 1

    return {label: totals[label] / counts[label] for label in totals}


def predict(measurement: float, centroids: dict[str, float]) -> str:
    """Choose the label whose mean is closest to the new measurement."""
    if not centroids:
        raise ValueError("centroids must not be empty")
    return min(centroids, key=lambda label: abs(measurement - centroids[label]))


def main() -> None:
    examples: list[TrainingExample] = [
        (10.0, "normal"),
        (12.0, "normal"),
        (80.0, "review"),
        (90.0, "review"),
    ]
    centroids = fit_centroids(examples)
    measurement = 70.0

    print("Rule-based threshold demonstration")
    print(f"measurement={measurement:.1f}, review={needs_review(measurement)}")
    print("\nLearned nearest-centroid demonstration")
    print(f"centroids={centroids}")
    print(f"measurement={measurement:.1f}, predicted={predict(measurement, centroids)}")
    print("These toy examples are educational, not operational recommendations.")


if __name__ == "__main__":
    main()
