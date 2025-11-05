import json
from statistics import mean
from app import assess_essay

THRESHOLD = 99.0  # Minimum accuracy target

def accuracy(pred, ref):
    total = 0
    for key in ref:
        total += 100 - abs(pred[key] - ref[key]) * 10
    return total / len(ref)

with open("tests/teacher_dataset_v14_2_0.json") as f:
    dataset = json.load(f)

factor_acc, subsystem_acc = [], []

for essay in dataset:
    # Use assess_essay wrapper with teacher targets for AutoAlign v2
    pred = assess_essay(essay["text"], essay["grade"], teacher_targets=essay["scores"])
    
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
