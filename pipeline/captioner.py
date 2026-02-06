from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

class Captioner:
    def __init__(self, model_name: str = "Salesforce/blip-image-captioning-base"):
        self.device = torch.device("cpu")
        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name).to(self.device)

    @torch.inference_mode()
    def caption(self, image: Image.Image, max_new_tokens: int = 30) -> str:
        image = image.convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        out = self.model.generate(**inputs, max_new_tokens=max_new_tokens)
        return self.processor.decode(out[0], skip_special_tokens=True).strip()
