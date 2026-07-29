from detection.configuration import Configuration
from detection.state import State
from detection.model_manager import ModelManager
from detection.preprocessing_client import PreprocessingClient
import numpy as np
from detection.class_labels import CLASS_LABELS, CLASS_NAMES
from datetime import datetime
from time import perf_counter



class DetectionEngine:

    def __init__(self):

        self.configuration = Configuration()

        self.state = State()

        self.model_manager = ModelManager()
        self.preprocessing_client = PreprocessingClient()

    def get_available_models(self):

        return self.model_manager.get_available_models()
    
    def load_model(self, model_name):

        model, model_path = self.model_manager.load_model(

            model_name

        )

        info = self.model_manager.extract_model_info(

            model,

            model_path,

        )

        self.state.loaded_model = model

        self.state.loaded_model_name = model_name

        self.state.loaded_model_info = info

        self.configuration.model_name = model_name
    def has_loaded_model(self):

        return self.state.loaded_model is not None
    
    def get_loaded_model_info(self):

        return self.state.loaded_model_info
    


    def is_model_loaded(self):

        return self.state.loaded_model is not None


    def get_current_model(self):

        if not self.is_model_loaded():

            return {

                "loaded": False

            }

        info = self.state.loaded_model_info.copy()

        info["loaded"] = True

        return info 
    
    def run_detection(self):

        if not self.is_model_loaded():

            raise ValueError(

                "Belum ada model yang dimuat."

            )

        data = self.get_preprocessed_data()

        images = []

        for item in data:

            images.append(

                item["image"]

            )

        batch = np.array(

            images,

            dtype=np.float32

        )

        start = perf_counter()

        predictions = self.state.loaded_model.predict(

            batch,

            verbose=0

        )

        batch_latency_ms = (

            perf_counter() - start

        ) * 1000

        average_latency_ms = (

            batch_latency_ms / len(predictions)

        )

        results = []

        for item, prediction in zip(data, predictions):

            pred_idx = int(np.argmax(prediction))

            probabilities = {

                CLASS_LABELS[index]: round(

                    float(probability * 100),

                    2

                )

                for index, probability

                in enumerate(prediction)

            }

            confidence = float(

                prediction[pred_idx] * 100

            )

            results.append({

                "packet_number": item["packet_number"],

                "selected_label": item["selected_label"],

                "window_label": item["window_label"],

                "prediction": CLASS_LABELS[pred_idx],

                "confidence": round(confidence, 2),

                "is_correct":

                    CLASS_LABELS[pred_idx]

                    ==

                    item["window_label"],

                "batch_latency_ms": round(
                    batch_latency_ms,
                    2
                ),

                "average_latency_ms": round(
                    average_latency_ms,
                    2
                ),

                "timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

                "probabilities": probabilities,

            })

        correct = sum(

            result["is_correct"]

            for result in results

        )

        wrong = len(results) - correct

        ground_truth_distribution = {}

        prediction_distribution = {}

        for result in results:

            gt = result["window_label"]

            pred = result["prediction"]

            ground_truth_distribution[gt] = (

                ground_truth_distribution.get(gt, 0) + 1

            )

            prediction_distribution[pred] = (

                prediction_distribution.get(pred, 0) + 1

            )

        labels = CLASS_NAMES
        confusion_matrix = {

            gt: {

                pred: 0

                for pred in labels

            }

            for gt in labels

        }
        for result in results:

            gt = result["window_label"]

            pred = result["prediction"]

            confusion_matrix[gt][pred] += 1

        precision = {}

        for label in labels:

            tp = confusion_matrix[label][label]

            fp = sum(

                confusion_matrix[gt][label]

                for gt in labels

                if gt != label

            )

            precision[label] = round(

                tp / (tp + fp) * 100,

                2

            ) if (tp + fp) > 0 else 0


        recall = {}

        for label in labels:

            tp = confusion_matrix[label][label]

            fn = sum(

                confusion_matrix[label][pred]

                for pred in labels

                if pred != label

            )

            recall[label] = round(

                tp / (tp + fn) * 100,

                2

            ) if (tp + fn) > 0 else 0


        f1_score = {}

        for label in labels:

            p = precision[label]

            r = recall[label]

            f1_score[label] = round(

                2 * p * r / (p + r),

                2

            ) if (p + r) > 0 else 0

        macro_precision = round(

            sum(precision.values()) / len(precision),

            2

        )

        macro_recall = round(

            sum(recall.values()) / len(recall),

            2

        )

        macro_f1_score = round(

            sum(f1_score.values()) / len(f1_score),

            2

        )


        summary = {

            "total_windows": len(results),

            "correct": correct,

            "wrong": wrong,

            "accuracy": round(

                (correct / len(results)) * 100,

                2

            ) if results else 0,

            "batch_latency_ms": round(

                batch_latency_ms,

                2

            ),

            "average_latency_ms": round(

                average_latency_ms,

                2

            ),

            "ground_truth_distribution":

                ground_truth_distribution,

            "prediction_distribution":

                prediction_distribution,

            "confusion_matrix": confusion_matrix,

            "precision": precision,

            "recall": recall,

            "f1_score": f1_score,
            "macro_precision": macro_precision,

            "macro_recall": macro_recall,

            "macro_f1_score": macro_f1_score,


        }

        return {

            "summary": summary,

            "results": results,

        }

            
    def get_preprocessed_data(self):

        return self.preprocessing_client.get_preprocessed_data()
    



    