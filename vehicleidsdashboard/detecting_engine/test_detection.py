from detection.engine import DetectionEngine





def print_summary(summary):

    print("\n" + "=" * 65)
    print("DETECTION SUMMARY")
    print("=" * 65)

    print(f"Total Windows     : {summary['total_windows']}")
    print(f"Correct           : {summary['correct']}")
    print(f"Wrong             : {summary['wrong']}")
    print(f"Accuracy          : {summary['accuracy']:.2f}%")
    print(f"Macro Precision  : {summary['macro_precision']:.2f}%")
    print(f"Macro Recall     : {summary['macro_recall']:.2f}%")
    print(f"Macro F1-Score   : {summary['macro_f1_score']:.2f}%")
    print(f"Batch Latency     : {summary['batch_latency_ms']:.2f} ms")
    print(f"Average Latency   : {summary['average_latency_ms']:.2f} ms")
    print("\nGround Truth Distribution")
    print("-" * 65)

    for label, count in summary["ground_truth_distribution"].items():

        print(f"{label:<18}: {count}")

    print("\nPrediction Distribution")
    print("-" * 65)

    for label, count in summary["prediction_distribution"].items():

        print(f"{label:<18}: {count}")

    print("\nConfusion Matrix")
    print("-" * 65)

    matrix = summary["confusion_matrix"]

    labels = list(matrix.keys())

    # Header
    print(f"{'GT\\Pred':<10}", end="")

    for label in labels:

        print(f"{label:^8}", end="")

    print()

    print("-" * (10 + 8 * len(labels)))

    # Rows
    for gt in labels:

        print(f"{gt:<10}", end="")

        for pred in labels:

            print(f"{matrix[gt][pred]:^8}", end="")

        print()

    print("\nPrecision")
    print("-" * 65)

    for label, value in summary["precision"].items():

        print(f"{label:<10}: {value:>6.2f}%")

    print("\nRecall")
    print("-" * 65)

    for label, value in summary["recall"].items():

        print(f"{label:<10}: {value:>6.2f}%")

    print("\nF1-Score")
    print("-" * 65)

    for label, value in summary["f1_score"].items():

        print(f"{label:<10}: {value:>6.2f}%")





def print_detection(result, index, total):

    print("\n" + "=" * 65)
    print(f"DETECTION {index}/{total}")
    print("=" * 65)

    print(f"Packet Number     : {result['packet_number']}")
    print(f"Selected Label    : {result['selected_label']}")
    print(f"Window Label      : {result['window_label']}")
    print(f"Prediction        : {result['prediction']}")
    print(f"Confidence        : {result['confidence']:.2f}%")

    print(
        f"Evaluation        : "
        f"{'CORRECT' if result['is_correct'] else 'WRONG'}"
    )

    print(f"Timestamp         : {result['timestamp']}")
    print(f"Batch Latency     : {result['batch_latency_ms']:.2f} ms")
    print(f"Average Latency   : {result['average_latency_ms']:.2f} ms")

    print("\nClass Probabilities")
    print("-" * 65)

    for label, probability in result["probabilities"].items():

        print(f"{label:<18}: {probability:>6.2f}%")

engine = DetectionEngine()

engine.load_model("global_model.h5")

response = engine.run_detection()

summary = response["summary"]

results = response["results"]


for i, result in enumerate(results, start=1):

    print_detection(

        result,

        i,

        len(results)

    )

print_summary(summary)