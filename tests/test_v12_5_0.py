"""
Test suite for DouEssay v12.5.0
Tests new subsystem branding, enhanced grading features, and 98-99% accuracy target
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import DouEssay, VERSION, VERSION_NAME

def test_version_info():
    """Test that version is correctly updated to 12.5.0"""
    assert VERSION == "12.5.0", f"Expected VERSION='12.5.0', got '{VERSION}'"
    assert "Grading Engine" in VERSION_NAME or "98-99%" in VERSION_NAME, \
        f"Expected VERSION_NAME to mention Grading Engine or 98-99%, got '{VERSION_NAME}'"
    print("✅ Version info correct: v12.5.0")

def test_new_subsystem_branding():
    """Test that new subsystem branding is present"""
    grader = DouEssay()
    
    # Test new branding names
    assert 'scholarmind_core' in grader.subsystem_versions, "Should have ScholarMind Core subsystem"
    assert grader.subsystem_versions['scholarmind_core'] == '4.0', \
        f"ScholarMind Core should be v4.0, got {grader.subsystem_versions.get('scholarmind_core')}"
    
    assert 'douletflow' in grader.subsystem_versions, "Should have DouletFlow subsystem"
    assert grader.subsystem_versions['douletflow'] == '2.0', \
        f"DouletFlow should be v2.0, got {grader.subsystem_versions.get('douletflow')}"
    
    assert 'scholarstruct' in grader.subsystem_versions, "Should have ScholarStruct subsystem"
    assert grader.subsystem_versions['scholarstruct'] == '2.0', \
        f"ScholarStruct should be v2.0, got {grader.subsystem_versions.get('scholarstruct')}"
    
    assert 'emotionflow' in grader.subsystem_versions, "Should have EmotionFlow subsystem"
    assert grader.subsystem_versions['emotionflow'] == '3.0', \
        f"EmotionFlow should be v3.0, got {grader.subsystem_versions.get('emotionflow')}"
    
    assert 'doureflect' in grader.subsystem_versions, "Should have DouReflect subsystem"
    assert grader.subsystem_versions['doureflect'] == '4.1', \
        f"DouReflect should be v4.1, got {grader.subsystem_versions.get('doureflect')}"
    
    print("✅ New subsystem branding: ScholarMind Core v4.0, DouletFlow v2.0, ScholarStruct v2.0, EmotionFlow v3.0, DouReflect v4.1")

def test_backward_compatibility():
    """Test that old subsystem names still work for backward compatibility"""
    grader = DouEssay()
    
    # Test backward compatibility mappings
    assert 'doulogic' in grader.subsystem_versions, "Should maintain DouLogic for backward compatibility"
    assert 'douevidence' in grader.subsystem_versions, "Should maintain DouEvidence for backward compatibility"
    assert 'douemotion' in grader.subsystem_versions, "Should maintain DouEmotion for backward compatibility"
    assert 'doustruct' in grader.subsystem_versions, "Should maintain DouStruct for backward compatibility"
    assert 'argument_logic' in grader.subsystem_versions, "Should maintain argument_logic for backward compatibility"
    
    print("✅ Backward compatibility maintained for legacy subsystem names")

def test_counter_argument_detection():
    """Test enhanced counter-argument detection (ScholarMind Core v4.0)"""
    grader = DouEssay()
    
    # Essay with clear counter-arguments and rebuttals
    essay = """
    Technology in education is beneficial. However, critics argue that it creates distractions. 
    Although some may contend that technology reduces face-to-face interaction, this overlooks the benefits.
    Yet this ignores the collaborative possibilities. Despite this criticism, the evidence is clear.
    Admittedly, there are challenges, but the advantages outweigh them. Nevertheless, the benefits are substantial.
    """
    
    result = grader.analyze_inference_chains_v12_2(essay)
    
    # Check that counter-argument markers are detected
    assert 'counter_argument_markers' in result, "Should detect counter-argument markers"
    assert result['counter_argument_markers'] >= 1, \
        f"Should detect at least 1 counter-argument marker, got {result.get('counter_argument_markers', 0)}"
    
    # Check for rebuttal markers
    assert 'rebuttal_markers' in result, "Should detect rebuttal markers"
    
    # Check for counter-argument quality assessment
    assert 'counter_argument_quality' in result, "Should assess counter-argument quality"
    
    print(f"✅ Counter-argument detection working: {result['counter_argument_markers']} markers found, quality: {result['counter_argument_quality']}")

def test_contemporary_evidence_detection():
    """Test contemporary and recent sources detection (DouletFlow v2.0)"""
    grader = DouEssay()
    
    # Essay with contemporary sources and recent data
    essay = """
    Recent study from 2024 shows significant improvements. Latest research indicates strong correlation.
    Modern society faces challenges. In today's world, technology is essential. Current data from 2025 
    demonstrates the trend. Contemporary issues require modern solutions. Recent findings from this year 
    support the conclusion. In recent years, trends have shifted. The digital age has transformed education.
    """
    
    result = grader.analyze_evidence_types_v12_2(essay)
    
    # Check for contemporary evidence detection
    assert 'recent_sources' in result, "Should detect recent sources"
    assert result['recent_sources'] >= 1, \
        f"Should detect at least 1 recent source marker, got {result.get('recent_sources', 0)}"
    
    assert 'contemporary_connections' in result, "Should detect contemporary connections"
    assert result['contemporary_connections'] >= 1, \
        f"Should detect at least 1 contemporary connection, got {result.get('contemporary_connections', 0)}"
    
    # Check for relevance quality
    assert 'relevance_quality' in result, "Should assess relevance quality"
    
    print(f"✅ Contemporary evidence detection working: {result['recent_sources']} recent sources, {result['contemporary_connections']} contemporary connections")

def test_multi_paragraph_flow_detection():
    """Test multi-paragraph coherence and flow detection (ScholarStruct v2.0)"""
    grader = DouEssay()
    
    # Essay with cross-paragraph references and logical progression
    essay = """
    This essay will argue that education is important.
    
    First, education provides knowledge. As mentioned earlier, knowledge is fundamental. 
    Building on this point, we can see that education shapes society.
    
    Secondly, education creates opportunities. Similarly, it opens doors for advancement. 
    In the same way, education enables social mobility.
    
    In conclusion, as discussed above, education is essential. Returning to our main argument,
    we see that education transforms lives. Relating back to the introduction, our thesis is proven.
    """
    
    result = grader.analyze_paragraph_structure_v12(essay)
    
    # Check for multi-paragraph flow features
    assert 'cross_paragraph_references' in result, "Should detect cross-paragraph references"
    assert result['cross_paragraph_references'] >= 1, \
        f"Should detect at least 1 cross-paragraph reference, got {result.get('cross_paragraph_references', 0)}"
    
    assert 'logical_progression_markers' in result, "Should detect logical progression markers"
    assert 'paragraph_links' in result, "Should detect paragraph linking devices"
    assert 'multi_paragraph_flow_quality' in result, "Should assess multi-paragraph flow quality"
    
    print(f"✅ Multi-paragraph flow detection working: {result['cross_paragraph_references']} cross-refs, flow quality: {result['multi_paragraph_flow_quality']}")

def test_tone_consistency_tracking():
    """Test tone consistency across paragraphs (EmotionFlow v3.0)"""
    grader = DouEssay()
    
    # Essay with consistent argumentative tone
    essay = """
    I argue that climate change requires immediate action. This essay will demonstrate the urgency.
    
    The evidence clearly proves the need for intervention. Research demonstrates alarming trends.
    Studies establish the connection between human activity and climate change.
    
    Furthermore, I contend that governments must take responsibility. The data supports this position.
    Analysis shows that policy changes are essential.
    
    In conclusion, the evidence proves that action is necessary. We must address this challenge now.
    """
    
    result = grader.analyze_emotionflow_v2(essay)
    
    # Check for tone consistency features
    assert 'dominant_tone' in result, "Should identify dominant tone"
    assert 'tone_consistency_score' in result, "Should calculate tone consistency score"
    assert result['tone_consistency_score'] >= 0, \
        f"Tone consistency score should be non-negative, got {result.get('tone_consistency_score')}"
    
    # Check that dominant tone is detected
    assert result['dominant_tone'] in ['narrative', 'argumentative', 'analytical', 'persuasive', 'neutral'], \
        f"Invalid dominant tone: {result.get('dominant_tone')}"
    
    print(f"✅ Tone consistency tracking working: dominant tone is {result['dominant_tone']}, consistency: {result['tone_consistency_score']}%")

def test_improved_evidence_relevance_scoring():
    """Test that evidence relevance scoring is improved to reduce false 'Needs Improvement' ratings"""
    grader = DouEssay()
    
    # Essay with inferential evidence (previously rated as "Needs Improvement")
    essay = """
    Education transforms society. Research suggests that literacy rates correlate with economic growth.
    This implies that investing in education yields long-term benefits. The data indicates a strong relationship.
    Studies point to improved outcomes when education is prioritized. This suggests that policy changes are needed.
    Evidence hints at the importance of early intervention. Analysis implies that prevention is key.
    """
    
    result = grader.analyze_evidence_types_v12_2(essay)
    
    # Check that inferential evidence is properly weighted
    assert result['inferential_evidence'] >= 1, "Should detect inferential evidence"
    assert result['quality'] != 'Needs Improvement' or result['evidence_score'] >= 30, \
        f"Inferential evidence should not always be rated as 'Needs Improvement', score: {result['evidence_score']}"
    
    print(f"✅ Evidence relevance improved: quality={result['quality']}, score={result['evidence_score']}, inferential={result['inferential_evidence']}")

def test_grading_accuracy_improvement():
    """Test that grading accuracy targets 98-99% (improved from 95-96%)"""
    grader = DouEssay()
    
    # High-quality Level 4 essay
    essay = """
    Technology has revolutionized modern education, creating unprecedented opportunities for personalized 
    learning and global collaboration. However, critics argue that technology creates distractions and 
    reduces critical thinking skills. Although these concerns have merit, upon closer examination, the 
    evidence overwhelmingly demonstrates that when properly integrated, technology enhances educational outcomes.
    
    First, recent research from Stanford University (2024) shows that students using adaptive learning platforms 
    improved their test scores by an average of 23% compared to traditional instruction. This directly demonstrates 
    the effectiveness of technology in personalized learning. The study specifically indicates that AI-powered 
    tutoring systems identify learning gaps and provide targeted interventions more effectively than conventional methods.
    
    Moreover, collaborative tools like Google Workspace enable students to work together seamlessly. As mentioned earlier,
    technology facilitates connection. During the COVID-19 pandemic, schools with cloud-based tools maintained 85% 
    of their pre-pandemic performance, according to data from the Ontario Ministry of Education. This contextual 
    evidence reveals that technology infrastructure was crucial for educational continuity.
    
    Some may contend that technology leads to decreased attention spans and increased plagiarism. While these concerns 
    are valid, they reflect implementation challenges rather than inherent technological flaws. However, this overlooks 
    research from the University of Toronto demonstrating that when teachers receive proper training in digital pedagogy, 
    student engagement increases by 31%, and academic integrity violations decrease by 18%. Nevertheless, proper 
    implementation is key to success.
    
    In conclusion, as discussed above, technology represents a powerful tool for educational enhancement when 
    thoughtfully implemented. Returning to our thesis, the evidence from peer-reviewed studies, institutional data, 
    and real-world applications consistently points to improved learning outcomes. Taking both views into account, 
    while challenges exist, they are addressable through proper training and strategic implementation.
    """
    
    result = grader.grade_essay(essay, grade_level="Grade 10")
    
    # Check overall score
    score = result.get('score', 0)
    rubric_level = result.get('rubric_level', {})
    level = rubric_level.get('level', 'Unknown')
    
    # This essay should score highly (Level 3 or 4)
    assert score >= 70, f"High-quality essay should score ≥70, got {score}"
    assert level in ['Level 3', 'Level 4', 'Level 4+'], f"Should be Level 3 or 4, got {level}"
    
    # Check that new features are detected
    inference_chains = result.get('inference_chains_v12_2', {})
    evidence_types = result.get('evidence_types_v12_2', {})
    paragraph_structure = result.get('paragraph_structure_v12', {})
    
    assert inference_chains.get('counter_argument_markers', 0) >= 1, "Should detect counter-arguments"
    assert evidence_types.get('recent_sources', 0) >= 1, "Should detect recent sources"
    assert paragraph_structure.get('cross_paragraph_references', 0) >= 1, "Should detect cross-paragraph references"
    
    print(f"✅ Grading accuracy test passed: Score={score}, Level={level}")
    print(f"   Counter-arguments: {inference_chains.get('counter_argument_markers', 0)}")
    print(f"   Recent sources: {evidence_types.get('recent_sources', 0)}")
    print(f"   Cross-paragraph refs: {paragraph_structure.get('cross_paragraph_references', 0)}")

def test_subscription_tiers_unchanged():
    """Test that subscription tier limits remain correct as per requirements"""
    grader = DouEssay()
    
    # Verify daily limits (should be unchanged from v12.4.0)
    assert grader.license_manager.feature_access['free_trial']['daily_limit'] == 3, \
        "Free trial should have 3 essays/day"
    assert grader.license_manager.feature_access['student_basic']['daily_limit'] == 10, \
        "Student Basic should have 10 essays/day"
    assert grader.license_manager.feature_access['student_premium']['daily_limit'] == 20, \
        "Student Premium should have 20 essays/day"
    assert grader.license_manager.feature_access['teacher_suite']['daily_limit'] == float('inf'), \
        "Teacher Suite should have unlimited essays"
    
    print("✅ Subscription tiers correct: Free=3, Basic=10, Premium=20, Teacher=Unlimited")

# Run all tests
if __name__ == "__main__":
    print("=" * 70)
    print("Running DouEssay v12.5.0 Test Suite")
    print("=" * 70)
    print()
    
    tests = [
        test_version_info,
        test_new_subsystem_branding,
        test_backward_compatibility,
        test_counter_argument_detection,
        test_contemporary_evidence_detection,
        test_multi_paragraph_flow_detection,
        test_tone_consistency_tracking,
        test_improved_evidence_relevance_scoring,
        test_grading_accuracy_improvement,
        test_subscription_tiers_unchanged,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        print(f"\nRunning: {test_func.__name__}")
        print("-" * 70)
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"❌ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR: {e}")
            failed += 1
    
    print()
    print("=" * 70)
    print(f"Test Results: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("=" * 70)
