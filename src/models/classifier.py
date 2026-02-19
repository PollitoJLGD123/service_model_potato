import tensorflow as tf
import numpy as np
from keras.preprocessing import image
import json
from src.constants.general import MODEL_PATH, JSON_PATH
from keras.models import load_model
from PIL import Image
import io
from keras.applications.efficientnet import preprocess_input


class PotatoDiseaseClassifier:
    def __init__(self):
        self.model = load_model(MODEL_PATH)

        with open(JSON_PATH, "r") as f:
            self.info = json.load(f)

        self.class_names = self.info["class_names"]
        self.img_size = self.info["img_size"]

    def _predict_from_pil(self, img: Image.Image):
        """
        Recibe una imagen PIL, la preprocesa y devuelve el resultado del modelo.
        """
        img = img.resize((self.img_size, self.img_size))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)

        img_array = preprocess_input(img_array)

        predictions = self.model.predict(img_array, verbose=0)
        predicted_class = np.argmax(predictions[0])
        confidence = predictions[0][predicted_class]

        result = {
            "clase_predicha": self.class_names[predicted_class],
            "confianza": float(confidence),
            "todas_predicciones": {
                self.class_names[i]: float(predictions[0][i])
                for i in range(len(self.class_names))
            },
        }

        return result

    def predict(self, img_path: str):
        """
        Predicción a partir de un path en disco (modo legacy).
        """
        img = Image.open(img_path).convert("RGB")
        return self._predict_from_pil(img)

    def predict_bytes(self, img_bytes: bytes):
        """
        Predicción a partir de bytes de imagen (subida desde el frontend).
        """
        img = Image.open(io.BytesIO(img_bytes))
        return self._predict_from_pil(img)

    def predict_batch(self, img_paths):
        """
        Predice múltiples imágenes a partir de paths en disco.
        """
        results = []
        for img_path in img_paths:
            result = self.predict(img_path)
            result["imagen"] = img_path
            results.append(result)
        return results


classifier = PotatoDiseaseClassifier()