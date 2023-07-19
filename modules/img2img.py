
import random
from diffusers import StableDiffusionImg2ImgPipeline, DPMSolverMultistepScheduler
from PIL import Image
from modules.config import Config
from modules.common.singleton import Singleton
import os
import io
import torch
from modules.convert_model import prepare_model


class Img2Img(metaclass=Singleton):
    pipe: StableDiffusionImg2ImgPipeline

    def __init__(self):
        self.load_model()

    def load_model(self):
        if Config().model_loaded():
            print("Img2Img: Load Model")
            self.pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
                "model"
            ).to("cuda")
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_pretrained(
                "model/scheduler",
                algorithm_type="dpmsolver++", solver_order=2, use_karras_sigmas=True)
            self.pipe.safety_checker = None
            print("Img2Img: Model Loaded")
        else:
            print("Img2Img: Scan for Model")
            if not os.path.exists('model'):
                os.makedirs('model')
            if os.path.exists(Config().model) and os.path.isfile(Config().model) and Config().model.endswith(".safetensors"):
                print("Img2Img: Prepare Model")
                prepare_model(Config().model)
                self.load_model()
            else:
                raise Exception("No Model")

    def generate(self, img_src, oputput_folder, index):
        seed = random.randint(0, 2147483647)
        generator = torch.Generator(device="cuda").manual_seed(seed)
        print(f"Generate: prompt={Config().prompt} negative prompt={Config().negative_prompt} strength={float(Config().denoise)} guidance_scale={float(Config().cfg)} num_inference_steps={int(Config().steps)} seed={seed}")
        images = self.pipe(prompt=Config().prompt, negative_prompt=Config().negative_prompt, image=img_src,
                           strength=float(Config().denoise), guidance_scale=float(Config().cfg), num_inference_steps=int(Config().steps), generator=generator).images
        filepath = os.path.join(oputput_folder, f"{index}.png")
        images[0].save(filepath)
        return filepath
