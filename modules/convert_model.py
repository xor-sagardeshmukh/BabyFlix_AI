from diffusers.pipelines.stable_diffusion.convert_from_ckpt import download_from_original_stable_diffusion_ckpt

def prepare_model(model_path): 
    pipe = download_from_original_stable_diffusion_ckpt(
        checkpoint_path = model_path,
        from_safetensors=True
    )
    pipe.save_pretrained("model/")
   