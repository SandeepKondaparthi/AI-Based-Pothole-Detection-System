import os
import shutil
import random
from pathlib import Path

# Paths
BASE_DIR = Path(r"c:/Users/Admin/React/AI-Based-Road-Damage-Pothole-Detection-System-main")
SOURCE_IMG_DIR = BASE_DIR / "test_images" / "final path holes"
SOURCE_LBL_DIR = SOURCE_IMG_DIR / "labels"
DATASET_DIR = BASE_DIR / "yolo_dataset"

# Target structure
TARGET_DIRS = [
    DATASET_DIR / "images" / "train",
    DATASET_DIR / "images" / "val",
    DATASET_DIR / "labels" / "train",
    DATASET_DIR / "labels" / "val",
]

def prepare_dataset():
    # Create directories
    for d in TARGET_DIRS:
        d.mkdir(parents=True, exist_ok=True)
        print(f"Created/Verified: {d}")

    # Get all images
    images = [f for f in os.listdir(SOURCE_IMG_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    random.seed(42)
    random.shuffle(images)

    split_idx = int(len(images) * 0.8)
    train_images = images[:split_idx]
    val_images = images[split_idx:]

    print(f"Total images: {len(images)}")
    print(f"Training set: {len(train_images)}")
    print(f"Validation set: {len(val_images)}")

    def move_files(file_list, target_img_dir, target_lbl_dir):
        count = 0
        for img_name in file_list:
            # Copy Image
            src_img = SOURCE_IMG_DIR / img_name
            dst_img = target_img_dir / img_name
            shutil.copy2(src_img, dst_img)

            # Copy Label
            lbl_name = Path(img_name).stem + ".txt"
            src_lbl = SOURCE_LBL_DIR / lbl_name
            dst_lbl = target_lbl_dir / lbl_name
            
            if src_lbl.exists():
                shutil.copy2(src_lbl, dst_lbl)
            else:
                # Create empty label for negative samples if needed
                # For this dataset, we assume potholes are labeled.
                open(dst_lbl, 'a').close()
            count += 1
        return count

    print("Moving training files...")
    train_count = move_files(train_images, DATASET_DIR / "images" / "train", DATASET_DIR / "labels" / "train")
    print(f"Moved {train_count} training files.")

    print("Moving validation files...")
    val_count = move_files(val_images, DATASET_DIR / "images" / "val", DATASET_DIR / "labels" / "val")
    print(f"Moved {val_count} validation files.")

    # Create data.yaml
    yaml_content = f"""
path: {DATASET_DIR.as_posix()}
train: images/train
val: images/val

names:
  0: pothole
"""
    with open(DATASET_DIR / "data.yaml", "w") as f:
        f.write(yaml_content.strip())
    print(f"Created data.yaml at {DATASET_DIR / 'data.yaml'}")

if __name__ == "__main__":
    prepare_dataset()
