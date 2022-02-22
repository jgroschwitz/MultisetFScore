from collections import Counter


class MultisetFScoreTracker:

    def __init__(self):
        self.total_predicted = 0
        self.total_gold = 0
        self.total_correct = 0
        self.wrong_predicted_labels = Counter()
        self.missed_gold_labels = Counter()

    def process_instance(self, gold, predicted):
        """
        Updates the internal counters with the given gold and predicted label lists
        :param gold: list of gold labels (strings)
        :param predicted: list of predicted labels (strings)
        :return: nothing
        """
        prediction_counts = Counter(predicted)  # maps each label to how often it occurs in the prediction
        gold_counts = Counter(gold)  # maps each label to how often it occurs in the gold
        # update total counts (divisors in recall and precision)
        self.total_predicted += sum(prediction_counts.values())
        self.total_gold += sum(gold_counts.values())
        # update correct counts (dividend in recall and precision)
        for label in gold_counts.keys():
            # the number of correct predictions for each label is the "overlap" between gold and predicted sequence, which is the minimum of the two counts.
            self.total_correct += min(gold_counts.get(label, 0), prediction_counts.get(label, 0)) # we default the count to 0 if the label was not seen.
            if gold_counts.get(label, 0) > prediction_counts.get(label, 0):
                self.missed_gold_labels.update([label])
        for label in prediction_counts.keys():
            if gold_counts.get(label, 0) < prediction_counts.get(label, 0):
                self.wrong_predicted_labels.update([label])

    def get_recall_precision_f(self):
        """
        Gets recall, precision and f-score for the currently processed instances
        :return: recall, precision, f
        """
        if self.total_gold > 1e-12:
            recall = float(self.total_correct) / float(self.total_gold)
        else:
            recall = 0.0
        if self.total_predicted > 1e-12:
            precision = float(self.total_correct) / float(self.total_predicted)
        else:
            precision = 0.0
        if recall > 1e-12 or precision > 1e-12:
            f = 2 * recall * precision / (recall + precision)
        else:
            f = 0.0
        return recall, precision, f
