# AI learning course

Start with [00_START_HERE.ipynb](00_START_HERE.ipynb).

This course contains **55 concept notebooks, 55 matching Python scripts,
70 worked examples, and 5 original diagrams**, progressing from Python
and AI foundations to classical ML, deep learning, transformers, LLM systems, and advanced applications.
Each example includes explanatory notes, execution steps, assertions, expected output, limitations,
and practice tasks. The research reading snapshot is dated **2026-10-17**, not a live release tracker.

## Setup on Windows

Run these commands from this folder. Python 3.13 was used for validation; Python 3.11+ is the intended
language baseline, subject to compatible wheels for the selected packages.

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m ipykernel install --user --name agency-ai --display-name "Agency AI"
.\.venv\Scripts\python.exe -m jupyter lab
```

Select the **Agency AI** kernel. Package installation requires internet and downloads from your
configured package index; running the lessons afterward needs no network. Use the official PyTorch
installation instructions if the wheel for your Python/OS is unavailable. GPU acceleration is not needed.

`requirements.txt` declares compatible ranges; `requirements-tested.txt` records tested direct
versions, not a complete transitive/hashes lock. The tested interpreter and versions are also in
`course_manifest.json`. Kernel and terminal interpreters must match.

## Run a notebook or a script

Open a topic notebook and run its worked code cells. Each example includes its own imports,
definitions, and synthetic/local input data. Async notebook cells use top-level `await`; the
corresponding Python script uses `asyncio.run` once.

```powershell
.\.venv\Scripts\python.exe ".\examples\13_Linear_Regression.py"
.\.venv\Scripts\python.exe ".\examples\28_Training_a_PyTorch_MLP.py"
```

Scripts have main guards, so importing one does not train a model. Paths with `AI & ML` must be quoted.
Close interactive figures when experimenting; the worked plotting exercise uses an in-memory image.

## Validate the materials

```powershell
.\.venv\Scripts\python.exe .\validate_course.py
.\.venv\Scripts\python.exe .\validate_course.py --execute
```

The default checks notebook schemas, local links, coverage, example parity, and the 256 KiB per-file
size limit. `--execute` additionally runs every script in a separate process and every notebook in
a fresh kernel, verifies expected output, and persists fresh notebook outputs only after successful
execution. It does not contact hosted models or download data. Execution can take several minutes.

## Study sequence

- **01-10:** AI/Python foundations, HTTP/async, environments, NumPy, Pandas, Matplotlib, math.
- **11-24:** supervised/unsupervised learning, leakage-safe evaluation, all requested classical algorithms.
- **25-31:** bandits, Q-learning, gradients, MLP/CNN training, sequences, transfer learning.
- **32-45:** NLP, attention, transformers, tokens, tiny language-model training, sampling, prompts,
  schemas/tools, retrieval, reliability, adaptation, and inference efficiency.
- **46-55:** generative/multimodal mechanisms, serving, operations, fairness/privacy, forecasting,
  bounded workflows, capstones, and recent research.

## Topic files

| # | Level | Notebook | Runnable script |
| --- | --- | --- | --- |
| 01 | Beginner | [What AI is: AI, ML, deep learning, and generative AI](01_AI_Foundations.ipynb) | [Python](examples/01_AI_Foundations.py) |
| 02 | Beginner | [Python variables, strings, and containers](02_Python_Variables_Strings_and_Containers.ipynb) | [Python](examples/02_Python_Variables_Strings_and_Containers.py) |
| 03 | Beginner | [Conditions, loops, functions, lambda, and OOP](03_Python_Control_Functions_and_OOP.ipynb) | [Python](examples/03_Python_Control_Functions_and_OOP.py) |
| 04 | Beginner | [Files, JSON, and explicit data boundaries](04_Files_JSON_and_Data_Validation.ipynb) | [Python](examples/04_Files_JSON_and_Data_Validation.py) |
| 05 | Beginner to intermediate | [HTTP, REST APIs, and async programming](05_HTTP_REST_and_Async.ipynb) | [Python](examples/05_HTTP_REST_and_Async.py) |
| 06 | Beginner | [Virtual environments, pip, and Jupyter](06_Environments_Pip_and_Jupyter.ipynb) | [Python](examples/06_Environments_Pip_and_Jupyter.py) |
| 07 | Beginner | [NumPy arrays, shapes, broadcasting, and vectorization](07_NumPy_Arrays_and_Vectorization.ipynb) | [Python](examples/07_NumPy_Arrays_and_Vectorization.py) |
| 08 | Beginner | [Pandas tables and exploratory data analysis](08_Pandas_DataFrames_and_EDA.ipynb) | [Python](examples/08_Pandas_DataFrames_and_EDA.py) |
| 09 | Beginner | [Matplotlib and visual reasoning](09_Matplotlib_and_Visual_Reasoning.ipynb) | [Python](examples/09_Matplotlib_and_Visual_Reasoning.py) |
| 10 | Beginner to intermediate | [Vectors, probability, losses, and optimization](10_Math_Probability_and_Optimization.ipynb) | [Python](examples/10_Math_Probability_and_Optimization.py) |
| 11 | Beginner to intermediate | [Datasets, supervision, and train/validation/test splits](11_Datasets_Supervision_and_Data_Splits.ipynb) | [Python](examples/11_Datasets_Supervision_and_Data_Splits.py) |
| 12 | Intermediate | [Preprocessing and leakage-safe pipelines](12_Preprocessing_and_Leakage_Safe_Pipelines.ipynb) | [Python](examples/12_Preprocessing_and_Leakage_Safe_Pipelines.py) |
| 13 | Intermediate | [Linear regression and numerical prediction](13_Linear_Regression.ipynb) | [Python](examples/13_Linear_Regression.py) |
| 14 | Intermediate | [Logistic regression and classification probabilities](14_Logistic_Regression.ipynb) | [Python](examples/14_Logistic_Regression.py) |
| 15 | Intermediate | [Decision trees and rule-like decisions](15_Decision_Trees.ipynb) | [Python](examples/15_Decision_Trees.py) |
| 16 | Intermediate | [Random forests and bagging](16_Random_Forests.ipynb) | [Python](examples/16_Random_Forests.py) |
| 17 | Intermediate | [Gradient boosting on tabular data](17_Gradient_Boosting.ipynb) | [Python](examples/17_Gradient_Boosting.py) |
| 18 | Intermediate | [K-nearest neighbors and support vector machines](18_KNN_and_Support_Vector_Machines.ipynb) | [Python](examples/18_KNN_and_Support_Vector_Machines.py) |
| 19 | Intermediate | [Naive Bayes and text classification](19_Naive_Bayes_and_Text_Classification.ipynb) | [Python](examples/19_Naive_Bayes_and_Text_Classification.py) |
| 20 | Intermediate | [Accuracy, precision, recall, F1, and calibration](20_Metrics_Thresholds_and_Calibration.ipynb) | [Python](examples/20_Metrics_Thresholds_and_Calibration.py) |
| 21 | Intermediate | [Bias, variance, overfitting, and model selection](21_Bias_Variance_Overfitting_and_Tuning.ipynb) | [Python](examples/21_Bias_Variance_Overfitting_and_Tuning.py) |
| 22 | Intermediate | [Unsupervised clustering: K-means and DBSCAN](22_KMeans_and_DBSCAN.ipynb) | [Python](examples/22_KMeans_and_DBSCAN.py) |
| 23 | Intermediate | [PCA and dimensionality reduction](23_PCA_and_Dimensionality_Reduction.ipynb) | [Python](examples/23_PCA_and_Dimensionality_Reduction.py) |
| 24 | Intermediate | [Isolation Forest and anomaly detection](24_Isolation_Forest_and_Anomaly_Detection.ipynb) | [Python](examples/24_Isolation_Forest_and_Anomaly_Detection.py) |
| 25 | Intermediate | [Reinforcement learning and exploration with bandits](25_Reinforcement_Learning_and_Bandits.ipynb) | [Python](examples/25_Reinforcement_Learning_and_Bandits.py) |
| 26 | Intermediate to advanced | [Q-learning, states, and discounted returns](26_Q_Learning_and_MDPs.ipynb) | [Python](examples/26_Q_Learning_and_MDPs.py) |
| 27 | Intermediate | [Neurons, backpropagation, and autograd](27_Neurons_Backpropagation_and_Autograd.ipynb) | [Python](examples/27_Neurons_Backpropagation_and_Autograd.py) |
| 28 | Intermediate | [Train a multilayer neural network with PyTorch](28_Training_a_PyTorch_MLP.ipynb) | [Python](examples/28_Training_a_PyTorch_MLP.py) |
| 29 | Intermediate | [Convolutional neural networks and image features](29_Convolutional_Neural_Networks.ipynb) | [Python](examples/29_Convolutional_Neural_Networks.py) |
| 30 | Intermediate | [RNNs, sequence modeling, and encoder-decoder ideas](30_RNNs_Sequences_and_Seq2Seq.ipynb) | [Python](examples/30_RNNs_Sequences_and_Seq2Seq.py) |
| 31 | Intermediate | [Transfer learning and frozen feature extractors](31_Transfer_Learning_and_Frozen_Features.ipynb) | [Python](examples/31_Transfer_Learning_and_Frozen_Features.py) |
| 32 | Intermediate | [NLP preprocessing, normalization, stemming, and lemmatization](32_NLP_Normalization_Stemming_and_Lemmas.ipynb) | [Python](examples/32_NLP_Normalization_Stemming_and_Lemmas.py) |
| 33 | Intermediate | [Bag-of-words, TF-IDF, and text classification](33_Bag_of_Words_TFIDF_and_Sentiment.ipynb) | [Python](examples/33_Bag_of_Words_TFIDF_and_Sentiment.py) |
| 34 | Intermediate | [Embeddings, semantic similarity, and named entities](34_Embeddings_Similarity_and_Named_Entities.ipynb) | [Python](examples/34_Embeddings_Similarity_and_Named_Entities.py) |
| 35 | Intermediate to advanced | [Attention, self-attention, and causal masking](35_Attention_and_Causal_Masking.ipynb) | [Python](examples/35_Attention_and_Causal_Masking.py) |
| 36 | Advanced | [Transformer blocks and positional information](36_Transformer_Blocks_and_Positions.ipynb) | [Python](examples/36_Transformer_Blocks_and_Positions.py) |
| 37 | Intermediate | [Tokens, subword tokenization, and context windows](37_Tokens_Subwords_and_Context_Windows.ipynb) | [Python](examples/37_Tokens_Subwords_and_Context_Windows.py) |
| 38 | Advanced | [Language models, pretraining, and next-token prediction](38_Language_Model_Pretraining_and_Next_Tokens.ipynb) | [Python](examples/38_Language_Model_Pretraining_and_Next_Tokens.py) |
| 39 | Intermediate to advanced | [Inference, temperature, top-p, and generation](39_Inference_Temperature_TopP_and_Generation.ipynb) | [Python](examples/39_Inference_Temperature_TopP_and_Generation.py) |
| 40 | Intermediate | [System/user prompts, context, and model boundaries](40_Prompts_Context_and_Model_Boundaries.ipynb) | [Python](examples/40_Prompts_Context_and_Model_Boundaries.py) |
| 41 | Intermediate | [Structured output, JSON, and safe tool calling](41_Structured_Output_and_Tool_Calling.ipynb) | [Python](examples/41_Structured_Output_and_Tool_Calling.py) |
| 42 | Intermediate to advanced | [Retrieval-augmented generation and evidence](42_Retrieval_Augmented_Generation.ipynb) | [Python](examples/42_Retrieval_Augmented_Generation.py) |
| 43 | Advanced | [Hallucinations, reasoning checks, and LLM evaluation](43_LLM_Evaluation_Hallucinations_and_Reliability.ipynb) | [Python](examples/43_LLM_Evaluation_Hallucinations_and_Reliability.py) |
| 44 | Advanced | [Fine-tuning, LoRA, distillation, and preference learning](44_FineTuning_LoRA_Distillation_and_Preferences.ipynb) | [Python](examples/44_FineTuning_LoRA_Distillation_and_Preferences.py) |
| 45 | Advanced | [Quantization, KV cache, and inference optimization](45_Quantization_KV_Cache_and_Inference_Cost.ipynb) | [Python](examples/45_Quantization_KV_Cache_and_Inference_Cost.py) |
| 46 | Advanced | [Generative models: autoencoders, GANs, and diffusion](46_Generative_Models_Autoencoders_and_Diffusion.ipynb) | [Python](examples/46_Generative_Models_Autoencoders_and_Diffusion.py) |
| 47 | Advanced | [Multimodal models and contrastive representations](47_Multimodal_Models_and_Contrastive_Learning.ipynb) | [Python](examples/47_Multimodal_Models_and_Contrastive_Learning.py) |
| 48 | Intermediate to advanced | [Pydantic, FastAPI, and a tested inference endpoint](48_Pydantic_FastAPI_and_Model_Serving.ipynb) | [Python](examples/48_Pydantic_FastAPI_and_Model_Serving.py) |
| 49 | Advanced | [MLOps, drift, reproducibility, and model artifacts](49_MLOps_Drift_and_Model_Artifacts.ipynb) | [Python](examples/49_MLOps_Drift_and_Model_Artifacts.py) |
| 50 | Intermediate to advanced | [Fairness, privacy, and responsible AI evaluation](50_Fairness_Privacy_and_Responsible_AI.ipynb) | [Python](examples/50_Fairness_Privacy_and_Responsible_AI.py) |
| 51 | Intermediate to advanced | [Time-series forecasting without future leakage](51_Time_Series_and_Forecasting.ipynb) | [Python](examples/51_Time_Series_and_Forecasting.py) |
| 52 | Advanced | [Agents, workflows, and bounded tool use](52_Agents_Workflows_and_Bounded_Tools.ipynb) | [Python](examples/52_Agents_Workflows_and_Bounded_Tools.py) |
| 53 | Advanced | [Capstone: a leakage-safe telemetry classifier](53_Capstone_Network_Telemetry_Classifier.ipynb) | [Python](examples/53_Capstone_Network_Telemetry_Classifier.py) |
| 54 | Advanced | [Capstone: an evidence assistant with regression tests](54_Capstone_Evidence_Assistant_and_Evals.ipynb) | [Python](examples/54_Capstone_Evidence_Assistant_and_Evals.py) |
| 55 | Advanced | [Recent advances and how to evaluate new AI claims](55_Recent_Advances_and_Reading_Research.ipynb) | [Python](examples/55_Recent_Advances_and_Reading_Research.py) |

## Safety and interpretation

Data is synthetic and offline. HTTP lessons use MockTransport or an in-process TestClient, not a
listening server. There are no API keys, external model/dataset downloads, real device commands, or
paid calls. Do not replace the synthetic data with confidential operational data without authorization.
Never load untrusted pickle/joblib artifacts.

Examples distinguish actual trained models from fixed-weight demonstrations, handcrafted embeddings,
regex entity rules, mock planner outputs, and extractive rather than LLM-generated answers. The local
tiny transformer is trained on a repeating pattern and is **not** a pretrained assistant. Assertions
verify stated behavior; they do not replace production validation, representative benchmarks,
authorization, or a reviewed deployment process.

The curriculum is intentionally broad, not an exhaustive encyclopedia of every AI topic. Primary
references are provided in each notebook. Mutable provider/library documentation may change; the
recent-advances lesson documents its date and uncertainty instead of asserting a permanent 'latest' winner.
