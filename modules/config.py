from modules.common.singleton import Singleton
import configparser
import os


class Config(metaclass=Singleton):
    model: str
    sampling_method: str
    prompt: str
    steps: int
    batch: int
    cfg: float
    denoise: float
    input_folder: str
    output_folder: str

    def __init__(self):
        self._config = configparser.ConfigParser()
        self._config.read("config.ini")
        self.load_config()

    def load_config(self):
        if self._config.has_section("Settings") == False:
            self._config.add_section("Settings")
        self.model = self.get_config(
            "model", "model/model.safetensors")
        self.prompt = self.get_config(
            "prompt", "newborn portrait close-up in ultrasound, natural colors, ultrasound image of a toddler in natural colorization, medical close-up portrait")
        self.steps = self.get_config("steps", 55)
        self.batch = self.get_config("batch", 2)
        self.cfg = self.get_config("cfg", 10)
        self.denoise = self.get_config("denoise", 0.7)
        self.input_folder = self.get_config("input_folder", "/input")
        self.output_folder = self.get_config("output_folder", "/output")
        with open("config.ini", "w") as configfile:
            self._config.write(configfile)

    def get_config(self, value_key, default_value):
        if self._config.has_option("Settings", value_key):
            return self._config.get("Settings", value_key)
        else:
            self._config.set("Settings", value_key, str(default_value))
            return default_value

    def model_loaded(self):
        model_index_path = 'model/model_index.json'
        return os.path.exists(model_index_path) and os.path.isfile(model_index_path)


Config()
