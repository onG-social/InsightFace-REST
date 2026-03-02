import json
import os

from if_rest.logger import logger


class Configs(object):

    def __init__(self, models_dir: str = None):
        """
        Initialize configuration with a dynamic models directory.
        """

        # Determine project root (two levels up from this file)
        base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )

        # If MODELS_DIR env variable exists, use it
        # Otherwise default to project_root/models
        if models_dir is None:
            models_dir = os.path.join(base_dir, "models")

        self.models_dir = self._get_param("MODELS_DIR", models_dir)

        self.onnx_models_dir = os.path.join(self.models_dir, "onnx")
        self.trt_engines_dir = os.path.join(self.models_dir, "trt-engines")

        self.models = self.__read_models_file()

        self.type2path = dict(
            onnx=self.onnx_models_dir,
            engine=self.trt_engines_dir,
            plan=self.trt_engines_dir
        )

    def __read_models_file(self):
        models_default_path = os.path.join(self.models_dir, "models.json")
        models_override_path = os.path.join(self.models_dir, "models.override.json")

        models_conf = models_default_path

        if os.path.exists(models_override_path):
            models_conf = models_override_path
            logger.warning(f"Found '{models_override_path}', using this instead of default.")

        if not os.path.exists(models_conf):
            raise FileNotFoundError(f"models.json not found at: {models_conf}")

        with open(models_conf, "r") as f:
            return json.load(f)

    def _get_param(self, ENV, default=None):
        return os.environ.get(ENV, default)

    def build_model_paths(self, model_name: str, ext: str):
        base = self.type2path[ext]
        parent = os.path.join(base, model_name)
        file = os.path.join(parent, f"{model_name}.{ext}")
        return parent, file

    def get_outputs_order(self, model_name):
        return self.models.get(model_name, {}).get("outputs")

    def get_shape(self, model_name):
        return self.models.get(model_name, {}).get("shape")

    def get_dl_link(self, model_name):
        return self.models.get(model_name, {}).get("link")

    def get_dl_type(self, model_name):
        return self.models.get(model_name, {}).get("dl_type")

    def get_function(self, model_name):
        return self.models.get(model_name, {}).get("function")


config = Configs()
