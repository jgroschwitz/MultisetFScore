# MultisetFScore

The code in this repo allows computing multi-set f-scores on sequences of labels/tokens.

## What is multiset f-score?
For example:

Say the system predicts the sentence "a mouse and a cat chase the mouse", and the gold (reference) sentence is "the mouse and the cat chase a second mouse". Then the multisets of tokens in the sentence are the sets of tokens with their multiplicity. That is:

Prediction: {"a": 2, "mouse": 2, "and": 1, "cat": 1, "chase":1, "the":1}
Gold: {"a":1, "mouse": 2, "and": 1, "cat": 1, "chase": 1, "the":2, "second":1}

Of the 8 predicted labels, 7 are correct ("a" is correct only once), and of the 9 gold labels, 7 were predicted ("second" was left out, and "the" only predicted once). Both 7s are actually the same number of _correctly predicted tokens".

Then precision is 7/8=0.875 and recall is 7/9=0.77777..., yielding a multiset f-score of about 0.82.

When given a corpus of prediction/gold sequence pairs, the code computes the micro-average as usual (i.e. computing the total number of predicted labels, gold labels and correct labels across the corpus, and getting the f-score from there).

The input sequences can of course be other sequences than sentences, such as the list of all node labels in a graph.

## Usage

The most convenient use is the `run_on_corpus` in `multiset_fscore.py`, which takes as input two lists of token lists, e.g. as in the main function:

```
  predicted_labels_corpus = [["The", "cat", "is", "on", "the", "mat"], ["John", "loves", "Mary"], ["John", "loves", "Mary"]]
  gold_labels_corpus = [["The", "cat", "sits", "on", "the", "desk"], ["John", "likes", "Mary"], ["John", "hates", "pancakes"]]
  run_on_corpus(predicted_labels_corpus, gold_labels_corpus)
```

For more custom-tailored use, make a `MultisetFScore` object, feed each prediction/gold sequence pair into `process_instance` and in the end call `get_recall_precision_f` to get the results.


## Installation

You can install this package by running `pip install -e .` (don't forget the dot) in its main directory. You can then `import multiset_fscore` to access the code in `multiset_fscore.py`.
