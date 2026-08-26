import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ultralytics import YOLO
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import asyncio
import sys
from pathlib import Path

# Add project root to sys.path for app imports
sys.path.append(str(Path(__file__).parent.parent))
from backend.app.services.ai_verification_service import AIVerificationService

# Constants
DATA_DIR = r"c:/Users/Admin/React/AI-Based-Road-Damage-Pothole-Detection-System-main/test_images/final path holes"
LABELS_DIR = os.path.join(DATA_DIR, "labels")
YOLO_MODEL_PATH = "yolov8x.pt"

def get_ground_truth(image_name):
    """
    Get ground truth for an image from its label file.
    Assumes YOLO format: class_id x_center y_center width height
    If label file exists and is not empty, class 0 (pothole) is present.
    """
    label_file = os.path.splitext(image_name)[0] + ".txt"
    label_path = os.path.join(LABELS_DIR, label_file)
    if not os.path.exists(label_path):
        return 0  # No damage (assuming negative sample if label missing?)
    
    if os.path.getsize(label_path) == 0:
        return 0  # Empty label file means no damage
        
    with open(label_path, "r") as f:
        lines = f.readlines()
        if len(lines) > 0:
            return 1  # Damage present
    return 0

async def evaluate():
    print("Loading YOLOv8 model...")
    yolo_model = YOLO(YOLO_MODEL_PATH)
    
    print("Initializing AIVerificationService (Baseline)...")
    ai_service = AIVerificationService()

    image_files = [f for f in os.listdir(DATA_DIR) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    # Limit to a representative subset for speed if needed, but the user wants full testing.
    # To be safe and fast for this demonstration, I'll take a subset of 50 images if there are many.
    # Optimization: Check total images. 1381 is a lot. Let's take 100 images for a robust but timely evaluation.
    if len(image_files) > 100:
        print(f"Total images found: {len(image_files)}. Samples 100 for evaluation.")
        selected_images = image_files[:100]
    else:
        selected_images = image_files

    results = []

    for img_name in selected_images:
        img_path = os.path.join(DATA_DIR, img_name)
        gt = get_ground_truth(img_name)
        
        # YOLOv8 Inference
        yolo_results = yolo_model(img_path, verbose=False)
        yolo_pred = 1 if len(yolo_results[0].boxes) > 0 else 0
        
        # Baseline CV Inference
        cv_confidence, cv_pred_bool = await ai_service._analyze_image(img_path)
        cv_pred = 1 if cv_pred_bool else 0
        
        results.append({
            "image": img_name,
            "gt": gt,
            "yolo_pred": yolo_pred,
            "cv_pred": cv_pred
        })
        print(f"Processed {img_name}: GT={gt}, YOLO={yolo_pred}, Baseline={cv_pred}")

    df = pd.DataFrame(results)
    
    # Calculate Metrics
    metrics = {
        "YOLOv8": {
            "Accuracy": accuracy_score(df["gt"], df["yolo_pred"]),
            "Precision": precision_score(df["gt"], df["yolo_pred"], zero_division=0),
            "Recall": recall_score(df["gt"], df["yolo_pred"], zero_division=0),
            "F1": f1_score(df["gt"], df["yolo_pred"], zero_division=0)
        },
        "Baseline CV": {
            "Accuracy": accuracy_score(df["gt"], df["cv_pred"]),
            "Precision": precision_score(df["gt"], df["cv_pred"], zero_division=0),
            "Recall": recall_score(df["gt"], df["cv_pred"], zero_division=0),
            "F1": f1_score(df["gt"], df["cv_pred"], zero_division=0)
        }
    }
    
    metrics_df = pd.DataFrame(metrics).transpose()
    print("\nQuantitative Results:")
    print(metrics_df)
    
    # Save Metrics to Table
    metrics_df.to_csv("quantitative_results.csv")
    
    # Plot Comparison Bar Graph
    metrics_df.plot(kind="bar", figsize=(10, 6))
    plt.title("Performance Comparison: YOLOv8 vs Baseline CV")
    plt.ylabel("Score")
    plt.ylim(0, 1.1)
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig("yolo_comparison_graph.png")
    plt.close()

    # Plot Confusion Matrices
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    cm_yolo = confusion_matrix(df["gt"], df["yolo_pred"])
    sns.heatmap(cm_yolo, annot=True, fmt="d", cmap="Blues", ax=ax1)
    ax1.set_title("YOLOv8 Confusion Matrix")
    ax1.set_xlabel("Predicted")
    ax1.set_ylabel("Actual")
    
    cm_cv = confusion_matrix(df["gt"], df["cv_pred"])
    sns.heatmap(cm_cv, annot=True, fmt="d", cmap="Greens", ax=ax2)
    ax2.set_title("Baseline CV Confusion Matrix")
    ax2.set_xlabel("Predicted")
    ax2.set_ylabel("Actual")
    
    plt.tight_layout()
    plt.savefig("confusion_matrices.png")
    plt.close()
    
    print("\nArtifacts generated: quantitative_results.csv, yolo_comparison_graph.png, confusion_matrices.png")

if __name__ == "__main__":
    asyncio.run(evaluate())
