# AI Fundamentals

> **Course status:** In progress  
> **This installment:** The AI landscape—what AI means, how the field evolved, how AI/ML/deep learning/generative AI relate, and narrow AI versus AGI.  
> **Next section in this file:** Models, algorithms, data, training, and inference.

## Section 1 — The AI landscape

### 1. What is Artificial Intelligence?

#### 1. Simple Explanation

**Artificial Intelligence (AI)** is the field of building computer systems that perform tasks we associate with intelligent behavior. Examples include recognizing patterns, understanding language, making predictions, planning steps, and generating text or images.

AI does not mean a computer thinks exactly like a person. It means the system produces useful behavior for a task. A spam filter can classify email without understanding the email as a human does.

#### 2. Why Do We Need It?

People face more information and repeated decisions than they can handle manually. AI can help sort large volumes of data, find patterns, make predictions, and assist with routine work. It is most useful when paired with clear goals, reliable data, and human judgment for consequential decisions.

#### 3. How Does It Work?

There is no single mechanism called “AI.” A system might use hand-written rules, a statistical model learned from examples, a neural network, or a combination of these.

At a high level:

```text
Task and input
      ↓
Rules, learned model, or both
      ↓
Prediction, recommendation, generated content, or action
      ↓
Check the result against the goal and safety limits
```

For example, a simple network alert tool might apply a rule: “If an interface is down, raise an alert.” A learned system might instead use many past telemetry measurements to estimate the likelihood of an incident. Both can be called AI approaches, but they work differently.

#### 4. Technical Explanation

AI is an umbrella field spanning systems that perceive, reason, learn, communicate, plan, or act. A **task** is the specific problem the system is built to address. A **model** is a representation or mechanism that maps inputs to outputs. Some models contain behavior explicitly programmed by a developer; others have parameters adjusted from data during training.

The word “intelligence” can be misleading: system performance is task- and context-dependent. A model may be excellent at one narrow task and unreliable at a seemingly related one. Performance on a benchmark also does not prove broad understanding or safe behavior in production.

#### 5. Architecture / Flow

```text
Define a bounded task
       ↓
Provide input data
       ↓
Apply rules and/or a model
       ↓
Produce an output
       ↓
Evaluate correctness, usefulness, and risk
```

#### 6. Simple Example

A rule-based thermostat checks the measured temperature and turns heating on or off according to thresholds. It performs a task that can look intelligent, but it does not learn unless a learning mechanism is added.

#### 7. Network Engineering Example

A monitoring script can flag a supplied interface record whose status is `down`. That is useful automation, but it does not by itself determine why the interface went down. A later AI-assisted workflow could summarize related logs and suggest possible causes, while showing evidence and leaving operational decisions to an engineer.

#### 8. Python Example

This tiny example is a **rule**, not a machine-learning model:

```python
def explain_interface(status: str) -> str:
    if status.lower() == "down":
        return "The interface is down; inspect approved read-only evidence."
    return "The interface is not reported as down."


print(explain_interface("DOWN"))
```

Line by line:

- `def explain_interface(status: str) -> str:` defines a function that accepts text and returns text. The `str` annotations are type hints: they describe intended types but do not enforce them at runtime.
- `status.lower()` normalizes letter case so `"DOWN"` and `"down"` follow the same branch.
- `if ...` applies a condition written by the programmer. It does not learn from examples.
- `return` sends back the selected message.
- `print(...)` displays the result for this one test input.

The example intentionally makes no connection to a device and changes nothing.

#### 9. Real-World Usage

AI appears in recommendation systems, fraud detection, speech recognition, image inspection, search, forecasting, code assistance, and language interfaces. Production systems often combine ordinary software, databases, rules, and one or more AI models.

#### 10. Common Mistakes

- Treating every automated script as machine learning.
- Assuming an AI system understands the world as a person does.
- Assuming a fluent answer is necessarily correct.
- Assuming a model that works on one task will work on a nearby task.
- Treating a model’s output as evidence without checking its source or reliability.

#### 11. Key Takeaways

- AI is a broad field, not one algorithm or product.
- AI systems can use programmed rules, learned patterns, or both.
- Always define the task and assess the output for that task.
- AI output should be checked, especially when actions could affect real networks.

#### 12. Interview Questions

- **Beginner:** What does AI mean? Give one example that does not learn from data.
- **Intermediate:** Why is a rule-based alert system different from a machine-learning model?
- **Advanced:** Why is high benchmark performance insufficient evidence that an AI system is safe for a production network?

#### 13. Practice Exercise

Write down one repetitive networking task. Specify its input, desired output, and what could go wrong if the output is incorrect. Decide whether a simple rule might solve it before proposing machine learning.

### 2. How AI evolved

#### 1. Simple Explanation

AI has developed through several broad approaches. Early systems often relied on rules people wrote down. Later systems increasingly learned patterns from data, and modern generative systems can produce new text, images, audio, and code based on patterns learned during training.

These approaches overlap; newer methods did not make every older method useless.

#### 2. Why Do We Need It?

Knowing the history helps explain why different methods exist. Rules are understandable when the logic is known. Machine learning can find patterns that are hard to write as rules. Deep learning can learn complex representations from large datasets. Generative AI can create flexible outputs, but it can also produce plausible-sounding errors.

#### 3. How Does It Work?

A simplified timeline:

1. **Symbolic and rule-based AI:** People encode symbols, facts, and logical rules.
2. **Statistical machine learning:** Systems estimate patterns from examples and statistics.
3. **Deep learning:** Multi-layer neural networks learn complex features, especially with more data and compute.
4. **Transformers and foundation models:** Attention-based architectures support training on broad datasets and adaptation to many language or multimodal tasks.
5. **Generative AI applications:** Models generate or transform content, often combined with retrieval, tools, and application-level controls.

This is a simplified learning map, not a claim that the field progressed in a single straight line.

#### 4. Technical Explanation

**Symbolic AI** represents knowledge explicitly as symbols and rules. **Statistical learning** fits model parameters to data to improve a defined objective. **Deep learning** uses neural networks with many processing layers to learn representations. A **foundation model** is a model trained broadly enough to be adapted to a range of downstream tasks; the term does not guarantee quality or general competence. **Generative AI** refers to systems that generate content, often by estimating what output is likely given the input and learned patterns.

Different methods have different assumptions and tradeoffs. For example, a deterministic rule can be easier to audit, while a learned model can generalize beyond explicitly enumerated cases but may be harder to explain.

#### 5. Architecture / Flow

```text
Explicit rules
     ↓ (use data to learn patterns)
Statistical models
     ↓ (learn layered representations)
Deep neural networks
     ↓ (broad pretraining and adaptation)
Foundation / generative model applications
```

#### 6. Simple Example

For sorting mail, a person could write rules based on exact words in a message. A statistical model could learn from examples labeled “spam” and “not spam.” A generative assistant could summarize a message or draft a response. These are different capabilities and are not interchangeable.

#### 7. Network Engineering Example

A fixed rule can detect a known syslog message ID. A machine-learning model may group previously unseen messages with similar patterns. A generative model can draft a plain-English incident summary from retrieved logs and runbooks. In all cases, an engineer should distinguish observed facts from model-generated interpretation.

#### 8. Python Example

No Python implementation is needed to understand this timeline. The earlier rule function illustrates the first approach; later sections will build data-driven examples using Python libraries.

#### 9. Real-World Usage

Real applications commonly combine these generations of techniques: deterministic input validation, statistical ranking, a neural model, retrieval from approved documents, and fixed policy checks around the result.

#### 10. Common Mistakes

- Thinking a new method makes rules or classical ML obsolete.
- Assuming “deep learning” and “generative AI” are synonyms.
- Assuming a foundation model has reliable knowledge of a particular organization’s current network.
- Describing a timeline as if each new idea completely replaced what came before.

#### 11. Key Takeaways

- AI history includes multiple approaches that remain useful.
- Machine learning learns patterns from examples; rules are explicitly specified.
- Deep learning is one family within machine learning.
- Generative AI is about producing content; it is not the whole of AI.

#### 12. Interview Questions

- **Beginner:** Name one difference between rule-based AI and machine learning.
- **Intermediate:** Why might a production AI application combine fixed rules with a learned model?
- **Advanced:** What does the term “foundation model” suggest, and what does it not guarantee?

#### 13. Practice Exercise

Take the repetitive task from the previous exercise. Sketch one rule-based approach and one data-driven approach. Write down what evidence each approach would need and one failure mode for each.

### 3. AI vs. Machine Learning vs. Deep Learning vs. Generative AI

#### 1. Simple Explanation

These terms describe related but different scopes:

- **Artificial Intelligence (AI):** The broad field of making computer systems perform intelligent-seeming tasks.
- **Machine Learning (ML):** A way to build some AI systems by learning patterns from data instead of specifying every decision as a rule.
- **Deep Learning (DL):** A family of ML methods that uses neural networks with multiple layers.
- **Generative AI (GenAI):** AI that generates new content, such as text, images, audio, or code. Many current generative systems use deep learning, but “generative” describes what the system does, not one single architecture.

#### 2. Why Do We Need It?

The distinctions help select tools and interpret claims. A classification model that labels an alarm is not necessarily generative AI. A text-generating model is not automatically a reliable predictor for every numerical task. Knowing the category gives a starting point for asking how it was built and evaluated.

#### 3. How Does It Work?

Think of nested categories, with one caveat: “generative” describes a capability that can cut across model families.

```text
Artificial Intelligence
├── Rule-based systems
└── Machine Learning
    ├── Traditional ML methods
    └── Deep Learning (multi-layer neural networks)
        └── Many modern generative AI systems
```

For instance, a decision tree can be machine learning without being deep learning. A deep neural network can classify images without generating them. A language model can generate text using deep learning.

#### 4. Technical Explanation

In supervised ML, a model is fitted using examples and a learning objective. Deep learning uses layered parameterized functions to transform inputs into useful representations and outputs. Generative models learn patterns that allow them to produce samples or sequences. A model’s category alone does not tell us its training data, objective, current knowledge, accuracy, or safety properties.

#### 5. Architecture / Flow

```text
AI: broad goal of intelligent behavior
  ├─ Explicit rules → output
  └─ ML: examples + learning procedure → fitted model → prediction
       └─ DL: multi-layer neural network → prediction or representation
            └─ GenAI: learned model → generated content
```

#### 6. Simple Example

- A rule says: “If a message contains this exact string, mark it.”
- An ML classifier learns from labeled messages to estimate whether a new message is spam.
- A deep-learning classifier uses a multi-layer neural network to classify messages.
- A generative model drafts a response to a message.

#### 7. Network Engineering Example

- **AI/rules:** Flag a supplied interface record if its status is `down`.
- **ML:** Estimate the likelihood that an alarm pattern indicates a link fault.
- **DL:** Learn richer patterns from sequences of telemetry, if sufficient suitable data is available.
- **GenAI:** Summarize retrieved syslogs and runbook steps in plain English, ideally with source references.

#### 8. Python Example

The following decision is deterministic and is not a learned model:

```python
def is_interface_down(status: str) -> bool:
    return status.strip().lower() == "down"
```

- `strip()` removes accidental whitespace around the value.
- `lower()` makes the comparison case-insensitive.
- `== "down"` checks a condition written by the programmer.
- The function returns `True` or `False`; it does not adjust itself based on examples.

Later, the machine-learning section will show how to fit a model from examples and compare it with rules like this.

#### 9. Real-World Usage

An enterprise assistant may use a generative model to explain a question, ML to rank relevant documents, a vector search system to retrieve them, and ordinary code to check permissions. Calling the entire system “an LLM” would hide important components and risks.

#### 10. Common Mistakes

- Using AI, ML, deep learning, and GenAI as if they mean the same thing.
- Assuming all ML uses neural networks.
- Assuming all deep-learning systems generate content.
- Assuming generated content is factual because it sounds confident.
- Choosing a model family before clearly defining the task and success criteria.

#### 11. Key Takeaways

- AI is the broadest term here.
- ML learns patterns from data; deep learning is a subset of ML.
- Generative AI describes content-generation capability, not a guarantee of correctness.
- A complete application can combine models with retrieval, rules, APIs, and human review.

#### 12. Interview Questions

- **Beginner:** Explain the relationship between AI and machine learning.
- **Intermediate:** Can a machine-learning system be non-generative? Give an example.
- **Advanced:** Why is “we use generative AI” not enough information to assess an application’s technical or operational risk?

#### 13. Practice Exercise

For each task—flag a down interface, predict an outage risk, classify a log category, summarize an RCA—identify whether a rule, traditional ML, deep learning, or generative AI is a plausible starting point. Explain why; more than one approach may be reasonable.

### 4. Narrow AI and Artificial General Intelligence

#### 1. Simple Explanation

**Narrow AI** is designed or used for a bounded set of tasks. A spam filter, translation system, or model that summarizes incident reports is narrow AI, even if it performs that task impressively.

**Artificial General Intelligence (AGI)** is a proposed kind of AI with broadly general capabilities across many different tasks, rather than performance limited to a narrower task range. There is no single universally agreed test for AGI, so claims about it require careful definitions.

#### 2. Why Do We Need It?

This distinction prevents us from assuming that skill in one area means general competence. It is especially important when deciding whether to let a system operate tools or influence real infrastructure.

#### 3. How Does It Work?

For narrow AI, developers define a task, provide inputs, and evaluate performance in that scope. A system may perform well within that scope while failing when the inputs or environment change.

AGI is a concept about breadth and adaptability, not a specific implementation recipe. This course focuses on engineering useful systems with measurable capabilities; it does not assume that current products meet a particular AGI definition.

#### 4. Technical Explanation

Task-specific evaluation measures behavior under a specified distribution of inputs and conditions. **Distribution shift** means that real inputs differ from the data or conditions used during development. Narrow systems may degrade under such shifts. Generality would require capabilities to transfer across diverse tasks and changing conditions, but what degree of transfer qualifies as AGI is debated.

#### 5. Architecture / Flow

```text
Bounded task → test within scope → monitor for changed conditions

AGI (concept) → broad, adaptable capability across many task domains
```

#### 6. Simple Example

A calculator is excellent at arithmetic but does not thereby know how to plan a trip or diagnose a network outage. High capability at one task does not imply general capability.

#### 7. Network Engineering Example

A model that summarizes BGP troubleshooting documents may still misinterpret a Juniper command output or propose an unsafe action. Test each vendor, task, and operating condition rather than treating success on one demonstration as universal competence.

#### 8. Python Example

No Python example is necessary: this distinction is about the scope of a system’s capabilities, not a particular code construct.

#### 9. Real-World Usage

Production design assumes bounded, testable capabilities. Applications constrain tool access, validate outputs, log actions, and include human approval when an operation can affect service.

#### 10. Common Mistakes

- Calling a capable chatbot “AGI” without stating a definition or test.
- Assuming strong performance on a demo will generalize to production.
- Giving a model broad tool permissions because it seems conversational or confident.
- Confusing a flexible interface with reliable general competence.

#### 11. Key Takeaways

- Narrow systems can be highly capable within a bounded scope.
- Generality is a separate claim and needs a clear definition.
- Evaluate the actual task, inputs, environment, and consequences.
- For network operations, default to read-only access and explicit human approval for changes.

#### 12. Interview Questions

- **Beginner:** What is narrow AI?
- **Intermediate:** Why does success on a single benchmark not prove general intelligence?
- **Advanced:** How would you design operational controls for a model whose performance may degrade under distribution shift?

#### 13. Practice Exercise

Choose a network-assistance task and write a one-sentence scope statement: what the system may do, what it must not do, and what conditions require a human engineer.

## Connecting the ideas

The vocabulary forms a useful first mental model:

```text
AI is the broad field.
├── Some systems use explicitly written rules.
└── Some use machine learning to learn patterns from data.
    └── Deep learning uses multi-layer neural networks.
        └── Many generative systems use deep learning to produce content.

Most deployed tools should be treated as bounded systems:
define the task → test the task → monitor the task → control its permissions.
```

The next section will define **algorithms, models, datasets, features, labels, parameters, weights, bias, training, and inference**, then connect those terms in a single prediction workflow.

## Section quiz

Answer these before checking the key.

1. Is a script that checks `status == "down"` necessarily machine learning? Why?
2. Which term is broader: deep learning or AI?
3. Can a deep-learning system classify an input without generating new content?
4. Why should a network engineer avoid assuming a model that summarizes BGP logs can safely diagnose every vendor and protocol?
5. Give one reason a production application might combine a learned model with ordinary rules.

### Quiz answers

1. No. It can be a fixed rule written by a programmer; it does not have to learn from examples.
2. AI is broader. Deep learning is one family of machine-learning methods within the broader AI landscape.
3. Yes. Deep learning is used for classification and other tasks as well as generation.
4. The task, vendor, input format, and operating conditions may differ; success in one scope does not prove reliability in another.
5. Rules can validate inputs or enforce permissions while a model handles pattern recognition or language tasks.

## What to request next

Continue in `01-AI-Fundamentals.md` with **Section 2 — Models, algorithms, datasets, features, labels, parameters, weights, bias, training, and inference**.
