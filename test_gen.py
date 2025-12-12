from generator import generate_3d_model
import os

# Create dummy image if none exists
if not os.path.exists("test_image.png"):
    from PIL import Image
    img = Image.new('RGB', (512, 512), color = 'red')
    img.save("test_image.png")

print("Starting generation...")
try:
    path = generate_3d_model("test_image.png", "output")
    print(f"Success! Model at {path}")
except Exception as e:
    print(f"Failed: {e}")
    import traceback
    traceback.print_exc()
