from config import MODELS


class ModelManager:

    def get_available_models(self):

        models = []

        for key, value in MODELS.items():

            models.append({

                "id": key,

                "name": value["display_name"],

                "framework": value["framework"],

                "window_size": value["window_size"],

                "dwt_level": value["dwt_level"],

                "input_size": value["input_size"],

                "classes": value["classes"],

                "file_size": value["file_size"]

            })

        return models