import os
import sys
import torch
import numpy as np
from PIL import Image
from rembg import remove

# Add TripoSR repository to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "TripoSR-main"))

try:
    from tsr.system import TSR
    from tsr.utils import remove_background, resize_foreground
except ImportError as e:
    print(f"Error importing TripoSR: {e}")
    TSR = None

class ModelHandler:
    def __init__(self):
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load_model(self):
        if self.model is None and TSR is not None:
            print("Loading TripoSR model...")
            # We use the pretrained model from Hugging Face
            self.model = TSR.from_pretrained(
                "stabilityai/TripoSR",
                config_name="config.yaml",
                weight_name="model.ckpt",
            )
            self.model.renderer.set_chunk_size(8192) # Reduce chunk size for 6GB VRAM
            self.model.to(self.device)

    def process(self, image_path, output_dir):
        if self.model is None:
            self.load_model()
            
        if self.model is None:
            raise RuntimeError("Failed to load TripoSR model")

        # Load and preprocess image
        image = Image.open(image_path).convert("RGB")
        
        # Remove background (using rembg directly or tsr util)
        # Using rembg directly is often safer if tsr util fails
        image = remove(image)
        
        # Resize/Center (TripoSR expects object centered)
        # We can use the utility from tsr if available
        image = resize_foreground(image, 0.85)
        image = np.array(image).astype(np.float32) / 255.0
        image = image[:, :, :3] * image[:, :, 3:4] + (1 - image[:, :, 3:4]) * 0.5
        image = Image.fromarray((image * 255.0).astype(np.uint8))

        # Inference
        with torch.no_grad():
            scene_codes = self.model([image], device=self.device)
            
        # Extract Mesh
        meshes = self.model.extract_mesh(scene_codes, has_vertex_color=True, resolution=256)
        
        # Save
        filename = os.path.basename(image_path)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, f"{base_name}.glb")
        
        meshes[0].export(output_path)
        return output_path

# Global instance
_handler = ModelHandler()

def generate_3d_model(image_path, output_dir):
    return _handler.process(image_path, output_dir)
