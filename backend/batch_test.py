import os
import cv2
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app', 'services')))
from app.services.ai_verification_service import AIVerificationService

# Path to images and labels
data_dir = r"c:/Users/Admin/React/AI-Based-Road-Damage-Pothole-Detection-System-main/test_images/final path holes"
labels_dir = os.path.join(data_dir, "labels")

# Get all image files
image_files = [f for f in os.listdir(data_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

# Helper: get label for image

def get_label(image_name):
    label_file = os.path.splitext(image_name)[0] + ".txt"
    label_path = os.path.join(labels_dir, label_file)
    if not os.path.exists(label_path):
        return None
    with open(label_path, "r", encoding="utf-8") as f:
        content = f.read().strip().lower()
        # Simple heuristic: if 'pothole' in label, positive
        return "pothole" in content

# Instantiate detection service
ai_service = AIVerificationService()

results = []
import asyncio
for img_name in image_files:
    img_path = os.path.join(data_dir, img_name)
    gt = get_label(img_name)
    if gt is None:
        continue  # skip if no label
    # Run detection
    confidence, pred = asyncio.run(ai_service._analyze_image(img_path))
    results.append({
        "image": img_name,
        "gt": gt,
        "pred": pred,
        "confidence": confidence
    })

# Compute metrics
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, precision_recall_curve
import matplotlib.pyplot as plt

# Prepare lists
y_true = [r["gt"] for r in results]
y_pred = [r["pred"] for r in results]
confidences = [r["confidence"] for r in results]

acc = accuracy_score(y_true, y_pred)
prec = precision_score(y_true, y_pred)
rec = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)
cm = confusion_matrix(y_true, y_pred)

# Print metrics

# Plot bar graph for metrics
plt.figure()
metrics = [acc, prec, rec, f1]
labels = ["Accuracy", "Precision", "Recall", "F1 Score"]
plt.bar(labels, metrics, color=["blue", "orange", "green", "red"])
plt.ylim(0, 1)
plt.title("Evaluation Metrics")
plt.ylabel("Score")
plt.savefig("metrics_bar_graph.png")

# Plot confusion matrix as heatmap
plt.figure()
import seaborn as sns
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.savefig("confusion_matrix_heatmap.png")

print("Graphs saved: metrics_bar_graph.png, confusion_matrix_heatmap.png")

# Plot Precision-Recall curve
probs = np.array(confidences) / 100.0
precision, recall, thresholds = precision_recall_curve(y_true, probs)
plt.figure()
plt.plot(recall, precision, marker=".")
plt.title("Precision-Recall Curve")
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.savefig("precision_recall_curve.png")

# Plot Accuracy graph
plt.figure()
plt.plot(range(len(y_true)), np.array(y_true) == np.array(y_pred), marker=".")
plt.title("Accuracy Graph")
plt.xlabel("Sample Index")
plt.ylabel("Correct Prediction (1=True, 0=False)")
plt.savefig("accuracy_graph.png")

print("Graphs saved: precision_recall_curve.png, accuracy_graph.png")
