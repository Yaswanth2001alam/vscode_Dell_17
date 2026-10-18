# Formula Cheatsheet

Introductory formulas used in the first lesson. Later modules will expand this reference with derivations, assumptions, and worked examples.

## Empirical accuracy

\[
\text{accuracy} = \frac{\text{number of correct predictions}}{\text{number of evaluated examples}}
\]

Accuracy is meaningful only relative to a representative evaluation set and can mislead when classes are imbalanced or error costs differ.

## One-dimensional nearest-centroid prediction

For class \(c\), with training values \(x_i\):

\[
\mu_c = \frac{1}{n_c}\sum_{i:y_i=c}x_i,\qquad
\hat{y}(x) = \underset{c}{\operatorname{argmin}}\;|x-\mu_c|
\]

Here \(n_c\) is the number of training observations in class \(c\), \(y_i\) is an observation's class, \(\mu_c\) is that class's mean, and \(x\) is a new observation. This simple rule works for the scalar example in the introductory lesson; it is not a universal model or a guarantee of a good decision boundary.

## Decision threshold

For a binary classifier that estimates probability \(p=P(y=1\mid x)\), a threshold \(t\) produces a positive prediction if \(p\geq t\). Changing \(t\) changes false-positive/false-negative tradeoffs; choose it using validation data and application costs, not test-set tuning.

