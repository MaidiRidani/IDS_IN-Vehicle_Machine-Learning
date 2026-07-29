# ==========================================================
# MAIN
#
# Federated Continual Learning
#
# 8-Class Global Model
# ==========================================================

# ==========================================================
# IMPORT
# ==========================================================

import gc
import time
import numpy as np
import tensorflow as tf

from config import (
    NUM_CLIENTS,
    NUM_ROUNDS,
    MODE,
    RANDOM_SEED,
    INITIAL_GLOBAL_MODEL_PATH,
)

from dataset import (
    CLIENT_DATA,
    initialize_partitions,
    load_validation_data,
)

from client import client_update_fn

from server import (
    global_model,
    run_one_round,
    clear_validation_data,
)

from common import (
    init_experiment_note,
    init_training_history_file,
    append_training_history,
    write_experiment_config,
    write_model_info,
    write_client_partition,
    write_training_time,
    save_initial_global_model,
    save_final_model,
    save_best_model,
)

# ==========================================================
# RANDOM SEED
# ==========================================================

np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)

# ==========================================================
# INITIALIZE CLIENT PARTITIONS
# ==========================================================

initialize_partitions(

    num_clients=NUM_CLIENTS,

    mode=MODE,

)

# ==========================================================
# MODEL INFO
# ==========================================================

print()

print("=" * 70)
print("GLOBAL MODEL")
print("=" * 70)

global_model.summary()

total_params = global_model.count_params()

trainable_params = sum(

    tf.keras.backend.count_params(w)

    for w in global_model.trainable_weights

)

non_trainable_params = sum(

    tf.keras.backend.count_params(w)

    for w in global_model.non_trainable_weights

)

print()

print(f"Total Parameters        : {total_params:,}")

print(f"Trainable Parameters    : {trainable_params:,}")

print(f"Non-trainable Parameters: {non_trainable_params:,}")

# ==========================================================
# INIT LOG FILE
# ==========================================================

history_file = init_training_history_file(

    filename="training_history.csv"

)

note_path = init_experiment_note()

# ==========================================================
# WRITE EXPERIMENT INFO
# ==========================================================

write_experiment_config(

    note_path

)

write_model_info(

    note_path,

    global_model,

)

write_client_partition(

    note_path,

    CLIENT_DATA,

)

# ==========================================================
# SAVE INITIAL MODEL
# ==========================================================

save_initial_global_model(

)

# ==========================================================
# BEST MODEL
# ==========================================================

best_weights = None

best_accuracy = -1.0

best_round = -1

# ==========================================================
# START TIMER
# ==========================================================

start_time = time.time()

# ==========================================================
# TRAINING INFO
# ==========================================================

print()

print("=" * 70)
print("FEDERATED CONTINUAL LEARNING")
print("=" * 70)

print(f"Clients             : {NUM_CLIENTS}")

print(f"Communication Round : {NUM_ROUNDS}")

print(f"Initial Model       : {INITIAL_GLOBAL_MODEL_PATH}")

print()

# ==========================================================
# BASELINE VALIDATION
# ==========================================================

print("=" * 70)
print("ROUND 0 (BASELINE)")
print("=" * 70)

x_val, y_val = load_validation_data()

initial_loss, initial_acc = global_model.evaluate(

    x_val,

    y_val,

    verbose=1,

)

print()

print(f"Validation Loss     : {initial_loss:.6f}")

print(f"Validation Accuracy : {initial_acc:.4f}")

append_training_history(

    history_file,

    0,

    initial_loss,

    initial_acc,

)

best_accuracy = initial_acc

best_round = 0

best_weights = [

    w.copy()

    for w in global_model.get_weights()

]

del x_val

del y_val

gc.collect()

print()

print("=" * 70)
print("START FEDERATED TRAINING")
print("=" * 70)



# ==========================================================
# FEDERATED TRAINING
# ==========================================================

for rnd in range(NUM_ROUNDS):

    current_round = rnd + 1

    print()

    print("=" * 70)
    print(f"ROUND {current_round}")
    print("=" * 70)

    # ------------------------------------------------------
    # One Federated Round
    # ------------------------------------------------------

    loss, acc = run_one_round(
        client_update_fn
    )

    # ------------------------------------------------------
    # Save History
    # ------------------------------------------------------

    append_training_history(

        history_file,

        current_round,

        loss,

        acc,

    )

    # ------------------------------------------------------
    # Best Model
    # ------------------------------------------------------

    if acc > best_accuracy:

        best_accuracy = acc

        best_round = current_round

        best_weights = [

            w.copy()

            for w in global_model.get_weights()

        ]

        print()

        print("=" * 60)
        print("BEST MODEL UPDATED")
        print("=" * 60)

        print(
            f"Round    : {best_round}"
        )

        print(
            f"Accuracy : {best_accuracy:.4f}"
        )

# ==========================================================
# TRAINING FINISHED
# ==========================================================

print()

print("=" * 70)
print("TRAINING FINISHED")
print("=" * 70)

print(
    f"Best Round      : {best_round}"
)

print(
    f"Best Accuracy   : {best_accuracy:.4f}"
)

# ==========================================================
# SAVE BEST MODEL
# ==========================================================

if best_weights is None:

    raise RuntimeError(
        "Best model belum tersedia."
    )

save_best_model(

    model=global_model,

    best_weights=best_weights,

    dataset_name="validation",

)

# ==========================================================
# SAVE FINAL MODEL
# ==========================================================

save_final_model(
    global_model
)

# ==========================================================
# TRAINING TIME
# ==========================================================

end_time = time.time()

training_seconds = end_time - start_time

write_training_time(

    note_path,

    training_seconds,

)

print()

print(
    f"Training Time : "
    f"{training_seconds:.2f} seconds"
)

# ==========================================================
# CLEAR VALIDATION DATA
# ==========================================================

clear_validation_data()

gc.collect()

print()

print(
    "Validation data released."
)





# ==========================================================
# LOAD TEST DATA
# ==========================================================

from dataset import (
    load_dataset23_test,
    load_test_data21,
)

from common import (
    calculate_metrics,
    save_test_results_to_csv,
    write_final_results,
)

print()

print("=" * 70)
print("LOAD TEST DATA")
print("=" * 70)

x_test23, y_test23 = load_dataset23_test()

x_test21, y_test21 = load_test_data21()

print(f"Dataset23 : {len(y_test23)} samples")

print(f"Dataset21 : {len(y_test21)} samples")


# ==========================================================
# HELPER
# ==========================================================

def evaluate_model(

    model,

    x_test,

    y_test,

    dataset_name,

):

    print()

    print("=" * 70)
    print(dataset_name)
    print("=" * 70)

    loss, acc = model.evaluate(

        x_test,

        y_test,

        verbose=1,

    )

    pred = np.argmax(

        model.predict(
            x_test,
            verbose=0,
        ),

        axis=1,

    )

    metrics = calculate_metrics(

        y_test,

        pred,

    )

    metrics["loss"] = loss

    print()

    print(f"Loss      : {loss:.6f}")

    print(f"Accuracy  : {metrics['accuracy']:.4f}")

    print(f"Precision : {metrics['precision_macro']:.4f}")

    print(f"Recall    : {metrics['recall_macro']:.4f}")

    print(f"F1 Score  : {metrics['f1_macro']:.4f}")

    print()

    print("Confusion Matrix")

    print(metrics["confusion_matrix"])

    return metrics


# ==========================================================
# FINAL MODEL
# ==========================================================

print()

print("=" * 70)
print("FINAL GLOBAL MODEL")
print("=" * 70)

final_metrics23 = evaluate_model(

    global_model,

    x_test23,

    y_test23,

    "Dataset23",

)

final_metrics21 = evaluate_model(

    global_model,

    x_test21,

    y_test21,

    "Dataset21",

)


# ==========================================================
# BEST MODEL
# ==========================================================

print()

print("=" * 70)
print("BEST GLOBAL MODEL")
print("=" * 70)

global_model.set_weights(
    best_weights
)

best_metrics23 = evaluate_model(

    global_model,

    x_test23,

    y_test23,

    "Dataset23",

)

best_metrics21 = evaluate_model(

    global_model,

    x_test21,

    y_test21,

    "Dataset21",

)


# ==========================================================
# SAVE RESULT
# ==========================================================

write_final_results(

    note_path=note_path,

    final_metrics23=final_metrics23,

    final_metrics21=final_metrics21,

    best_metrics23=best_metrics23,

    best_metrics21=best_metrics21,

    best_round=best_round,

)

save_test_results_to_csv(

    final_metrics23,

    final_metrics21,

    best_metrics23,

    best_metrics21,

)


# ==========================================================
# SUMMARY
# ==========================================================

print()

print("=" * 70)
print("FINAL SUMMARY")
print("=" * 70)

print()

print("Final Global Model")

print(

    f"Dataset23 Accuracy : "

    f"{final_metrics23['accuracy']:.4f}"

)

print(

    f"Dataset21 Accuracy : "

    f"{final_metrics21['accuracy']:.4f}"

)

print()

print("Best Global Model")

print(

    f"Round : {best_round}"

)

print(

    f"Dataset23 Accuracy : "

    f"{best_metrics23['accuracy']:.4f}"

)

print(

    f"Dataset21 Accuracy : "

    f"{best_metrics21['accuracy']:.4f}"

)

print()

print("=" * 70)
print("FINISHED")
print("=" * 70)


# ==========================================================
# CLEAN MEMORY
# ==========================================================

del x_test23
del y_test23

del x_test21
del y_test21

gc.collect()