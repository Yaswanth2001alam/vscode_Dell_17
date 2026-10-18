import importlib.util
import unittest
from pathlib import Path

MODULE_DIR = (
    Path(__file__).resolve().parents[1]
    / "07_Artificial_Intelligence_Fundamentals"
    / "examples"
)


def load_example(filename: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, MODULE_DIR / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load example module: {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


categories = load_example("ai_categories.py", "ai_categories")
classifier = load_example("tiny_classifier.py", "tiny_classifier")


class AICategoriesTests(unittest.TestCase):
    def test_threshold_rule_boundary(self):
        self.assertFalse(categories.needs_review(74.9, threshold=75.0))
        self.assertTrue(categories.needs_review(75.0, threshold=75.0))

    def test_threshold_must_be_non_negative(self):
        with self.assertRaisesRegex(ValueError, "non-negative"):
            categories.needs_review(10.0, threshold=-1.0)

    def test_centroid_fit_and_prediction(self):
        centroids = categories.fit_centroids([(10.0, "normal"), (90.0, "review")])
        self.assertEqual(centroids, {"normal": 10.0, "review": 90.0})
        self.assertEqual(categories.predict(70.0, centroids), "review")

    def test_empty_training_examples_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "at least one"):
            categories.fit_centroids([])

    def test_empty_centroids_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "must not be empty"):
            categories.predict(5.0, {})


class TinyClassifierTests(unittest.TestCase):
    def test_fit_predict_and_accuracy(self):
        training = [(10.0, 0), (12.0, 0), (80.0, 1), (90.0, 1)]
        centroids = classifier.fit_centroids(training)
        self.assertEqual(centroids, {0: 11.0, 1: 85.0})
        self.assertEqual(classifier.predict(70.0, centroids), 1)
        self.assertEqual(classifier.accuracy([(11.0, 0), (85.0, 1)], centroids), 1.0)

    def test_empty_training_or_evaluation_data_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "training data"):
            classifier.fit_centroids([])
        with self.assertRaisesRegex(ValueError, "evaluation data"):
            classifier.accuracy([], {0: 1.0})

    def test_prediction_without_fitted_model_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "without fitted"):
            classifier.predict(1.0, {})


if __name__ == "__main__":
    unittest.main()
