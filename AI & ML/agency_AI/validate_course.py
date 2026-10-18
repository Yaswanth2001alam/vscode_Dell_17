"""Validate this course, optionally executing every script and notebook offline."""

import argparse
import ast
import asyncio
import importlib.metadata
import json
import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

import nbformat
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "course_manifest.json"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def local_path(value):
    return ROOT.joinpath(*PurePosixPath(value).parts)


def check_links(source, origin):
    for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", source):
        if target.startswith(("https://", "http://", "#")):
            continue
        require(local_path(target).is_file(), f"Broken local link in {origin}: {target}")


def normalized_ast(source):
    source = source.replace("await main()", "asyncio.run(main())")
    return ast.dump(ast.parse(source), include_attributes=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true",
                        help="Run all scripts and fresh notebook kernels; persist successful notebook outputs.")
    arguments = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    lessons = manifest["lessons"]
    require([item["number"] for item in lessons] == list(range(1, 56)), "Expected 55 ordered lessons.")
    require(sum(item["examples"] for item in lessons) == manifest["worked_examples"] == 70,
            "Worked-example counts do not match.")

    required = {
        "Artificial intelligence", "AI vs ML vs deep learning vs generative AI", "Narrow AI", "General AI",
        "Models", "Training", "Inference", "Datasets", "Features", "Labels", "Parameters", "Predictions",
        "Classification vs regression", "Supervised learning", "Unsupervised learning", "Reinforcement learning",
        "Train data", "Validation data", "Test data", "Overfitting", "Underfitting", "Accuracy", "Precision",
        "Recall", "F1", "Bias", "Variance", "Variables", "Strings", "Lists", "Tuples", "Sets", "Dictionaries",
        "Conditions", "Loops", "Functions", "lambda", "Classes", "OOP", "Exceptions", "File handling", "JSON",
        "REST APIs", "HTTP", "Async programming", "Virtual environments", "pip", "NumPy", "Pandas",
        "Matplotlib", "Jupyter", "Pydantic", "FastAPI", "LLM", "Tokens", "Tokenization", "Context window",
        "System prompt", "User prompt", "Temperature", "Top-P", "Structured output", "JSON output",
        "Function calling", "Tool calling", "Hallucination", "Reasoning", "Model inference",
        "Linear regression", "Logistic regression", "Decision trees", "Random forests", "Gradient boosting",
        "K-nearest neighbors", "Support vector machines", "K-means", "DBSCAN", "PCA", "Isolation Forest",
        "Naive Bayes", "Text preprocessing", "Normalization", "Subword tokenization", "Stemming",
        "Lemmatization", "Bag-of-words", "TF-IDF", "Embeddings", "Semantic similarity",
        "Named entity recognition", "Text classification", "Sentiment analysis", "Sequence-to-sequence",
        "Attention", "Transformers", "Positional information", "Self-attention", "Multi-head attention",
        "Transformer blocks", "Pretraining", "Next-token prediction", "Autoregressive generation",
        "Quantization", "Inference optimization", "Open-weight models", "Hosted models",
        "Model limitations", "Knowledge boundaries", "Transfer learning", "Neural networks",
        "Latest advancements",
    }
    covered = {concept for item in lessons for concept in item["concepts"]}
    require(not (required - covered), f"Missing requested topics: {sorted(required - covered)}")

    generated_paths = [ROOT / "00_START_HERE.ipynb", MANIFEST, ROOT / "README.md",
                       ROOT / "requirements.txt", ROOT / "requirements-tested.txt", Path(__file__).resolve()]
    generated_paths.extend(local_path(path) for path in manifest["images"])
    for item in lessons:
        generated_paths.extend([local_path(item["notebook"]), local_path(item["script"])])
    for path in generated_paths:
        require(path.is_file(), f"Missing course file: {path.name}")
        require(path.stat().st_size < manifest["file_limit_bytes"], f"File exceeds size limit: {path.name}")

    check_links((ROOT / "README.md").read_text(encoding="utf-8"), "README")
    index = nbformat.read(ROOT / "00_START_HERE.ipynb", as_version=4)
    nbformat.validate(index)
    for cell in index.cells:
        check_links(cell.source, "course index")
    for item in lessons:
        notebook = nbformat.read(local_path(item["notebook"]), as_version=4)
        nbformat.validate(notebook)
        require(len({cell.id for cell in notebook.cells}) == len(notebook.cells),
                f"Duplicate cell IDs in lesson {item['number']}")
        require(all(cell.source.strip() for cell in notebook.cells), f"Empty cell in lesson {item['number']}")
        for cell in notebook.cells:
            if cell.cell_type == "markdown":
                check_links(cell.source, item["notebook"])
        examples = [cell for cell in notebook.cells if cell.cell_type == "code"]
        require(len(examples) == item["examples"] == len(item["expected_stdout"]),
                f"Example count mismatch in lesson {item['number']}")
        script_tree = ast.parse(local_path(item["script"]).read_text(encoding="utf-8"))
        guards = [node for node in script_tree.body if isinstance(node, ast.If)]
        require(len(guards) == len(examples), f"Script main-guard count mismatch in lesson {item['number']}")
        for guard, cell in zip(guards, examples, strict=True):
            require(ast.unparse(guard.test) == "__name__ == '__main__'", "Unexpected script execution guard.")
            original = ast.Module(body=guard.body, type_ignores=[])
            require(ast.dump(original, include_attributes=False) == normalized_ast(cell.source),
                    f"Notebook/script code differs in lesson {item['number']}")
            require(any(isinstance(node, ast.Assert) for node in ast.walk(original)),
                    f"No executable behavior check in lesson {item['number']}")
    print("Structural validation passed: requested topics, 55 notebook/script pairs, 70 examples, links, schemas, sizes.",
          flush=True)
    if not arguments.execute:
        return

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    environment = os.environ.copy()
    environment.update(OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MPLBACKEND="Agg",
                       PYTHONIOENCODING="utf-8")
    same_environment = sys.version.split()[0] == manifest["tested_python"] and all(
        importlib.metadata.version(name) == version for name, version in manifest["dependencies"].items()
    )
    if not same_environment:
        print("Dependency versions differ from the recorded environment; checking assertions and script/notebook parity, "
              "not exact historical numeric output.", flush=True)
    total = 0
    for item in lessons:
        print(f"[{item['number']:02d}/55] Running script and fresh notebook: {item['title']}", flush=True)
        result = subprocess.run([sys.executable, str(local_path(item["script"]))],
                                cwd=ROOT, env=environment, capture_output=True, text=True,
                                encoding="utf-8", timeout=150, check=False)
        if result.returncode != 0:
            raise RuntimeError(f"Script failed: {item['script']}\n{result.stdout}\n{result.stderr}")
        if result.stderr.strip():
            print(f"Script diagnostic ({item['number']:02d}): {result.stderr.strip()}", file=sys.stderr, flush=True)
        if same_environment:
            require(result.stdout == "".join(item["expected_stdout"]),
                    f"Script output differs from recorded results in lesson {item['number']}:\n{result.stdout}")
        path = local_path(item["notebook"])
        notebook = nbformat.read(path, as_version=4)
        NotebookClient(notebook, timeout=150, kernel_name="python3", allow_errors=False,
                       record_timing=False, resources={"metadata": {"path": str(ROOT)}}).execute(
                           env=environment)
        code_cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
        output = ""
        for cell in code_cells:
            require(cell.execution_count is not None, f"Unexecuted cell in lesson {item['number']}")
            require(not any(part.output_type == "error" for part in cell.outputs),
                    f"Error output in lesson {item['number']}")
            output += "".join(part.text for part in cell.outputs
                              if part.output_type == "stream" and part.name == "stdout")
            for part in cell.outputs:
                if part.output_type == "stream" and part.name == "stderr" and part.text.strip():
                    print(f"Notebook diagnostic ({item['number']:02d}): {part.text.strip()}",
                          file=sys.stderr, flush=True)
        require(output == result.stdout, f"Fresh notebook/script output mismatch in lesson {item['number']}")
        notebook.metadata.ai_course["execution_verified"] = True
        notebook.metadata.ai_course["execution_python"] = sys.version.split()[0]
        nbformat.validate(notebook)
        nbformat.write(notebook, path)
        require(path.stat().st_size < manifest["file_limit_bytes"],
                f"Executed notebook exceeds size budget: {item['notebook']}")
        nbformat.validate(nbformat.read(path, as_version=4))
        total += len(code_cells)
    print(f"Execution passed: 55 standalone scripts and 55 fresh notebook kernels; {total} worked examples per format.",
          flush=True)


if __name__ == "__main__":
    main()
