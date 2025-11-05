"""
Test suite for v14.1.0 - Multi-Grade Accuracy Testing with Per-Factor Validation

Tests for:
- ≥99% overall accuracy across Grades 7-12
- ≥97% per-subsystem accuracy (Argus, Nexus, DepthCore, Empathica, Structura)
- ≥99% per-factor accuracy (Content, Structure, Grammar, Application, Insight)
"""

import json
import csv
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import DouEssay, VERSION


def compare_scores(pred, truth, tolerance=1.0):
    """
    Returns True if score matches teacher within tolerance.
    Using 1.0 point tolerance for 10-point scale scoring (10% tolerance).
    This represents "high accuracy" alignment with teacher grading.
    """
    return abs(pred - truth) <= tolerance


def compare_subsystem_metric(pred_val, truth_val, tolerance=0.05):
    """
    Returns True if subsystem metric matches within tolerance.
    Using 5% tolerance for subsystem metrics (0-1 scale).
    """
    return abs(pred_val - truth_val) <= tolerance


def test_accuracy_v14_1_0():
    """
    Main test function for v14.1.0 accuracy validation.
    Tests against teacher dataset and generates CSV report.
    """
    print("=" * 70)
    print("DouEssay v14.1.0 Accuracy Test Suite")
    print("Multi-Grade Testing: Grades 7-12")
    print("Target: ≥99% Overall, ≥97% Per-Subsystem, ≥99% Per-Factor")
    print("=" * 70)
    
    # Verify version
    assert VERSION == "14.1.0", f"VERSION must be 14.1.0, got {VERSION}"
    print(f"✅ Version: {VERSION}")
    
    # Load teacher dataset
    dataset_path = os.path.join(os.path.dirname(__file__), "teacher_dataset.json")
    with open(dataset_path, "r") as f:
        teacher_dataset = json.load(f)
    
    print(f"✅ Loaded {len(teacher_dataset)} teacher-graded essays")
    
    # Initialize grader
    grader = DouEssay()
    
    results = []
    overall_factor_accuracies = {f: [] for f in ["Content", "Structure", "Grammar", "Application", "Insight"]}
    overall_subsystem_accuracies = {s: [] for s in ["Argus", "Nexus", "DepthCore", "Empathica", "Structura"]}
    
    # Run tests for each essay
    for i, essay in enumerate(teacher_dataset, 1):
        grade = essay["grade"]
        text = essay["text"]
        teacher_scores = essay["scores"]
        teacher_subs = essay["subsystems"]
        
        print(f"\n{'='*70}")
        print(f"Testing Essay {i}/{len(teacher_dataset)} - Grade {grade}")
        print(f"Topic: {essay['topic']}")
        print(f"{'='*70}")
        
        # Grade essay with v14.1.0
        grade_level = f"Grade {grade}"
        full_result = grader.grade_essay(text, grade_level)
        
        # Extract factor scores from detailed_analysis
        detailed = full_result.get('detailed_analysis', {})
        pred_scores = {
            'Content': detailed.get('content', {}).get('score', 0),
            'Structure': detailed.get('structure', {}).get('score', 0),
            'Grammar': detailed.get('grammar', {}).get('score', 0),
            'Application': detailed.get('application', {}).get('score', 0),
            'Insight': detailed.get('insight', {}).get('score', 0)
        }
        
        # Extract subsystem scores
        # Note: These are computed from various analysis results
        pred_subs = {}
        
        # Argus: Counter-argument & rebuttal detection
        counter_arg = full_result.get('evaluate_counter_argument_depth', {})
        # Count counter arguments from the result
        counter_count = counter_arg.get('counter_arguments', 0)
        rebuttal_count = counter_arg.get('rebuttals', 0)
        argus_score = counter_arg.get('depth_score', 0.5)
        pred_subs['Argus'] = {
            'counters': counter_count,
            'rebuttals': rebuttal_count,
            'sophistication': argus_score
        }
        
        # Nexus: Logical flow & transitions
        para_transitions = full_result.get('paragraph_transitions', {})
        structure_data = detailed.get('structure', {})
        nexus_score = para_transitions.get('score', structure_data.get('coherence_score', 0.5))
        pred_subs['Nexus'] = {
            'transitions': para_transitions.get('transition_count', 0),
            'flow_score': nexus_score
        }
        
        # DepthCore: Evidence depth & connections
        claim_evidence = full_result.get('claim_evidence_ratio', {})
        content_data = detailed.get('content', {})
        # Count evidence connections from content analysis
        evidence_rel = content_data.get('evidence_relevance', {})
        depthcore_score = evidence_rel.get('relevance_score', 0.5)
        pred_subs['DepthCore'] = {
            'evidence_connections': content_data.get('example_count', 0),
            'claim_strength': depthcore_score
        }
        
        # Empathica: Emotional tone & engagement
        emotionflow = full_result.get('emotionflow_v2', {})
        tone_analysis = full_result.get('tone_analysis', {})
        empathica_score = emotionflow.get('engagement_level', 50) / 100.0
        # Detect tone from analysis
        tone = tone_analysis.get('dominant_tone', 'Neutral')
        if 'positive' in str(tone).lower() or 'optimistic' in str(tone).lower():
            tone = 'Positive'
        elif 'negative' in str(tone).lower():
            tone = 'Negative'
        else:
            tone = 'Neutral'
        pred_subs['Empathica'] = {
            'tone': tone,
            'engagement': empathica_score,
            'anecdotes': detailed.get('application', {}).get('insight_score', 0) * 5  # Estimate
        }
        
        # Structura: Paragraph structure & coherence
        para_struct = full_result.get('paragraph_structure_v12', {})
        structura_score = structure_data.get('coherence_score', 0.5)
        pred_subs['Structura'] = {
            'topic_sentences': structure_data.get('paragraph_count', 0),
            'paragraph_coherence': structura_score
        }
        
        # Compare factor scores
        print("\n📊 Factor Scores (Teacher vs Predicted):")
        factor_accuracies = {}
        for factor in teacher_scores:
            teacher_val = teacher_scores[factor]
            pred_val = pred_scores[factor]
            matches = compare_scores(pred_val, teacher_val)
            factor_accuracies[factor] = 1.0 if matches else 0.0
            overall_factor_accuracies[factor].append(factor_accuracies[factor])
            
            status = "✅" if matches else "❌"
            print(f"  {status} {factor}: Teacher={teacher_val:.1f}, Predicted={pred_val:.1f}, Diff={abs(pred_val-teacher_val):.1f}")
        
        # Compare subsystem metrics
        print("\n🔧 Subsystem Metrics:")
        subsystem_accuracies = {}
        for sub in teacher_subs:
            sub_gt = teacher_subs[sub]
            sub_pred = pred_subs.get(sub, {})
            
            # Compare each metric in the subsystem
            matches = []
            for metric in sub_gt:
                truth_val = sub_gt[metric]
                pred_val = sub_pred.get(metric, 0)
                
                # Different comparison based on metric type
                if isinstance(truth_val, str):
                    # String comparison (e.g., tone)
                    match = (truth_val == pred_val)
                elif isinstance(truth_val, int):
                    # Integer counts - allow ±1 tolerance
                    match = abs(pred_val - truth_val) <= 1
                else:
                    # Float metrics - use subsystem tolerance
                    match = compare_subsystem_metric(pred_val, truth_val)
                
                matches.append(1.0 if match else 0.0)
            
            # Average accuracy for this subsystem
            sub_acc = sum(matches) / len(matches) if matches else 0.0
            subsystem_accuracies[sub] = sub_acc
            overall_subsystem_accuracies[sub].append(sub_acc)
            
            status = "✅" if sub_acc >= 0.97 else "❌"
            print(f"  {status} {sub}: {sub_acc:.3f}")
        
        # Calculate overall accuracy for this essay
        avg_factor_acc = sum(factor_accuracies.values()) / len(factor_accuracies)
        avg_sub_acc = sum(subsystem_accuracies.values()) / len(subsystem_accuracies)
        overall_acc = (avg_factor_acc + avg_sub_acc) / 2
        
        print(f"\n📈 Essay Overall Accuracy: {overall_acc:.3f}")
        
        # Store results
        results.append({
            "grade": grade,
            "topic": essay["topic"],
            "factor_accuracies": factor_accuracies,
            "subsystem_accuracies": subsystem_accuracies,
            "overall_accuracy": overall_acc
        })
    
    # Calculate aggregate statistics
    print(f"\n{'='*70}")
    print("AGGREGATE RESULTS")
    print(f"{'='*70}")
    
    # Per-factor accuracy across all essays
    print("\n📊 Per-Factor Accuracy (Target: ≥99%):")
    all_factors_pass = True
    for factor in overall_factor_accuracies:
        accs = overall_factor_accuracies[factor]
        avg_acc = sum(accs) / len(accs) if accs else 0.0
        passed = avg_acc >= 0.99
        status = "✅" if passed else "❌"
        print(f"  {status} {factor}: {avg_acc:.3f}")
        if not passed:
            all_factors_pass = False
    
    # Per-subsystem accuracy across all essays
    print("\n🔧 Per-Subsystem Accuracy (Target: ≥97%):")
    all_subsystems_pass = True
    for subsystem in overall_subsystem_accuracies:
        accs = overall_subsystem_accuracies[subsystem]
        avg_acc = sum(accs) / len(accs) if accs else 0.0
        passed = avg_acc >= 0.97
        status = "✅" if passed else "❌"
        print(f"  {status} {subsystem}: {avg_acc:.3f}")
        if not passed:
            all_subsystems_pass = False
    
    # Overall accuracy
    print("\n📈 Overall Accuracy (Target: ≥99%):")
    overall_accs = [r["overall_accuracy"] for r in results]
    overall_avg = sum(overall_accs) / len(overall_accs) if overall_accs else 0.0
    overall_pass = overall_avg >= 0.99
    status = "✅" if overall_pass else "❌"
    print(f"  {status} Overall: {overall_avg:.3f}")
    
    # Write CSV report
    csv_path = os.path.join(os.path.dirname(__file__), "accuracy_report_v14_1_0.csv")
    with open(csv_path, "w", newline="") as csvfile:
        fieldnames = ["grade", "topic", "overall_accuracy"]
        fieldnames += [f"factor_{f}" for f in ["Content", "Structure", "Grammar", "Application", "Insight"]]
        fieldnames += [f"sub_{s}" for s in ["Argus", "Nexus", "DepthCore", "Empathica", "Structura"]]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for r in results:
            row = {
                "grade": r["grade"],
                "topic": r["topic"],
                "overall_accuracy": f"{r['overall_accuracy']:.3f}"
            }
            row.update({f"factor_{k}": f"{v:.3f}" for k, v in r["factor_accuracies"].items()})
            row.update({f"sub_{k}": f"{v:.3f}" for k, v in r["subsystem_accuracies"].items()})
            writer.writerow(row)
    
    print(f"\n✅ Accuracy report written to: {csv_path}")
    
    # Final verdict
    print(f"\n{'='*70}")
    if all_factors_pass and all_subsystems_pass and overall_pass:
        print("✅ ALL ACCURACY TARGETS MET!")
        print("   ✅ Per-Factor Accuracy: ≥99%")
        print("   ✅ Per-Subsystem Accuracy: ≥97%")
        print("   ✅ Overall Accuracy: ≥99%")
        print(f"{'='*70}")
        return True
    else:
        print("❌ ACCURACY TARGETS NOT MET")
        if not all_factors_pass:
            print("   ❌ Some factors below ≥99% threshold")
        if not all_subsystems_pass:
            print("   ❌ Some subsystems below ≥97% threshold")
        if not overall_pass:
            print("   ❌ Overall accuracy below ≥99% threshold")
        print(f"{'='*70}")
        return False


if __name__ == "__main__":
    try:
        success = test_accuracy_v14_1_0()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
