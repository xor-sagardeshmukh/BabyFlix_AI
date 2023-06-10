from concurrent.futures import ThreadPoolExecutor
import os
import shutil
import time
import traceback
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image

from modules.config import Config
from modules.img2img import Img2Img


class SdGenService():
    observer = None
    pool_executor = None
    img2img = None

    def __init__(self):
        self.img2img = Img2Img()
        self.observer = Observer()
        event_handler = FileSystemEventHandler()
        event_handler.on_created = self.on_created
        self.observer.schedule(
            event_handler, Config().input_folder, recursive=False)
        self.observer.start()

        self.pool_executor = ThreadPoolExecutor(
            max_workers=1)
        self.load_work()

    def load_work(self):
        if not os.path.exists(Config().input_folder):
            os.makedirs(Config().input_folder)
            return
        file_list = os.listdir(Config().input_folder)
        for file_name in file_list:
            self.pool_executor.submit(self.process_image, file_name)

    def on_created(self, event):
        file_name = os.path.basename(event.src_path)
        self.pool_executor.submit(self.process_image, file_name)

    def process_image(self, file_name):
        try:
            # Load source image
            print(f"Process Image: {file_name}")
            file_input_path = os.path.join(Config().input_folder, file_name)
            output_folder = os.path.join(
                Config().output_folder, f"{int(time.time())}-img")
            os.makedirs(output_folder)
            
            # Resize Image to closes 768px
            image = Image.open(file_input_path).convert("RGB")
            original_width, original_height = image.size
            aspect_ratio = original_width / original_height
            if original_width > original_height:
                target_width = 768
                target_height = round(target_width / aspect_ratio)
            else:
                target_height = 768
                target_width = round(target_height * aspect_ratio)
            resized_image = image.resize((target_width, target_height))
            resized_image.save(os.path.join(output_folder, "resized_src.png"))

            # Generate Image Batch
            for i in range(1, int(Config().batch)+1):
                print(f"Image Generate: {i}/{Config().batch}")
                gen_image = Img2Img().generate(resized_image, output_folder, i)
                print(f"Image Generated: {gen_image}")

            # Move Source Image to output folder
            file_output_path = os.path.join(output_folder, "src.png")
            if os.path.isfile(file_input_path):
                shutil.move(file_input_path, file_output_path)
        except:
            traceback.print_exc()


if __name__ == "__main__":
    service = SdGenService()
    try:
        while True:
            time.sleep(1)
    finally:
        service.observer.stop()
        service.observer.join()
