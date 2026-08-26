from ultralytics import YOLO
from pathlib import Path
import os

# Use the most advanced YOLO model (YOLOv8x)
model = YOLO('yolov8x.pt')  # This will download the model if not present

data_dir = Path(r'c:/Users/Admin/React/AI-Based-Road-Damage-Pothole-Detection-System-main/test_images/final path holes')
image_files = list(data_dir.glob('*.jpg')) + list(data_dir.glob('*.jpeg')) + list(data_dir.glob('*.png'))

output_dir = Path('runs/detect/pothole_yolov8')
output_dir.mkdir(parents=True, exist_ok=True)

for img_path in image_files:
    results = model(img_path, save=True, project=str(output_dir), name='exp', exist_ok=True)
    print(f"Processed: {img_path}")

print(f"Detection complete. Results saved in {output_dir}/exp/")
