import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path

root = Path(__file__).resolve().parent.parent.parent
image_path = root / "data" / "computer_vision_engine" / "images" / "image.png"
output_path = root / "data" / "computer_vision_engine" / "images" / "output_image.png"

def load_image_as_tensor(path):
    """Loads a PNG and converts it into a 3D NumPy Tensor."""
    if not path.exists():
        print(f"❌ Error: Could not find image at {path}")
        print("Please put a color image named 'image.png' in the data/images/ folder!")
        exit()
        
    img = Image.open(path)
    tensor = np.array(img) / 255.0 
    print(f"📸 Image Loaded! Tensor Shape: {tensor.shape} | Dimensions: {tensor.ndim}D")
    return tensor

def apply_grayscale(image_tensor):
    """Uses the Dot Product to crush 3 RGB channels into 1 Grayscale channel."""
    weights = np.array([0.2989, 0.5870, 0.1140])
    
    grayscale_matrix = np.dot(image_tensor[..., :3], weights)
    return grayscale_matrix

def apply_sepia(image_tensor):
    """Uses Matrix Multiplication to apply a vintage Sepia filter."""
    sepia_weights = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])
    
    sepia_tensor = image_tensor[..., :3] @ sepia_weights.T
    
    sepia_tensor = np.clip(sepia_tensor, 0, 1)
    return sepia_tensor

def visualize_transformations(original, grayscale, sepia):
    """Draws the Tensors side-by-side using Matplotlib."""
    print("🎨 Rendering Tensor Transformations...")
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].imshow(original)
    axes[0].set_title(f"Original RGB Tensor\nShape: {original.shape}")
    axes[0].axis('off')
    
    axes[1].imshow(grayscale, cmap='gray')
    axes[1].set_title(f"Grayscale Matrix (Dot Product)\nShape: {grayscale.shape}")
    axes[1].axis('off')
    
    axes[2].imshow(sepia)
    axes[2].set_title(f"Sepia Filter (Matrix Math)\nShape: {sepia.shape}")
    axes[2].axis('off')
    
    plt.tight_layout()
    
    plt.savefig(output_path)
    print(f"💾 Render saved to: {output_path.name}")
    plt.show()

if __name__ == "__main__":
    print("--- 👁️ NUMPY COMPUTER VISION ENGINE ---")
    
    original_tensor = load_image_as_tensor(image_path)
    
    gray_matrix = apply_grayscale(original_tensor)
    sepia_tensor = apply_sepia(original_tensor)
    
    visualize_transformations(original_tensor, gray_matrix, sepia_tensor)