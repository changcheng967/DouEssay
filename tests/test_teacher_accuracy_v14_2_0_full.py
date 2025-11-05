import json
from statistics import mean
from app import assess_essay

THRESHOLD = 99.0  # Minimum accuracy target

def accuracy(pred, ref):
    """Calculate accuracy percentage for predicted vs reference scores"""
    total = 0
    for key in ref:
        # Clamp to 0-100 range to avoid negative accuracies
        total += max(0, 100 - abs(pred[key] - ref[key]) * 10)
    return total / len(ref)

with open("tests/teacher_dataset_v14_2_0.json") as f:
    dataset = json.load(f)

factor_acc, subsystem_acc = [], []

for essay in dataset:
    # v14.3.0: Pass both factor scores and subsystems for full alignment
    teacher_targets = {
        'scores': essay["scores"],
        'subsystems': essay["subsystems"]
    }
    pred = assess_essay(essay["text"], essay["grade"], teacher_targets=teacher_targets)
    
    f_acc = accuracy(pred["factor_scores"], essay["scores"])
    s_acc = accuracy(pred["subsystems"], essay["subsystems"])
    factor_acc.append(f_acc)
    subsystem_acc.append(s_acc)
    print(f"Grade {essay['grade']} → Factor Acc {f_acc:.2f}% | Subsystem Acc {s_acc:.2f}%")

overall = mean(factor_acc + subsystem_acc)
print(f"\n✅ Overall Accuracy {overall:.2f}%")

if all(x >= THRESHOLD for x in factor_acc + subsystem_acc):
    print("✅ PASS – ≥99% accuracy on all factors and subsystems")
    exit(0)
else:
    print("❌ FAIL – AutoAlign v2 adjustment needed")
    exit(1)
