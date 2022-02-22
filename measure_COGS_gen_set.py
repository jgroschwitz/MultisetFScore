from multiset_fscore import MultisetFScoreTracker

if __name__ == "__main__":
    metrics_by_category = dict()
    metric = MultisetFScoreTracker()
    with open("out.gen.pred") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) == 4:
                category = parts[2]
                gold_sequence = parts[1].strip().split(" ")
                predicted_sequence = parts[3].strip().split(" ")
                if category not in metrics_by_category:
                    metrics_by_category[category] = MultisetFScoreTracker()
                metrics_by_category[category].process_instance(gold_sequence, predicted_sequence)
                metric.process_instance(gold_sequence, predicted_sequence)
            else:
                print(parts)
    r, p, f = metric.get_recall_precision_f()
    print(f"\nTotal:  R: {r:.2f}   P: {p:.2f}   F: {f:.2f}")

    for category in metrics_by_category.keys():
        r, p, f = metrics_by_category[category].get_recall_precision_f()
        print(f"\n{category}:  R: {r:.2f}   P: {p:.2f}   F: {f:.2f}")
        print(f"Wrongly predicted labels: {metrics_by_category[category].wrong_predicted_labels}")
        print(f"Missed labels: {metrics_by_category[category].missed_gold_labels}")
