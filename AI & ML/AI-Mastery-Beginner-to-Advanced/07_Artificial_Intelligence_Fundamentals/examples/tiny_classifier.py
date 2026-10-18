"""Train and evaluate a tiny nearest-centroid classifier without dependencies."""

from collections import defaultdict
from collections.abc import Sequence

Example = tuple[float, int]


def fit_centroids(examples: Sequence[Example]) -> dict[int, float]:
    """Return the mean feature value for each class label."""
    if not examples:
        raise ValueError("training data must contain at least one example")

    sums: dict[int, float] = defaultdict(float)
    counts: dict[int, int] = defaultdict(int)
    for value, label in examples:
        sums[label] += value
        counts[label] += 1

    return {label: sums[label] / counts[label] for label in sums}


def predict(value: float, centroids: dict[int, float]) -> int:
    """Predict the label with the nearest class centroid."""
    if not centroids:
        raise ValueError("cannot predict without fitted centroids")
    return min(centroids, key=lambda label: abs(value - centroids[label]))


def accuracy(examples: Sequence[Example], centroids: dict[int, float]) -> float:
    """Compute the fraction of examples whose predicted labels match."""
    if not examples:
        raise ValueError("evaluation data must contain at least one example")
    correct = sum(predict(value, centroids) == label for value, label in examples)
    return correct / len(examples)


def main() -> None:
    training: list[Example] = [(10.0, 0), (12.0, 0), (80.0, 1), (90.0, 1)]
    evaluation: list[Example] = [(11.0, 0), (85.0, 1)]
    centroids = fit_centroids(training)

    print(f"centroids: {centroids}")
    for value, expected in evaluation:
        print(f"value={value:.1f}, predicted={predict(value, centroids)}, expected={expected}")
    print(f"evaluation accuracy: {accuracy(evaluation, centroids):.0%}")
    print("Two toy evaluation examples do not establish real-world performance.")


if __name__ == "__main__":
    main()
