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
        :param gold: list of gold labels (i.e. a list of strings)
        :param predicted: list of predicted labels (i.e. a list of strings)
        :return: nothing
        """
        prediction_counts, gold_counts = MultisetFScoreTracker.__count_labels_in_sequences(predicted, gold)
        self.__update_total_predicted_and_gold_counts(prediction_counts, gold_counts)
        self.__update_total_correct_counts_and_count_label_mistakes(prediction_counts, gold_counts)

    def __update_total_predicted_and_gold_counts(self, prediction_counts, gold_counts):
        self.total_predicted += sum(prediction_counts.values())
        self.total_gold += sum(gold_counts.values())

    def __update_total_correct_counts_and_count_label_mistakes(self, prediction_counts, gold_counts):
        for label in gold_counts.keys():
            # the number of correct predictions for each label is the "overlap" between gold and predicted sequence,
            # which is the minimum of the two counts.
            # we default the count to 0 if the label was not seen.
            self.total_correct += min(gold_counts.get(label, 0), prediction_counts.get(label, 0))
            if gold_counts.get(label, 0) > prediction_counts.get(label, 0):
                self.missed_gold_labels.update([label])
        for label in prediction_counts.keys():
            if gold_counts.get(label, 0) < prediction_counts.get(label, 0):
                self.wrong_predicted_labels.update([label])

    @staticmethod
    def __count_labels_in_sequences(predicted, gold):
        """
        Returns two Counter objects (one for predict and one for gold). These Counter objects are dicts (with some extra
        methods) that map labels to counts.
        """
        return Counter(predicted), Counter(gold)  # the Counter class does the counting for us

    def get_recall_precision_f(self):
        """
        Returns recall, precision and f-score (as scores between 0 and 1) for the currently processed instances
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

    def get_wrong_predicted_labels(self):
        """
        Returns a Counter object that maps labels to the number of times they were predicted but not in the gold
        (or predicted too often in the multiset).
        :return:
        """
        return self.wrong_predicted_labels

    def get_missed_gold_labels(self):
        """
        Returns a Counter object that maps labels to the number of times they were in the gold but not predicted
        (or not predicted often enough in the multiset).
        :return:
        """
        return self.missed_gold_labels

    def print_most_common_errors(self, number_of_wrong_labels_to_print=10):
        MultisetFScoreTracker.__print_most_common_counts_formatted(self.wrong_predicted_labels,
                                                                   "wrongly predicted labels",
                                                                   number_of_wrong_labels_to_print)
        MultisetFScoreTracker.__print_most_common_counts_formatted(self.missed_gold_labels,
                                                                   "missed gold labels", number_of_wrong_labels_to_print)

    @staticmethod
    def __print_most_common_counts_formatted(counter, description, number_of_wrong_labels_to_print=10):
        """
        Prints the most common labels in counter.
        :param counter:
        :return:
        """
        print(f"Most common {description}:")
        for label, count in counter.most_common(number_of_wrong_labels_to_print):
            print(f"{label}: {count}")


def run_on_corpus(predicted_labels_corpus, gold_labels_corpus, number_of_wrong_labels_to_print=10):
    """
    Give this function two corpora (lists of lists of strings) of predicted and gold labels.
    Then this function will return the recall, precision and f-score for the label multisets, as well as print
    the most common wrongly predicted labels and missed gold labels.
    """
    tracker = MultisetFScoreTracker()
    for predicted, gold in zip(predicted_labels_corpus, gold_labels_corpus):
        tracker.process_instance(gold, predicted)
    recall, precision, f = tracker.get_recall_precision_f()
    print(f"Recall: {recall:.3f}, Precision: {precision:.3f}, F-score: {f:.3f}")
    tracker.print_most_common_errors(number_of_wrong_labels_to_print)


if __name__ == "__main__":
    # example usage
    predicted_labels_corpus = [["The", "cat", "is", "on", "the", "mat"], ["John", "loves", "Mary"],
                               ["John", "loves", "Mary"]]
    gold_labels_corpus = [["The", "cat", "sits", "on", "the", "desk"], ["John", "likes", "Mary"],
                          ["John", "hates", "pancakes"]]
    run_on_corpus(predicted_labels_corpus, gold_labels_corpus)
