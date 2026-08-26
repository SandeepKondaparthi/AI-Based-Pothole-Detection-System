from ultralytics import YOLO
import os
from pathlib import Path

def train_model():
    # Paths
    BASE_DIR = Path(r"c:/Users/Admin/React/AI-Based-Road-Damage-Pothole-Detection-System-main")
    DATA_YAML = BASE_DIR / "yolo_dataset" / "data.yaml"
    MODEL_PATH = "yolov8x.pt"
    
    # Load model
    print(f"Loading model from {MODEL_PATH}...")
    model = YOLO(MODEL_PATH)
    
    # Train
    print("Starting training...")
    # Using small number of epochs and image size for demonstration speed
    # but enough to show improvement.
    results = model.train(
        data=str(DATA_YAML),
        epochs=10,
        imgsz=640,
        batch=4,  # Small batch to avoid memory issues on typical hardware
        name='pothole_tuning',
        exist_ok=True
    )
    
    print("Training complete.")
    # The best weights are usually saved in runs/detect/pothole_tuning/weights/best.pt
    # but let's confirm the path or save it specifically.
    save_path = BASE_DIR / "backend" / "yolov8x_fine_tuned.pt"
    model.export(format='engine') # Just in case, but weights are what we need
    
    # Copy best weights to the backend folder for easy access
    best_weights = Path("runs/detect/pothole_tuning/weights/best.pt")
    if best_weights.exists():
        import shutil
        shutil.copy2(best_weights, save_path)
        print(f"Best weights saved to {save_path}")
    else:
        print("Warning: Best weights not found in expected location.")

if __name__ == "__main__":
    train_model()
