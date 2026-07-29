import requests
import numpy as np

class PreprocessingClient:
    """
    Client untuk berkomunikasi dengan Preprocessing Engine.
    """

    def __init__(self):

        self.base_url = "http://127.0.0.1:8000"

    def get_preprocessed_data(self):

        response = requests.get(

            f"{self.base_url}/preprocessing/data"

        )

        response.raise_for_status()

        data = response.json()

        for item in data:

            item["image"] = np.array(

                item["image"],

                dtype=np.float32

            )

        return data