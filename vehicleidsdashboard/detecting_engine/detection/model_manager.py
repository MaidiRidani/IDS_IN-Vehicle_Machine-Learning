from pathlib import Path
import tensorflow as tf

class ModelManager:
    """
    Mengelola file model yang tersedia.
    """

    def __init__(self):

        self.model_folder = Path("model")

    def get_available_models(self):

        if not self.model_folder.exists():

            return []

        models = []

        for file in self.model_folder.iterdir():

            if file.is_file() and file.suffix.lower() in [".h5", ".keras"]:

                models.append(file.name)

        models.sort()

        return models
    
    def load_model(self, model_name):
        """
        Memuat model TensorFlow berdasarkan nama file.

        Parameters
        ----------
        model_name : str

        Returns
        -------
        tuple
            (model, model_path)
        """

        model_path = self.model_folder / model_name

        if not model_path.exists():

            raise ValueError(

                f"Model '{model_name}' tidak ditemukan."

            )

        model = tf.keras.models.load_model(

            model_path,

            compile=False,

        )

        return model, model_path
    


    def extract_model_info(self, model, model_path):
        """
        Mengambil informasi dasar dari model.
        """

        return {

            "model_name": model_path.name,

            "framework": "TensorFlow / Keras",

            "input_shape": list(model.input_shape),

            "output_classes": model.output_shape[-1],

            "total_parameters": model.count_params(),

            "file_size_mb": round(
                model_path.stat().st_size / (1024 * 1024),
                2
            ),

        }