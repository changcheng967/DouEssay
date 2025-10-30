import gradio as gr
import re
import language_tool_python
from typing import Dict, List, Tuple
import random
import nltk
import sys
import os
from datetime import datetime, timedelta
import supabase
from supabase import create_client

class LicenseManager:
    def __init__(self):
        self.supabase_url = os.environ.get('SUPABASE_URL')
        self.supabase_key = os.environ.get('SUPABASE_KEY')
        self.client = create_client(self.supabase_url, self.supabase_key)
        
    def validate_license(self, license_key: str) -> Dict:
        try:
            response = self.client.table('licenses').select('*').eq('license_key', license_key).execute()
            if not response.data:
                return {'valid': False, 'message': 'Invalid license key'}
            
            license_data = response.data[0]
            
            if datetime.now() > datetime.fromisoformat(license_data['expires_at']):
                return {'valid': False, 'message': 'License expired'}
            
            if not license_data['is_active']:
                return {'valid': False, 'message': 'License deactivated'}
            
            usage_response = self.client.table('usage').select('*').eq('license_key', license_key).eq('usage_date', datetime.now().date().isoformat()).execute()
            
            daily_usage = 0
            if usage_response.data:
                daily_usage = usage_response.data[0]['usage_count']
            
            limits = {
                'free': 5,
                'plus': 100,
                'premium': 1000,
                'unlimited': float('inf')
            }
            
            user_type = license_data['user_type']
            if daily_usage >= limits[user_type]:
                return {'valid': False, 'message': f'Daily usage limit reached for {user_type} user'}
            
            return {
                'valid': True,
                'user_type': user_type,
                'daily_usage': daily_usage,
                'daily_limit': limits[user_type]
            }
            
        except Exception as e:
            return {'valid': False, 'message': f'License validation error: {str(e)}'}
    
    def increment_usage(self, license_key: str) -> bool:
        try:
            today = datetime.now().date().isoformat()
            usage_response = self.client.table('usage').select('*').eq('license_key', license_key).eq('usage_date', today).execute()
            
            if usage_response.data:
                current_count = usage_response.data[0]['usage_count']
                self.client.table('usage').update({'usage_count': current_count + 1}).eq('license_key', license_key).eq('usage_date', today).execute()
            else:
                self.client.table('usage').insert({
                    'license_key': license_key,
                    'usage_date': today,
                    'usage_count': 1
                }).execute()
            
            return True
        except Exception as e:
            print(f"Error incrementing usage: {e}")
            return False

class DouEssay:
    def __init__(self):
        self.setup_nltk()
        self.setup_grammar_tool()
        self.setup_semantic_analyzers()
        self.setup_feedback_templates()
        self.license_manager = LicenseManager()
    
    def setup_nltk(self):
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('punkt_tab', quiet=True)
        except:
            pass

    def setup_grammar_tool(self):
        try:
            self.grammar_tool = language_tool_python.LanguageTool('en-US')
            self.grammar_enabled = True
        except:
            self.grammar_enabled = False

    def setup_semantic_analyzers(self):
        # v6.0.0: Enhanced with originality and argument strength detection
        self.thesis_keywords = [
            'important', 'essential', 'crucial', 'significant', 'key', 'vital',
            'necessary', 'valuable', 'beneficial', 'should', 'must', 'need to',
            'critical', 'plays a role', 'contributes to', 'impacts', 'affects',
            'influences', 'matters because', 'is important because', 'fundamental',
            'paramount', 'indispensable', 'integral', 'pivotal'
        ]
        
        # v6.0.0: Enhanced argument strength indicators
        self.argument_strength_indicators = [
            'argue that', 'contend that', 'assert that', 'maintain that', 'claim that',
            'propose that', 'posit that', 'thesis', 'position', 'stance', 'viewpoint'
        ]
        
        # v6.0.0: Unsupported claim indicators (negative scoring)
        self.unsupported_indicators = [
            'obviously', 'clearly', 'everyone knows', 'it is common knowledge',
            'without a doubt', 'undeniably', 'certainly', 'always', 'never'
        ]
        
        self.example_indicators = [
            'for example', 'for instance', 'such as', 'like when', 'as an example',
            'specifically', 'including', 'case in point', 'to illustrate',
            'as evidence', 'demonstrated by', 'shown by', 'evidenced by',
            'research shows', 'studies indicate', 'according to', 'data reveals'
        ]
        
        self.analysis_indicators = [
            'because', 'this shows', 'therefore', 'as a result', 'thus', 'so',
            'which means', 'this demonstrates', 'consequently', 'this indicates',
            'this suggests', 'for this reason', 'due to', 'owing to', 'leads to',
            'results in', 'implies that', 'suggests that', 'indicates that',
            'reveals that', 'proves that', 'establishes that', 'confirms that'
        ]
        
        # v6.0.0: Enhanced with more nuanced reflection indicators
        self.insight_indicators = [
            'in my experience', 'from my perspective', 'personally', 'i have learned',
            'this taught me', 'i realized', 'what this means for me', 'my understanding',
            'this applies to', 'real-world application', 'in real life', 'this reminds me',
            'similar to how', 'just like when', 'in my opinion', 'from my viewpoint',
            'i believe that', 'i feel that', 'in my view', 'reflecting on', 'looking back',
            'upon reflection', 'i have come to understand', 'my experience shows'
        ]
        
        self.emotional_indicators = [
            'important', 'valuable', 'meaningful', 'significant', 'challenging',
            'difficult', 'rewarding', 'inspiring', 'painful', 'confident', 'proud',
            'grateful', 'frustrating', 'encouraging', 'motivating', 'impactful',
            'transformative', 'profound', 'enlightening', 'eye-opening'
        ]
        
        # v6.0.0: Rhetorical technique detection
        self.rhetorical_indicators = {
            'rhetorical_question': ['?', 'why', 'how', 'what if', 'can we', 'should we'],
            'irony': ['ironically', 'paradoxically', 'surprisingly', 'contrary to'],
            'persuasive': ['must', 'should', 'need to', 'have to', 'ought to', 'it is imperative']
        }



    def setup_feedback_templates(self):
        # v5.0.0: Enhanced feedback templates with specific, actionable guidance
        self.teacher_feedback_templates = {
            'thesis': [
                "Your main idea needs to be stated more explicitly in the introduction. Try: 'This essay will argue that...'",
                "Strengthen your thesis by making a clear, arguable claim. Current thesis is too broad or vague.",
                "Good foundation - now refine your thesis to include your specific position on the topic."
            ],
            'examples': [
                "Add at least 2-3 specific, detailed examples. Include names, dates, situations, or concrete evidence.",
                "Your examples need more depth. For each example, add: who, what, where, when, and why it matters.",
                "Examples are present but generic. Replace general statements with specific real-world instances or personal experiences."
            ],
            'analysis': [
                "After each example, explain WHY it supports your thesis. Add 2-3 sentences of analysis per example.",
                "Connect your examples back to your main argument. Show the 'so what' - why does this example matter?",
                "Deepen your analysis by explaining the cause-effect relationship between your examples and your thesis."
            ],
            'structure': [
                "Use transition words at the start of body paragraphs: 'Furthermore,' 'Additionally,' 'However,' 'Moreover'.",
                "Each paragraph needs: (1) topic sentence, (2) example/evidence, (3) analysis, (4) link back to thesis.",
                "Improve flow by ensuring each paragraph builds on the previous one. Add connecting sentences."
            ],
            'application': [
                "Add a personal experience or real-world example that directly relates to your topic.",
                "Connect your argument to current events, community issues, or your own life. Make it relatable.",
                "Include reflection: What did you learn? How does this apply beyond the classroom?"
            ]
        }
        
        # Inline feedback templates for specific improvements
        self.inline_suggestions = {
            'vague_statement': [
                "💡 How-to: Explain *how* this happens. Add a specific example or personal experience.",
                "💡 Deepen: What does this mean in practice? Provide concrete details.",
                "💡 Connect: How does this support your main argument?"
            ],
            'weak_analysis': [
                "💡 Analysis: Explain *why* this matters. What's the deeper significance?",
                "💡 Connect: Link this back to your thesis statement.",
                "💡 Reflection: What real-world experience illustrates this?"
            ],
            'generic_word': [
                "💡 Vocabulary: Consider using a more specific word here.",
                "💡 Strengthen: This word is generic. Try a more powerful alternative.",
            ],
            'repetitive_start': [
                "💡 Variety: Try starting with a transition word like 'Furthermore,' 'Moreover,' or 'Consequently.'",
                "💡 Flow: Vary your sentence openings for better rhythm."
            ],
            'passive_voice': [
                "💡 Active Voice: Consider rewording this in active voice for more impact.",
                "💡 Clarity: Who is performing this action? Make it explicit."
            ],
            'needs_transition': [
                "💡 Transition: Add a connecting word or phrase to link this to the previous idea.",
                "💡 Flow: Use transitions like 'However,' 'Additionally,' or 'Therefore' for better coherence."
            ]
        }

    def validate_license_and_increment(self, license_key: str) -> Dict:
        validation_result = self.license_manager.validate_license(license_key)
        if not validation_result['valid']:
            return validation_result
        
        if self.license_manager.increment_usage(license_key):
            return validation_result
        else:
            return {'valid': False, 'message': 'Failed to update usage count'}

    def grade_essay(self, essay_text: str, grade_level: str = "Grade 10") -> Dict:
        """
        v6.0.0: Enhanced with grade level support and comprehensive analysis.
        """
        if not essay_text or len(essay_text.strip()) < 100:
            return self.handle_short_essay(essay_text)
        
        stats = self.analyze_basic_stats(essay_text)
        structure = self.analyze_essay_structure_semantic(essay_text)
        content = self.analyze_essay_content_semantic(essay_text)
        grammar = self.check_grammar_errors(essay_text)
        application = self.analyze_personal_application_semantic(essay_text)
        
        # v6.0.0: Pass grade_level to scoring calculation
        score = self.calculate_calibrated_ontario_score(stats, structure, content, grammar, application, grade_level)
        rubric_level = self.get_accurate_rubric_level(score)
        feedback = self.generate_ontario_teacher_feedback(score, rubric_level, stats, structure, content, grammar, application, essay_text)
        corrections = self.get_grammar_corrections(essay_text)
        inline_feedback = self.analyze_inline_feedback(essay_text)
        
        return {
            "score": score,
            "rubric_level": rubric_level,
            "feedback": feedback,
            "corrections": corrections,
            "inline_feedback": inline_feedback,
            "detailed_analysis": {
                "statistics": stats,
                "structure": structure,
                "content": content,
                "grammar": grammar,
                "application": application
            }
        }



    def analyze_essay_themes(self, essay: str) -> Dict:
        """
        v5.0.0: Detect specific topics for generating targeted feedback and reflection prompts.
        """
        text_lower = essay.lower()
        
        # Detect specific topics for targeted feedback
        specific_topics = {
            'technology': any(word in text_lower for word in ['technology', 'computer', 'digital', 'internet', 'software', 'app', 'device', 'tablet', 'smartphone', 'online', 'tech']),
            'sports': any(word in text_lower for word in ['sport', 'athlete', 'team', 'game', 'play', 'physical', 'exercise', 'coach', 'training', 'competition']),
            'arts': any(word in text_lower for word in ['art', 'music', 'paint', 'creative', 'artist', 'cultural', 'performance', 'theater', 'drama', 'dance']),
            'friendship': any(word in text_lower for word in ['friend', 'friendship', 'social', 'companion', 'peer', 'relationship', 'connection']),
            'environment': any(word in text_lower for word in ['environment', 'climate', 'nature', 'pollution', 'sustainability', 'green', 'eco', 'conservation']),
            'reading': any(word in text_lower for word in ['read', 'book', 'literature', 'novel', 'story', 'author', 'writing', 'text'])
        }
        
        # Original generic themes
        themes = {
            'workload': any(word in text_lower for word in ['work', 'homework', 'assignment', 'busy']),
            'tests': any(word in text_lower for word in ['test', 'exam', 'stress', 'nervous']),
            'boring': any(word in text_lower for word in ['boring', 'not interesting', 'pay attention']),
            'difficult': any(word in text_lower for word in ['hard', 'difficult', 'challenging']),
            'school_negative': any(word in text_lower for word in ['not fun', 'don\'t like', 'hate', 'dislike']),
            'specific_topic': next((topic for topic, detected in specific_topics.items() if detected), None),
            'has_specific_topic': any(specific_topics.values())
        }
        return themes















    def analyze_basic_stats(self, text: str) -> Dict:
        words = text.split()
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        avg_sentence_len = len(words) / max(1, len(sentences)) if sentences else 0
        
        return {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "paragraph_count": len(paragraphs),
            "avg_sentence_length": round(avg_sentence_len, 1)
        }

    def analyze_essay_structure_semantic(self, text: str) -> Dict:
        text_lower = text.lower()
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        intro_score = self.assess_introduction_quality_semantic(text, paragraphs)
        conclusion_score = self.assess_conclusion_quality_semantic(text, paragraphs)
        coherence_score = self.assess_paragraph_coherence_semantic(paragraphs)
        
        # v3.0.0: Add explicit paragraph transition evaluation
        transition_analysis = self.assess_paragraph_transitions(paragraphs)
        
        # v3.0.0: Include transitions in structure score
        structure_score = (intro_score + conclusion_score + coherence_score + transition_analysis['score']) / 4 * 10
        
        return {
            "score": min(10, structure_score),
            "has_introduction": intro_score >= 0.6,
            "has_conclusion": conclusion_score >= 0.6,
            "paragraph_count": len(paragraphs),
            "intro_quality": round(intro_score, 2),
            "conclusion_quality": round(conclusion_score, 2),
            "coherence_score": round(coherence_score, 2),
            "transition_analysis": transition_analysis  # v3.0.0: Detailed transition data
        }

    def assess_introduction_quality_semantic(self, text: str, paragraphs: List[str]) -> float:
        if not paragraphs:
            return 0.0
            
        first_para = paragraphs[0].lower()
        score = 0.0
        thesis_indicators = sum(1 for word in self.thesis_keywords if word in first_para)
        if thesis_indicators >= 2:
            score += 0.6
        elif thesis_indicators >= 1:
            score += 0.4
            
        topic_indicators = sum(1 for phrase in ['this essay', 'will discuss', 'i think', 'i believe', 
                                               'the purpose', 'topic', 'subject'] if phrase in first_para)
        if topic_indicators >= 1:
            score += 0.3
            
        if len(first_para.split()) > 20:
            score += 0.4
        elif len(first_para.split()) > 10:
            score += 0.2
            
        if any(word in first_para for word in ['everyone', 'many', 'often', 'when', 'in today']):
            score += 0.2
            
        return min(1.0, score)

    def assess_conclusion_quality_semantic(self, text: str, paragraphs: List[str]) -> float:
        if not paragraphs:
            return 0.0
            
        last_para = paragraphs[-1].lower()
        score = 0.0
        conclusion_phrases = sum(1 for phrase in ['in conclusion', 'in summary', 'to conclude', 
                                                 'overall', 'finally', 'ultimately'] if phrase in last_para)
        if conclusion_phrases >= 1:
            score += 0.4
            
        summary_indicators = sum(1 for word in ['therefore', 'thus', 'so', 'should', 'must', 
                                               'important', 'key', 'essential'] if word in last_para)
        if summary_indicators >= 2:
            score += 0.4
        elif summary_indicators >= 1:
            score += 0.2
            
        if any(word in last_para for word in ['learn', 'teach', 'show', 'demonstrate', 'understand']):
            score += 0.2
            
        return min(1.0, score)

    def assess_paragraph_coherence_semantic(self, paragraphs: List[str]) -> float:
        if len(paragraphs) <= 1:
            return 0.5
            
        transition_words = ['however', 'therefore', 'furthermore', 'additionally', 
                           'moreover', 'consequently', 'nevertheless', 'thus',
                           'also', 'another', 'first', 'second', 'finally', 'next']
        
        transition_count = 0
        for para in paragraphs:
            para_lower = para.lower()
            transition_count += sum(1 for word in transition_words if word in para_lower)
        
        expected_transitions = max(1, (len(paragraphs) - 1) * 1.5)
        coherence_ratio = min(1.0, transition_count / expected_transitions)
        
        return coherence_ratio

    def analyze_essay_content_semantic(self, text: str) -> Dict:
        text_lower = text.lower()
        thesis_score = self.assess_thesis_presence_semantic(text)
        example_score, example_count = self.assess_examples_quality_semantic(text)
        analysis_score = self.assess_analysis_depth_semantic(text)
        
        # v6.0.0: Enhanced with argument strength, rhetorical techniques, and vocabulary sophistication
        argument_analysis = self.assess_argument_strength(text)
        rhetorical_analysis = self.detect_rhetorical_techniques(text)
        vocab_analysis = self.detect_context_vocabulary(text)
        
        # v6.0.0: Adjusted scoring to include new components
        # Base score from thesis, examples, and analysis
        base_score = (thesis_score + example_score + analysis_score) / 3
        
        # Bonus for argument strength and sophistication
        argument_bonus = argument_analysis['strength_score'] * 0.15
        rhetorical_bonus = rhetorical_analysis['technique_score'] * 0.10
        vocab_bonus = vocab_analysis['sophistication_score'] * 0.10
        
        # Penalty for unsupported claims
        unsupported_penalty = min(0.15, argument_analysis['unsupported_claims'] * 0.05)
        
        content_score = (base_score + argument_bonus + rhetorical_bonus + vocab_bonus - unsupported_penalty) * 10
        
        return {
            "score": min(10, max(0, content_score)),
            "has_thesis": thesis_score >= 0.6,
            "example_count": example_count,
            "analysis_count": int(analysis_score * 5),
            "thesis_quality": round(thesis_score, 2),
            "example_quality": round(example_score, 2),
            "analysis_quality": round(analysis_score, 2),
            # v6.0.0: New metrics
            "argument_strength": argument_analysis,
            "rhetorical_techniques": rhetorical_analysis,
            "vocabulary_sophistication": vocab_analysis
        }

    def assess_thesis_presence_semantic(self, text: str) -> float:
        text_lower = text.lower()
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        if not paragraphs:
            return 0.0
            
        first_para = paragraphs[0].lower()
        score = 0.0
        thesis_indicators = sum(1 for word in self.thesis_keywords if word in first_para)
        if thesis_indicators >= 2:
            score += 0.6
        elif thesis_indicators >= 1:
            score += 0.4
            
        topic_indicators = sum(1 for phrase in ['this essay', 'will discuss', 'i think', 
                                               'i believe', 'the purpose'] if phrase in first_para)
        if topic_indicators >= 1:
            score += 0.3
            
        supporting_evidence = 0
        for para in paragraphs[1:]:
            para_lower = para.lower()
            supporting_evidence += sum(1 for word in self.thesis_keywords if word in para_lower)
        
        if supporting_evidence >= 2:
            score += 0.3
        elif supporting_evidence >= 1:
            score += 0.2
            
        return min(1.0, score)

    def assess_argument_strength(self, text: str) -> Dict:
        """
        v6.0.0: Enhanced argument analysis detecting thesis strength, relevance, and originality.
        Returns detailed metrics about argument quality.
        """
        text_lower = text.lower()
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        if not paragraphs:
            return {
                'strength_score': 0.0,
                'has_clear_position': False,
                'originality_score': 0.0,
                'logical_flow_score': 0.0,
                'unsupported_claims': 0
            }
        
        first_para = paragraphs[0].lower()
        
        # Detect clear argumentative position
        strong_position_count = sum(1 for phrase in self.argument_strength_indicators if phrase in first_para)
        has_clear_position = strong_position_count >= 1
        
        # Detect originality (avoiding clichés and generic statements)
        generic_phrases = ['since the beginning of time', 'throughout history', 'in today\'s society',
                          'in conclusion', 'in summary', 'as we all know', 'it goes without saying']
        generic_count = sum(1 for phrase in generic_phrases if phrase in text_lower)
        originality_score = max(0.0, 1.0 - (generic_count * 0.15))
        
        # Detect unsupported claims (absolute statements without evidence)
        unsupported_count = sum(1 for phrase in self.unsupported_indicators if phrase in text_lower)
        
        # Assess logical flow between examples and analysis
        logical_connectors = ['therefore', 'consequently', 'as a result', 'this shows that',
                             'this demonstrates', 'this proves', 'thus', 'hence', 'accordingly']
        logical_count = sum(1 for phrase in logical_connectors if phrase in text_lower)
        
        # Calculate logical flow score based on essay length
        words = text.split()
        expected_connectors = max(1, len(words) // 100)  # ~1 per 100 words
        logical_flow_score = min(1.0, logical_count / expected_connectors)
        
        # Calculate overall strength score
        position_weight = 0.4 if has_clear_position else 0.0
        originality_weight = originality_score * 0.3
        logical_weight = logical_flow_score * 0.3
        
        strength_score = position_weight + originality_weight + logical_weight
        
        return {
            'strength_score': round(strength_score, 2),
            'has_clear_position': has_clear_position,
            'originality_score': round(originality_score, 2),
            'logical_flow_score': round(logical_flow_score, 2),
            'unsupported_claims': unsupported_count
        }

    def assess_examples_quality_semantic(self, text: str) -> Tuple[float, int]:
        text_lower = text.lower()
        explicit_examples = sum(1 for phrase in self.example_indicators if phrase in text_lower)
        implicit_examples = 0
        example_contexts = ['test', 'game', 'edison', 'invent', 'try', 'attempt', 
                           'experience', 'student', 'teacher', 'school', 'work', 
                           'life', 'society', 'people', 'when', 'where']
        for context in example_contexts:
            if context in text_lower:
                implicit_examples += text_lower.count(context) * 0.3
        
        total_examples = explicit_examples + implicit_examples
        example_quality = 0.0
        if total_examples >= 4:
            example_quality = 1.0
        elif total_examples >= 3:
            example_quality = 0.8
        elif total_examples >= 2:
            example_quality = 0.6
        elif total_examples >= 1:
            example_quality = 0.4
            
        return example_quality, int(total_examples)

    def assess_analysis_depth_semantic(self, text: str) -> float:
        text_lower = text.lower()
        analysis_count = sum(1 for indicator in self.analysis_indicators if indicator in text_lower)
        explanation_quality = 0.0
        if analysis_count >= 4:
            explanation_quality = 1.0
        elif analysis_count >= 3:
            explanation_quality = 0.8
        elif analysis_count >= 2:
            explanation_quality = 0.6
        elif analysis_count >= 1:
            explanation_quality = 0.4
            
        cause_effect = sum(1 for word in ['because', 'therefore', 'thus', 'as a result'] 
                          if word in text_lower)
        if cause_effect >= 2:
            explanation_quality = min(1.0, explanation_quality + 0.2)
            
        return explanation_quality

    def detect_rhetorical_techniques(self, text: str) -> Dict:
        """
        v6.0.0: Detects advanced rhetorical techniques including irony, rhetorical questions,
        and persuasive language.
        """
        text_lower = text.lower()
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        
        # Detect rhetorical questions
        rhetorical_questions = sum(1 for s in sentences if '?' in s and 
                                   any(word in s.lower() for word in self.rhetorical_indicators['rhetorical_question']))
        
        # Detect irony and paradox
        irony_count = sum(1 for phrase in self.rhetorical_indicators['irony'] if phrase in text_lower)
        
        # Detect persuasive language
        persuasive_count = sum(1 for phrase in self.rhetorical_indicators['persuasive'] if phrase in text_lower)
        
        # Calculate sophistication score
        total_techniques = rhetorical_questions + irony_count + persuasive_count
        technique_score = min(1.0, total_techniques / 3)  # Target: 3+ techniques
        
        return {
            'rhetorical_questions': rhetorical_questions,
            'irony_count': irony_count,
            'persuasive_language': persuasive_count,
            'technique_score': round(technique_score, 2),
            'has_advanced_techniques': total_techniques >= 2
        }

    def detect_context_vocabulary(self, text: str) -> Dict:
        """
        v6.0.0: Detects context-specific vocabulary for different subject areas.
        Recognizes scientific, literary, historical, and technical terms.
        """
        text_lower = text.lower()
        words = text_lower.split()
        
        # Scientific vocabulary
        scientific_terms = ['hypothesis', 'theory', 'experiment', 'data', 'analysis', 'evidence',
                           'research', 'study', 'methodology', 'conclusion', 'variable', 'control',
                           'observe', 'measure', 'quantitative', 'qualitative']
        scientific_count = sum(1 for word in words if any(term in word for term in scientific_terms))
        
        # Literary vocabulary
        literary_terms = ['metaphor', 'simile', 'symbolism', 'theme', 'character', 'plot',
                         'narrative', 'author', 'protagonist', 'antagonist', 'imagery', 'tone',
                         'mood', 'irony', 'foreshadowing', 'conflict']
        literary_count = sum(1 for word in words if any(term in word for term in literary_terms))
        
        # Historical vocabulary
        historical_terms = ['era', 'period', 'century', 'revolution', 'movement', 'civilization',
                           'dynasty', 'empire', 'war', 'treaty', 'reform', 'industrial', 'renaissance']
        historical_count = sum(1 for word in words if any(term in word for term in historical_terms))
        
        # Technical/Academic vocabulary
        academic_terms = ['furthermore', 'nevertheless', 'consequently', 'moreover', 'alternatively',
                         'specifically', 'particularly', 'fundamentally', 'essentially', 'significantly']
        academic_count = sum(1 for word in words if any(term in word for term in academic_terms))
        
        total_specialized = scientific_count + literary_count + historical_count + academic_count
        vocabulary_sophistication = min(1.0, total_specialized / max(1, len(words) / 20))  # ~5% specialized
        
        return {
            'scientific_terms': scientific_count,
            'literary_terms': literary_count,
            'historical_terms': historical_count,
            'academic_terms': academic_count,
            'total_specialized': total_specialized,
            'sophistication_score': round(vocabulary_sophistication, 2)
        }

    def analyze_personal_application_semantic(self, text: str) -> Dict:
        text_lower = text.lower()
        insight_score = self.assess_personal_insight_semantic(text)
        real_world_score = self.assess_real_world_connections_semantic(text)
        lexical_score = self.assess_lexical_diversity_semantic(text)
        reflection_score = self.assess_reflection_depth(text)  # v3.0.0: New reflection detection
        
        # v4.0.0: Include reflection in scoring (normalized to 10-point scale)
        application_score = (insight_score + real_world_score + lexical_score + reflection_score) / 4 * 10
        
        return {
            "score": min(10, application_score),
            "insight_score": round(insight_score, 2),
            "real_world_score": round(real_world_score, 2),
            "lexical_score": round(lexical_score, 2),
            "reflection_score": round(reflection_score * 10, 1)  # v4.0.0: Normalized to 10-point scale
        }

    def assess_personal_insight_semantic(self, text: str) -> float:
        text_lower = text.lower()
        insight_count = sum(1 for indicator in self.insight_indicators if indicator in text_lower)
        emotional_count = sum(1 for word in self.emotional_indicators if word in text_lower)
        total_insight = insight_count + (emotional_count * 0.5)
        
        if total_insight >= 3:
            return 1.0
        elif total_insight >= 2:
            return 0.8
        elif total_insight >= 1:
            return 0.6
        else:
            return 0.4

    def assess_real_world_connections_semantic(self, text: str) -> float:
        text_lower = text.lower()
        real_world_indicators = sum(1 for word in ['real life', 'real world', 'society', 
                                                  'everyday', 'experience', 'actual', 'today'] 
                                  if word in text_lower)
        specific_contexts = sum(1 for word in ['test', 'game', 'edison', 'invent', 
                                              'school', 'work', 'life', 'world'] if word in text_lower)
        total_connections = real_world_indicators + (specific_contexts * 0.5)
        
        if total_connections >= 4:
            return 1.0
        elif total_connections >= 3:
            return 0.8
        elif total_connections >= 2:
            return 0.6
        elif total_connections >= 1:
            return 0.4
        else:
            return 0.3

    def assess_lexical_diversity_semantic(self, text: str) -> float:
        words = text.lower().split()
        if not words:
            return 0.0
            
        unique_words = set(words)
        lexical_diversity = len(unique_words) / len(words)
        sophisticated_words = sum(1 for word in words if len(word) > 7 and word.isalpha())
        sophistication_ratio = sophisticated_words / len(words)
        combined_score = (lexical_diversity * 0.6) + (sophistication_ratio * 0.4)
        
        return min(1.0, combined_score)
    
    def assess_reflection_depth(self, text: str) -> float:
        """
        v3.0.0: Assess reflection depth through personal pronouns, causal terms, and evaluative phrases.
        Scores reflection quality separately to encourage critical thinking.
        """
        text_lower = text.lower()
        
        # Personal pronouns indicating reflection
        personal_pronouns = ['i', 'my', 'me', 'myself', 'we', 'our', 'us']
        pronoun_count = sum(text_lower.count(f' {pronoun} ') for pronoun in personal_pronouns)
        
        # Causal terms showing deeper thinking
        causal_terms = [
            'because', 'since', 'as a result', 'therefore', 'thus', 'consequently',
            'due to', 'owing to', 'leads to', 'results in', 'causes', 'affects',
            'influences', 'impacts', 'for this reason', 'this is why'
        ]
        causal_count = sum(1 for term in causal_terms if term in text_lower)
        
        # Evaluative phrases showing critical analysis
        evaluative_phrases = [
            'i believe', 'i think', 'in my opinion', 'from my perspective',
            'i realized', 'i learned', 'this taught me', 'i discovered',
            'what i found', 'my understanding', 'i came to understand',
            'this made me realize', 'i now see', 'looking back', 'reflecting on'
        ]
        evaluative_count = sum(1 for phrase in evaluative_phrases if phrase in text_lower)
        
        # Depth indicators showing sophisticated reflection
        depth_indicators = [
            'complex', 'nuanced', 'multifaceted', 'paradox', 'tension',
            'balance', 'perspective', 'lens', 'framework', 'context',
            'implications', 'significance', 'underlying', 'fundamental'
        ]
        depth_count = sum(1 for indicator in depth_indicators if indicator in text_lower)
        
        # Calculate reflection score (normalized to 0-1 scale)
        pronoun_score = min(1.0, pronoun_count / 8)  # Target ~8 personal references
        causal_score = min(1.0, causal_count / 3)    # Target ~3 causal connections
        evaluative_score = min(1.0, evaluative_count / 2)  # Target ~2 evaluative phrases
        depth_score = min(1.0, depth_count / 2)      # Target ~2 depth indicators
        
        # Weighted combination emphasizing evaluation and depth
        total_score = (
            pronoun_score * 0.2 +
            causal_score * 0.25 +
            evaluative_score * 0.3 +
            depth_score * 0.25
        )
        
        return min(1.0, total_score)
    
    def assess_paragraph_transitions(self, paragraphs: List[str]) -> Dict:
        """
        v3.0.0: Explicitly evaluate paragraph transitions and coherence.
        Provides detailed guidance on transition quality.
        """
        if len(paragraphs) <= 1:
            return {
                'score': 0.5,
                'transition_count': 0,
                'quality': 'Limited',
                'suggestions': ['Add more paragraphs to structure your essay effectively.']
            }
        
        # Advanced transition words categorized by function
        transition_categories = {
            'addition': ['furthermore', 'moreover', 'additionally', 'in addition', 'also', 'besides'],
            'contrast': ['however', 'nevertheless', 'conversely', 'on the other hand', 'in contrast', 'yet'],
            'cause_effect': ['therefore', 'thus', 'consequently', 'as a result', 'hence', 'accordingly'],
            'example': ['for example', 'for instance', 'specifically', 'to illustrate', 'namely'],
            'sequence': ['first', 'second', 'finally', 'next', 'then', 'subsequently'],
            'emphasis': ['indeed', 'in fact', 'certainly', 'notably', 'particularly'],
            'summary': ['in conclusion', 'to summarize', 'overall', 'in sum', 'ultimately']
        }
        
        transition_usage = {cat: 0 for cat in transition_categories}
        total_transitions = 0
        
        # Check each paragraph for transitions
        for i, para in enumerate(paragraphs):
            if i == 0:  # Skip intro
                continue
            para_lower = para.lower()
            for category, words in transition_categories.items():
                for word in words:
                    if para_lower.startswith(word) or f'. {word}' in para_lower:
                        transition_usage[category] += 1
                        total_transitions += 1
                        break  # Count once per paragraph per category
        
        # Calculate expected transitions (at least one per body paragraph)
        expected_transitions = max(1, len(paragraphs) - 1)
        transition_ratio = min(1.0, total_transitions / expected_transitions)
        
        # Evaluate variety (using different types of transitions)
        variety_score = len([v for v in transition_usage.values() if v > 0]) / len(transition_categories)
        
        # Combined score
        score = (transition_ratio * 0.6 + variety_score * 0.4)
        
        suggestions = []
        if transition_ratio < 0.5:
            suggestions.append('Add transition words at the start of paragraphs to improve flow.')
        if variety_score < 0.3:
            suggestions.append('Use a greater variety of transition types (contrast, cause-effect, examples).')
        if not suggestions:
            suggestions.append('Good use of transitions! Consider refining for even smoother flow.')
        
        quality = 'Excellent' if score >= 0.8 else 'Good' if score >= 0.6 else 'Fair' if score >= 0.4 else 'Needs Improvement'
        
        return {
            'score': round(score, 2),
            'transition_count': total_transitions,
            'variety': round(variety_score, 2),
            'quality': quality,
            'suggestions': suggestions,
            'usage_by_type': transition_usage
        }
    


    def check_grammar_errors(self, text: str) -> Dict:
        if not self.grammar_enabled:
            return {"error_count": 0, "score": 8}
            
        try:
            matches = self.grammar_tool.check(text)
            error_count = len(matches)
            if error_count == 0:
                grammar_score = 10
            elif error_count <= 2:
                grammar_score = 9
            elif error_count <= 5:
                grammar_score = 8
            elif error_count <= 8:
                grammar_score = 7
            else:
                grammar_score = 6
                
            return {
                "error_count": error_count,
                "score": grammar_score
            }
        except:
            return {"error_count": 0, "score": 8}

    def get_grammar_corrections(self, text: str) -> List[Dict]:
        if not self.grammar_enabled:
            return []
            
        try:
            matches = self.grammar_tool.check(text)
            corrections = []
            for match in matches[:10]:
                if match.replacements:
                    correction = {
                        'offset': match.offset,
                        'length': match.errorLength,
                        'original': text[match.offset:match.offset + match.errorLength],
                        'suggestion': match.replacements[0],
                        'message': match.message
                    }
                    corrections.append(correction)
            return corrections
        except:
            return []

    def calculate_calibrated_ontario_score(self, stats: Dict, structure: Dict, content: Dict, 
                                         grammar: Dict, application: Dict, grade_level: str = "Grade 10") -> int:
        # v6.0.0: Enhanced with dynamic calibration based on length, complexity, and grade level
        # Focus on content depth, structural organization, real-world application, and mechanics
        weights = {
            'content': 0.35,      # Content & Analysis (thesis, examples, argument depth)
            'structure': 0.25,    # Structure & Organization (coherence, transitions, flow)
            'application': 0.25,  # Application & Insight (real-world connections, reflection)
            'grammar': 0.15       # Grammar & Mechanics (accuracy, sentence variety)
        }
        
        base_score = (
            content['score'] * weights['content'] * 10 +
            structure['score'] * weights['structure'] * 10 +
            grammar['score'] * weights['grammar'] * 10 +
            application['score'] * weights['application'] * 10
        )
        
        # v6.0.0: Dynamic length calibration based on word count with finer granularity
        word_count = stats['word_count']
        if word_count >= 450:
            length_bonus = 5  # Exceptional depth
        elif word_count >= 380:
            length_bonus = 4
        elif word_count >= 320:
            length_bonus = 3
        elif word_count >= 280:
            length_bonus = 2
        elif word_count >= 240:
            length_bonus = 1
        elif word_count >= 200:
            length_bonus = 0
        else:
            length_bonus = -2  # Too short
        
        # v6.0.0: Complexity bonus based on sophistication metrics
        complexity_bonus = 0
        if 'vocabulary_sophistication' in content:
            vocab_score = content['vocabulary_sophistication'].get('sophistication_score', 0)
            complexity_bonus += vocab_score * 2  # Up to +2 points
        
        if 'rhetorical_techniques' in content:
            if content['rhetorical_techniques'].get('has_advanced_techniques', False):
                complexity_bonus += 1.5
        
        if 'argument_strength' in content:
            arg_strength = content['argument_strength'].get('strength_score', 0)
            complexity_bonus += arg_strength * 2  # Up to +2 points
        
        # v6.0.0: Grade level calibration (expectations increase with grade)
        grade_multiplier = 1.0
        if grade_level == "Grade 12":
            grade_multiplier = 1.05  # Higher expectations
        elif grade_level == "Grade 11":
            grade_multiplier = 1.02
        elif grade_level == "Grade 10":
            grade_multiplier = 1.0
        elif grade_level == "Grade 9":
            grade_multiplier = 0.98  # Slightly more lenient
        
        # v6.0.0: Apply all calibrations
        final_score = (base_score + length_bonus + complexity_bonus) * grade_multiplier
        
        # v6.0.0: Quality bonus for well-structured essays with strong fundamentals
        if content.get('has_thesis', False) and structure.get('has_introduction', False) and grammar['score'] >= 8:
            final_score += 2
        
        # v6.0.0: Additional bonus for essays demonstrating mastery
        if content.get('argument_strength', {}).get('has_clear_position', False) and \
           content.get('argument_strength', {}).get('unsupported_claims', 0) == 0:
            final_score += 1.5
            
        return max(65, min(98, int(final_score)))

    def get_accurate_rubric_level(self, score: int) -> Dict:
        if score >= 85:
            return {"level": "Level 4", "description": "Excellent - Exceeds Standards"}
        elif score >= 75:
            return {"level": "Level 3", "description": "Good - Meets Standards"}
        elif score >= 70:
            return {"level": "Level 2+", "description": "Developing - Approaching Standards"}
        elif score >= 65:
            return {"level": "Level 2", "description": "Developing - Basic Standards"}
        elif score >= 60:
            return {"level": "Level 1", "description": "Limited - Below Standards"}
        else:
            return {"level": "R", "description": "Remedial - Needs Significant Improvement"}

    def generate_ontario_teacher_feedback(self, score: int, rubric: Dict, stats: Dict, 
                                        structure: Dict, content: Dict, grammar: Dict, 
                                        application: Dict, essay_text: str) -> List[str]:
        feedback = []
        feedback.append(f"Overall Score: {score}/100")
        feedback.append(f"Ontario Level: {rubric['level']} - {rubric['description']}")
        
        # v6.0.0: Add advanced analysis summary
        if 'argument_strength' in content:
            arg_strength = content['argument_strength']
            feedback.append("")
            feedback.append("🎯 ARGUMENT ANALYSIS (v6.0.0):")
            feedback.append(f"  • Argument Strength: {arg_strength.get('strength_score', 0)*100:.0f}%")
            feedback.append(f"  • Clear Position: {'Yes ✓' if arg_strength.get('has_clear_position', False) else 'Needs Work'}")
            feedback.append(f"  • Originality: {arg_strength.get('originality_score', 0)*100:.0f}%")
            feedback.append(f"  • Logical Flow: {arg_strength.get('logical_flow_score', 0)*100:.0f}%")
            if arg_strength.get('unsupported_claims', 0) > 0:
                feedback.append(f"  ⚠️  Unsupported Claims Detected: {arg_strength.get('unsupported_claims', 0)}")
        
        feedback.append("")
        
        strengths = self.identify_strengths_semantic(structure, content, grammar, application, stats)
        improvements = self.identify_improvements_semantic(structure, content, grammar, application, stats, essay_text)
        
        feedback.append("✅ STRENGTHS:")
        for strength in strengths:
            feedback.append(f"• {strength}")
        if not strengths:
            feedback.append("• Building a solid foundation for essay writing")
            
        feedback.append("")
        feedback.append("📝 AREAS TO IMPROVE:")
        for improvement in improvements:
            feedback.append(f"• {improvement}")
            
        feedback.append("")
        feedback.append("👨‍🏫 TEACHER'S VOICE:")
        teacher_comments = self.generate_teacher_comments_semantic(structure, content, application, essay_text)
        for comment in teacher_comments:
            feedback.append(f"  {comment}")
        
        # v4.0.1: Add essay-specific self-reflection prompts
        feedback.append("")
        feedback.append("💭 SELF-REFLECTION PROMPTS (Optional):")
        reflection_prompts = self.generate_reflection_prompts(score, content, application, essay_text)
        for prompt in reflection_prompts:
            feedback.append(f"  • {prompt}")
            
        feedback.append("")
        feedback.append("🎯 NEXT STEPS:")
        next_steps = self.get_ontario_next_steps(score, structure, content, application)
        for step in next_steps:
            feedback.append(f"• {step}")
            
        return feedback
    
    def generate_reflection_prompts(self, score: int, content: Dict, application: Dict, essay_text: str = "") -> List[str]:
        """
        v4.0.1: Enhanced to generate essay-specific reflection prompts tied to actual content.
        Analyzes essay to create personalized prompts instead of generic ones.
        """
        prompts = []
        
        # v4.0.1: Detect essay topic for specific prompts
        essay_lower = essay_text.lower()
        specific_prompts_added = False
        
        # v6.0.0: Enhanced topic-specific prompts with real-world connections
        # Technology-specific prompts
        if any(word in essay_lower for word in ['technology', 'computer', 'digital', 'internet', 'app', 'software', 'online']):
            if content.get('analysis_quality', 0) < 0.7:
                prompts.append("How has technology personally changed the way you learn? Can you describe a specific instance?")
                prompts.append("Think of a time when technology either helped or hindered your learning. What happened and what did you learn?")
            else:
                prompts.append("What aspect of technology in education do you find most transformative, and why?")
                prompts.append("How might emerging technologies (AI, VR, etc.) reshape education in the next 5 years? What excites or concerns you?")
            specific_prompts_added = True
        
        # Sports-specific prompts
        elif any(word in essay_lower for word in ['sport', 'athlete', 'team', 'game', 'physical', 'exercise', 'competition']):
            prompts.append("What personal experience with sports or teamwork shaped your perspective on this topic?")
            prompts.append("Describe a moment in sports where you learned something applicable to life beyond the game. What was the lesson?")
            prompts.append("How do the skills from sports (teamwork, perseverance, strategy) apply to your academic or career goals?")
            specific_prompts_added = True
        
        # Arts-specific prompts
        elif any(word in essay_lower for word in ['art', 'music', 'creative', 'paint', 'performance', 'theater', 'dance']):
            prompts.append("How has your own experience with the arts influenced your understanding of creativity in education?")
            prompts.append("What artistic work (yours or someone else's) deeply affected you? Why did it resonate?")
            prompts.append("How do creative skills learned through arts transfer to other areas of your life or studies?")
            specific_prompts_added = True
        
        # Reading/Literature-specific prompts
        elif any(word in essay_lower for word in ['read', 'book', 'literature', 'story', 'author', 'novel', 'text']):
            prompts.append("What book or reading experience had the greatest impact on your thinking about this topic?")
            prompts.append("Describe a character or story that changed your perspective. What specific moment or quote stuck with you?")
            prompts.append("How has your reading outside of school shaped your worldview or academic interests?")
            specific_prompts_added = True
        
        # v6.0.0: Environment/Sustainability prompts
        elif any(word in essay_lower for word in ['environment', 'climate', 'sustainability', 'nature', 'pollution', 'green']):
            prompts.append("What environmental issue in your community concerns you most? What could you personally do about it?")
            prompts.append("How do your daily choices impact the environment? What changes have you made or could you make?")
            specific_prompts_added = True
        
        # v6.0.0: Social issues prompts
        elif any(word in essay_lower for word in ['society', 'community', 'culture', 'diversity', 'justice', 'equity']):
            prompts.append("What experience has shaped your understanding of this social issue? How has it influenced your perspective?")
            prompts.append("How can young people like you contribute to positive change in your community regarding this issue?")
            specific_prompts_added = True
        
        # v4.0.1: Content-based prompts with more specificity
        if content.get('analysis_quality', 0) < 0.7:
            if not specific_prompts_added:
                prompts.append("Which example in your essay could be developed further with real-world connections? What details would you add?")
        
        if application.get('reflection_score', 0) < 0.6:
            prompts.append("Looking at your main argument, what personal experience directly relates to it that you haven't mentioned?")
        
        # Score-based prompts with actionable guidance
        if score < 75:
            prompts.append("What was the most challenging part of writing this essay? What specific strategy would help you next time?")
            if not specific_prompts_added:
                prompts.append("If you could strengthen one paragraph with a concrete example, which would it be and what would you add?")
        else:
            prompts.append("What specific technique in this essay worked best? How could you use it in other writing?")
            prompts.append("How could you take your strongest paragraph and make it even more compelling?")
        
        # Universal prompts
        prompts.append("After reading the feedback, what is one specific change you will make in your next draft?")
        
        return prompts[:3]  # Return top 3 most relevant prompts

    def identify_strengths_semantic(self, structure: Dict, content: Dict, grammar: Dict, 
                                  application: Dict, stats: Dict) -> List[str]:
        strengths = []
        
        if content['thesis_quality'] >= 0.7:
            strengths.append("Clear main idea and thesis development")
        elif content['thesis_quality'] >= 0.5:
            strengths.append("Good attempt at establishing a main idea")
            
        if content['example_count'] >= 3:
            strengths.append("Strong use of supporting examples")
        elif content['example_count'] >= 2:
            strengths.append("Good examples to support your points")
            
        if structure['intro_quality'] >= 0.7:
            strengths.append("Effective introduction that engages the reader")
        if structure['conclusion_quality'] >= 0.7:
            strengths.append("Strong conclusion that summarizes key points")
            
        if grammar['score'] >= 9:
            strengths.append("Excellent grammar and sentence structure")
        elif grammar['score'] >= 8:
            strengths.append("Good control of grammar and mechanics")
            
        if application['score'] >= 8:
            strengths.append("Strong personal insight and real-world connections")
        elif application['score'] >= 6:
            strengths.append("Good attempt at personal application")
            
        if stats['word_count'] >= 300:
            strengths.append("Appropriate length for thorough development")
            
        return strengths

    def analyze_paragraph_structure(self, essay_text: str) -> Dict:
        """
        v6.0.0: Analyzes each paragraph for structure issues including missing topic sentences,
        weak examples, and analysis gaps.
        """
        paragraphs = [p.strip() for p in essay_text.split('\n\n') if p.strip()]
        paragraph_issues = []
        
        for i, para in enumerate(paragraphs):
            para_lower = para.lower()
            sentences = [s.strip() for s in re.split(r'[.!?]+', para) if s.strip()]
            
            issues = []
            
            # Check for topic sentence (first sentence should introduce paragraph theme)
            if i > 0 and i < len(paragraphs) - 1:  # Body paragraphs
                first_sentence = sentences[0].lower() if sentences else ""
                has_topic_sentence = any(word in first_sentence for word in 
                    ['first', 'second', 'another', 'furthermore', 'moreover', 'additionally', 
                     'however', 'one reason', 'one example', 'most importantly'])
                
                if not has_topic_sentence and len(sentences) > 2:
                    issues.append("Missing clear topic sentence")
            
            # Check for examples
            has_examples = any(indicator in para_lower for indicator in self.example_indicators)
            if i > 0 and i < len(paragraphs) - 1 and not has_examples and len(sentences) > 2:
                issues.append("Needs specific examples or evidence")
            
            # Check for analysis
            has_analysis = any(indicator in para_lower for indicator in self.analysis_indicators)
            if i > 0 and i < len(paragraphs) - 1 and has_examples and not has_analysis:
                issues.append("Example provided but lacks analysis explaining its significance")
            
            # Check paragraph length
            word_count = len(para.split())
            if i > 0 and i < len(paragraphs) - 1:  # Body paragraphs
                if word_count < 40:
                    issues.append("Too brief - needs development")
                elif word_count > 150:
                    issues.append("Consider splitting into two paragraphs for clarity")
            
            if issues:
                paragraph_issues.append({
                    'paragraph_num': i + 1,
                    'issues': issues,
                    'word_count': word_count
                })
        
        return {
            'total_paragraphs': len(paragraphs),
            'paragraphs_with_issues': len(paragraph_issues),
            'issues': paragraph_issues
        }

    def identify_improvements_semantic(self, structure: Dict, content: Dict, grammar: Dict, 
                                    application: Dict, stats: Dict, essay_text: str) -> List[str]:
        improvements = []
        
        # v6.0.0: Add paragraph-level guidance
        para_analysis = self.analyze_paragraph_structure(essay_text)
        if para_analysis['paragraphs_with_issues'] > 0:
            for para_issue in para_analysis['issues'][:2]:  # Show top 2 paragraph issues
                para_num = para_issue['paragraph_num']
                for issue in para_issue['issues']:
                    improvements.append(f"Paragraph {para_num}: {issue}")
        
        if content['thesis_quality'] < 0.6:
            improvements.append("Strengthen your thesis statement in the introduction")
        if content['example_count'] < 2:
            improvements.append("Add more specific examples to support each main point (target: 2-3 per paragraph)")
        if content['analysis_quality'] < 0.6:
            improvements.append("Deepen your analysis by explaining how examples prove your points")
            
        if structure['intro_quality'] < 0.6:
            improvements.append("Work on creating a more engaging introduction with a clear hook")
        if structure['conclusion_quality'] < 0.6:
            improvements.append("Develop a stronger conclusion that reinforces your main idea")
        if structure['coherence_score'] < 0.5:
            improvements.append("Improve transitions between paragraphs for better flow")
            
        if grammar['error_count'] > 3:
            improvements.append(f"Proofread to address {grammar['error_count']} grammar issues")
            
        if application['score'] < 6:
            improvements.append("Add more personal reflection and real-world connections")
            
        if stats['word_count'] < 280:
            improvements.append("Develop your ideas more fully with additional details")
        
        # v6.0.0: Add argument-specific improvements
        if 'argument_strength' in content:
            arg_strength = content['argument_strength']
            if not arg_strength.get('has_clear_position', False):
                improvements.append("State your position more explicitly using phrases like 'I argue that' or 'This essay contends'")
            if arg_strength.get('originality_score', 1.0) < 0.6:
                improvements.append("Avoid generic opening phrases; be more original in your approach")
            if arg_strength.get('unsupported_claims', 0) > 0:
                improvements.append("Support absolute statements (e.g., 'always', 'never') with concrete evidence")
            
        return improvements

    def generate_teacher_comments_semantic(self, structure: Dict, content: Dict, 
                                         application: Dict, essay_text: str) -> List[str]:
        comments = []
        
        if content['example_count'] < 3:
            comments.append("Try adding more specific examples from literature or real life to strengthen your argument")
        if content['analysis_quality'] < 0.7:
            comments.append("Explain why your examples prove your point rather than just listing them")
        if application['score'] < 7:
            comments.append("Connect this topic more explicitly to your own experiences or current events")
        if structure['coherence_score'] < 0.6:
            comments.append("Use transition words to create smoother connections between ideas")
            
        if not comments:
            comments.append("Excellent work! Your essay demonstrates strong understanding and organization.")
            comments.append("Continue developing your analytical skills and personal voice.")
            
        return comments

    def get_ontario_next_steps(self, score: int, structure: Dict, content: Dict, 
                              application: Dict) -> List[str]:
        next_steps = []
        
        if score >= 80:
            next_steps.extend([
                "Focus on more sophisticated vocabulary and complex sentence structures",
                "Develop deeper analytical insights and unique perspectives",
                "Experiment with different organizational patterns"
            ])
        elif score >= 70:
            next_steps.extend([
                "Strengthen thesis development and supporting evidence",
                "Improve paragraph transitions and overall coherence",
                "Add more personal reflection and real-world applications"
            ])
        else:
            next_steps.extend([
                "Practice writing clear thesis statements",
                "Work on including 2-3 specific examples per main point",
                "Focus on basic paragraph structure and organization"
            ])
            
        return next_steps

    def handle_short_essay(self, text: str) -> Dict:
        word_count = len(text.split()) if text else 0
        return {
            "score": max(60, min(75, word_count)),
            "rubric_level": self.get_accurate_rubric_level(max(60, min(75, word_count))),
            "feedback": [
                "Essay is too short for full assessment",
                f"Current length: {word_count} words",
                "Recommended length: 250-500 words for Ontario high school essays",
                "",
                "Please expand your essay with:",
                "- A clear introduction with main idea",
                "- 3-5 developed paragraphs with specific examples",
                "- Analysis explaining how examples support your points",
                "- A conclusion that summarizes your argument"
            ],
            "corrections": [],
            "detailed_analysis": {
                "statistics": {"word_count": word_count},
                "structure": {"score": 5},
                "content": {"score": 5},
                "grammar": {"score": 8},
                "application": {"score": 5}
            },
            "inline_feedback": []
        }

    def detect_word_repetition(self, essay_text: str) -> Dict:
        """
        v6.0.0: Detects overused words and suggests synonyms for variety.
        """
        words = essay_text.lower().split()
        word_freq = {}
        
        # Count significant words (exclude common articles, prepositions)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
                     'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                     'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'}
        
        for word in words:
            clean_word = word.strip('.,!?;:"\'-')
            if len(clean_word) > 3 and clean_word not in stop_words:
                word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
        
        # Identify overused words (appearing more than expected)
        total_words = len([w for w in words if w not in stop_words])
        overused_threshold = max(3, total_words / 50)  # ~2% repetition threshold
        
        overused_words = {word: count for word, count in word_freq.items() 
                         if count >= overused_threshold}
        
        # Sort by frequency
        overused_sorted = sorted(overused_words.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'overused_words': dict(overused_sorted[:5]),  # Top 5 overused words
            'total_unique_words': len(word_freq),
            'repetition_score': 1.0 - (len(overused_words) / max(1, len(word_freq)))
        }

    def analyze_inline_feedback(self, essay_text: str) -> List[Dict]:
        """
        v6.0.0: Enhanced with word repetition detection and advanced style suggestions.
        Prevents overlapping suggestions for the same sentence.
        """
        inline_feedback = []
        sentences = [s.strip() for s in re.split(r'[.!?]+', essay_text) if s.strip()]
        feedback_seen = {}  # v4.0.0: Track feedback per sentence to avoid duplicates
        
        # v6.0.0: Detect word repetition across entire essay
        repetition_analysis = self.detect_word_repetition(essay_text)
        
        for idx, sentence in enumerate(sentences):
            sentence_lower = sentence.lower()
            
            # v4.0.0: Initialize feedback tracking for this sentence
            if idx not in feedback_seen:
                feedback_seen[idx] = set()
            
            # Check for vague statements that need elaboration
            vague_patterns = ['helps', 'useful', 'good', 'bad', 'makes', 'does']
            if any(pattern in sentence_lower for pattern in vague_patterns) and len(sentence.split()) < 15:
                if not any(word in sentence_lower for word in ['because', 'for example', 'such as', 'specifically']):
                    # v4.0.0: Only add if not already flagged for this sentence
                    if 'vague_statement' not in feedback_seen[idx]:
                        inline_feedback.append({
                            'sentence_index': idx,
                            'sentence': sentence,
                            'type': 'vague_statement',
                            'severity': 'yellow',
                            'suggestion': random.choice(self.inline_suggestions['vague_statement'])
                        })
                        feedback_seen[idx].add('vague_statement')
            
            # Check for weak analysis
            if any(word in sentence_lower for word in ['important', 'essential', 'crucial', 'significant']):
                if not any(word in sentence_lower for word in ['because', 'this shows', 'this demonstrates', 'therefore']):
                    # v4.0.0: Avoid duplicate if already flagged as vague
                    if 'weak_analysis' not in feedback_seen[idx] and 'vague_statement' not in feedback_seen[idx]:
                        inline_feedback.append({
                            'sentence_index': idx,
                            'sentence': sentence,
                            'type': 'weak_analysis',
                            'severity': 'yellow',
                            'suggestion': random.choice(self.inline_suggestions['weak_analysis'])
                        })
                        feedback_seen[idx].add('weak_analysis')
            
            # v6.0.0: Check for overused words from essay-wide analysis
            sentence_words = set(sentence_lower.split())
            for overused_word in repetition_analysis['overused_words'].keys():
                if overused_word in sentence_words and 'repetition' not in feedback_seen[idx]:
                    count = repetition_analysis['overused_words'][overused_word]
                    inline_feedback.append({
                        'sentence_index': idx,
                        'sentence': sentence,
                        'type': 'word_repetition',
                        'severity': 'yellow',
                        'suggestion': f"💡 Word Repetition: '{overused_word}' appears {count} times. Consider using synonyms for variety.",
                        'word': overused_word,
                        'count': count
                    })
                    feedback_seen[idx].add('repetition')
                    break  # Only flag once per sentence
            
            # Check for generic words
            generic_words = ['very', 'really', 'a lot', 'many', 'most', 'some', 'things', 'stuff', 'big', 'small']
            found_generic = [
                word for word in generic_words
                if re.search(r'\b' + re.escape(word) + r'\b', sentence_lower)
            ]
            if found_generic and 'generic_word' not in feedback_seen[idx]:
                alternatives = self.get_vocabulary_alternatives(found_generic[0])
                inline_feedback.append({
                    'sentence_index': idx,
                    'sentence': sentence,
                    'type': 'generic_word',
                    'severity': 'yellow',
                    'suggestion': f"💡 Vocabulary: Replace '{found_generic[0]}' with: {', '.join(alternatives)}",
                    'word': found_generic[0],
                    'alternatives': alternatives
                })
                feedback_seen[idx].add('generic_word')
            
            # v6.0.0: Enhanced sentence variety checking
            if idx > 0:
                current_start = sentence.split()[0].lower() if sentence.split() else ''
                prev_start = sentences[idx-1].split()[0].lower() if sentences[idx-1].split() else ''
                
                # Check for repetitive sentence openings
                if current_start == prev_start and current_start in ['the', 'it', 'this', 'they', 'students', 'teachers', 'people', 'in', 'when', 'there']:
                    inline_feedback.append({
                        'sentence_index': idx,
                        'sentence': sentence,
                        'type': 'repetitive_start',
                        'severity': 'yellow',
                        'suggestion': random.choice(self.inline_suggestions['repetitive_start'])
                    })
                
                # v6.0.0: Check for similar sentence lengths (monotonous rhythm)
                current_len = len(sentence.split())
                prev_len = len(sentences[idx-1].split())
                if idx > 1:
                    prev_prev_len = len(sentences[idx-2].split())
                    # If 3 consecutive sentences are similar length, suggest variety
                    if abs(current_len - prev_len) <= 2 and abs(prev_len - prev_prev_len) <= 2 and 'sentence_variety' not in feedback_seen[idx]:
                        inline_feedback.append({
                            'sentence_index': idx,
                            'sentence': sentence,
                            'type': 'monotonous_rhythm',
                            'severity': 'yellow',
                            'suggestion': "💡 Sentence Variety: Vary sentence length for better rhythm. Try mixing short, punchy sentences with longer, complex ones."
                        })
                        feedback_seen[idx].add('sentence_variety')
            
            # Check for passive voice
            passive_indicators = [' is ', ' are ', ' was ', ' were ', ' been ', ' being ']
            if any(indicator in f' {sentence_lower} ' for indicator in passive_indicators):
                if any(word in f' {sentence_lower} ' for word in [' by ', ' done ', ' made ', ' created ']):
                    inline_feedback.append({
                        'sentence_index': idx,
                        'sentence': sentence,
                        'type': 'passive_voice',
                        'severity': 'yellow',
                        'suggestion': random.choice(self.inline_suggestions['passive_voice'])
                    })
        
        # Identify strengths to highlight in green
        for idx, sentence in enumerate(sentences):
            sentence_lower = sentence.lower()
            
            # Strong analytical language
            if any(phrase in sentence_lower for phrase in ['this demonstrates', 'this shows that', 'this illustrates', 
                                                           'for example', 'specifically', 'as evidence', 'research shows']):
                inline_feedback.append({
                    'sentence_index': idx,
                    'sentence': sentence,
                    'type': 'strength',
                    'severity': 'green',
                    'suggestion': '✅ Strong analytical connection! This effectively supports your argument.'
                })
            
            # Good personal insight
            if any(phrase in sentence_lower for phrase in ['in my experience', 'i learned', 'this taught me', 
                                                           'i realized', 'from my perspective']):
                inline_feedback.append({
                    'sentence_index': idx,
                    'sentence': sentence,
                    'type': 'strength',
                    'severity': 'green',
                    'suggestion': '✅ Excellent personal reflection! This adds depth to your essay.'
                })
        
        return inline_feedback

    def get_vocabulary_alternatives(self, word: str) -> List[str]:
        """
        v6.0.0: Enhanced with more sophisticated vocabulary alternatives.
        """
        vocab_map = {
            'very': ['extremely', 'remarkably', 'particularly', 'exceptionally', 'profoundly', 'decidedly'],
            'really': ['genuinely', 'truly', 'certainly', 'indeed', 'authentically', 'undeniably'],
            'a lot': ['numerous', 'substantial', 'considerable', 'extensive', 'abundant', 'copious'],
            'many': ['numerous', 'various', 'multiple', 'countless', 'myriad', 'manifold'],
            'most': ['majority of', 'predominant', 'principal', 'primary', 'preponderant'],
            'some': ['several', 'certain', 'particular', 'specific', 'select', 'designated'],
            'things': ['elements', 'aspects', 'factors', 'components', 'dimensions', 'facets'],
            'stuff': ['material', 'content', 'subject matter', 'information', 'data', 'resources'],
            'big': ['substantial', 'significant', 'considerable', 'extensive', 'monumental', 'profound'],
            'small': ['minimal', 'modest', 'limited', 'negligible', 'marginal', 'inconsequential'],
            'good': ['beneficial', 'advantageous', 'valuable', 'effective', 'constructive', 'favorable'],
            'bad': ['detrimental', 'problematic', 'ineffective', 'counterproductive', 'adverse', 'harmful'],
            'important': ['significant', 'crucial', 'vital', 'essential', 'pivotal', 'paramount'],
            'get': ['obtain', 'acquire', 'attain', 'procure', 'secure', 'gain'],
            'make': ['create', 'construct', 'produce', 'generate', 'develop', 'formulate'],
            'show': ['demonstrate', 'illustrate', 'exhibit', 'reveal', 'display', 'manifest'],
            'use': ['utilize', 'employ', 'apply', 'implement', 'leverage', 'harness']
        }
        return vocab_map.get(word.lower(), ['more specific term'])

    def create_annotated_essay_html(self, essay_text: str, inline_feedback: List[Dict]) -> str:
        """Create HTML version of essay with color-coded inline annotations."""
        sentences = [s.strip() for s in re.split(r'([.!?]+)', essay_text) if s.strip()]
        
        # Create a mapping of sentence index to feedback
        feedback_map = {}
        for feedback in inline_feedback:
            idx = feedback['sentence_index']
            if idx not in feedback_map:
                feedback_map[idx] = []
            feedback_map[idx].append(feedback)
        
        html_parts = ['<div style="font-family: Georgia, serif; line-height: 1.8; font-size: 1.1em;">']
        
        sentence_idx = 0
        for i, part in enumerate(sentences):
            if re.match(r'^[.!?]+$', part):
                html_parts.append(part)
            else:
                # This is a sentence
                color_class = 'normal'
                tooltips = []
                
                if sentence_idx in feedback_map:
                    feedbacks = feedback_map[sentence_idx]
                    # Determine the most important severity
                    severities = [f['severity'] for f in feedbacks]
                    if 'red' in severities:
                        color_class = 'red'
                    elif 'yellow' in severities:
                        color_class = 'yellow'
                    elif 'green' in severities:
                        color_class = 'green'
                    
                    # Collect all suggestions
                    tooltips = [f['suggestion'] for f in feedbacks]
                
                # Apply styling
                if color_class == 'green':
                    style = 'background-color: #d4edda; border-left: 3px solid #28a745; padding: 5px; margin: 2px 0; display: inline-block;'
                elif color_class == 'yellow':
                    style = 'background-color: #fff3cd; border-left: 3px solid #ffc107; padding: 5px; margin: 2px 0; display: inline-block;'
                elif color_class == 'red':
                    style = 'background-color: #f8d7da; border-left: 3px solid #dc3545; padding: 5px; margin: 2px 0; display: inline-block;'
                else:
                    style = 'display: inline;'
                
                if tooltips:
                    tooltip_text = '<br>'.join(tooltips)
                    html_parts.append(
                        f'<span style="{style}" title="{tooltip_text.replace("<", "&lt;").replace(">", "&gt;")}">{part}</span>'
                    )
                else:
                    html_parts.append(f'<span style="{style}">{part}</span>')
                
                sentence_idx += 1
        
        html_parts.append('</div>')
        return ''.join(html_parts)

    def create_vocabulary_suggestions_html(self, inline_feedback: List[Dict]) -> str:
        """Create HTML for vocabulary enhancement suggestions."""
        vocab_suggestions = [f for f in inline_feedback if f['type'] == 'generic_word']
        
        if not vocab_suggestions:
            return '<p style="color: #28a745;">✅ Great vocabulary variety! No generic words detected.</p>'
        
        html = ['<div style="font-family: Arial, sans-serif;">']
        html.append('<h3 style="color: #2c3e50; margin-bottom: 15px;">📚 Vocabulary Enhancement Suggestions</h3>')
        
        for idx, sugg in enumerate(vocab_suggestions, 1):
            word = sugg.get('word', 'word')
            alternatives = sugg.get('alternatives', [])
            html.append(f'''
            <div style="background: #f8f9fa; padding: 12px; margin: 8px 0; border-radius: 8px; border-left: 4px solid #ffc107;">
                <strong style="color: #856404;">Replace "{word}":</strong>
                <div style="margin-top: 5px;">
                    {' • '.join([f'<span style="background: #fff; padding: 3px 8px; margin: 2px; border-radius: 4px; display: inline-block;">{alt}</span>' for alt in alternatives])}
                </div>
            </div>
            ''')
        
        html.append('</div>')
        return ''.join(html)

def create_douessay_interface():
    douessay = DouEssay()
    
    # Session state for draft history
    draft_history = []
    
    def create_score_breakdown_html(detailed_analysis: Dict, score: int) -> str:
        """Create visual dashboard for score breakdown."""
        content_score = detailed_analysis['content']['score']
        structure_score = detailed_analysis['structure']['score']
        grammar_score = detailed_analysis['grammar']['score']
        application_score = detailed_analysis['application']['score']
        
        def create_progress_bar(label, score, max_score=10, color='#3498db'):
            percentage = (score / max_score) * 100
            return f'''
            <div style="margin: 15px 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="font-weight: bold; color: #2c3e50;">{label}</span>
                    <span style="color: {color}; font-weight: bold;">{score:.1f}/{max_score}</span>
                </div>
                <div style="background: #ecf0f1; border-radius: 10px; height: 25px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, {color}, {color}dd); width: {percentage}%; height: 100%; border-radius: 10px; transition: width 0.3s ease;"></div>
                </div>
            </div>
            '''
        
        html = '<div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">'
        html += '<h3 style="color: #2c3e50; margin-top: 0; border-bottom: 2px solid #3498db; padding-bottom: 10px;">📊 Score Breakdown</h3>'
        html += create_progress_bar('Content & Analysis', content_score, color='#e74c3c')
        html += create_progress_bar('Structure & Organization', structure_score, color='#f39c12')
        html += create_progress_bar('Grammar & Mechanics', grammar_score, color='#27ae60')
        html += create_progress_bar('Application & Insight', application_score, color='#9b59b6')
        html += f'<div style="margin-top: 20px; text-align: center; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">'
        html += f'<div style="font-size: 2.5em; font-weight: bold;">{score}/100</div>'
        html += f'<div style="font-size: 1.2em; margin-top: 5px;">Overall Score</div>'
        html += '</div></div>'
        return html
    
    def save_draft(essay_text, result):
        """v3.0.0: Enhanced draft saving with vocabulary tracking."""
        # Calculate vocabulary metrics
        words = essay_text.lower().split()
        generic_words = ['very', 'really', 'a lot', 'many', 'most', 'some', 'things', 'stuff', 'big', 'small', 'good', 'bad']
        generic_count = sum(1 for word in words if word.strip('.,!?;:') in generic_words)
        
        sophisticated_words = [w for w in words if len(w) > 7 and w.isalpha()]
        vocab_score = max(0, 10 - generic_count) + min(10, len(sophisticated_words) / 5)
        
        draft_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'essay': essay_text,
            'score': result['score'],
            'level': result['rubric_level']['level'],
            'word_count': len(words),
            'generic_word_count': generic_count,
            'sophisticated_word_count': len(sophisticated_words),
            'vocab_score': round(vocab_score, 1),
            'reflection_score': result.get('detailed_analysis', {}).get('application', {}).get('reflection_score', 0)
        }
        draft_history.append(draft_entry)
        return draft_history
    
    def create_draft_history_html():
        """v3.0.0: Enhanced draft history with vocabulary improvement tracking."""
        if not draft_history:
            return '<p style="color: #7f8c8d; text-align: center; padding: 20px;">No draft history yet. Submit essays to track your progress!</p>'
        
        html = '<div style="font-family: Arial, sans-serif;">'
        html += '<h3 style="color: #2c3e50; margin-bottom: 15px;">📚 Draft History & Progress</h3>'
        
        # v3.0.0: Multi-metric progress tracking
        if len(draft_history) > 1:
            scores = [d['score'] for d in draft_history]
            vocab_scores = [d.get('vocab_score', 0) for d in draft_history]
            
            html += '<div style="background: white; padding: 15px; border-radius: 8px; margin-bottom: 15px;">'
            html += '<h4 style="color: #2c3e50; margin-top: 0;">📈 Score Evolution</h4>'
            html += '<div style="display: flex; align-items: flex-end; height: 100px; gap: 5px;">'
            max_score = max(scores)
            for i, score in enumerate(scores):
                height_pct = (score / max_score) * 100 if max_score > 0 else 0
                color = '#27ae60' if i > 0 and score > scores[i-1] else '#3498db' if i > 0 and score == scores[i-1] else '#e74c3c'
                html += f'<div style="flex: 1; background: {color}; height: {height_pct}%; min-height: 20px; border-radius: 4px 4px 0 0; position: relative;">'
                html += f'<span style="position: absolute; top: -20px; left: 50%; transform: translateX(-50%); font-size: 0.8em; font-weight: bold; color: {color};">{score}</span>'
                html += '</div>'
            html += '</div>'
            
            # v3.0.0: Vocabulary improvement chart
            html += '<h4 style="color: #2c3e50; margin-top: 20px;">📚 Vocabulary Quality Evolution</h4>'
            html += '<div style="display: flex; align-items: flex-end; height: 80px; gap: 5px;">'
            max_vocab = max(vocab_scores) if vocab_scores else 1
            for i, vocab_score in enumerate(vocab_scores):
                height_pct = (vocab_score / max_vocab) * 100 if max_vocab > 0 else 0
                color = '#9b59b6' if i > 0 and vocab_score > vocab_scores[i-1] else '#3498db'
                html += f'<div style="flex: 1; background: {color}; height: {height_pct}%; min-height: 20px; border-radius: 4px 4px 0 0; position: relative;">'
                html += f'<span style="position: absolute; top: -20px; left: 50%; transform: translateX(-50%); font-size: 0.8em; font-weight: bold; color: {color};">{vocab_score:.1f}</span>'
                html += '</div>'
            html += '</div></div>'
            
            # v3.0.0: Achievement badges
            total_improvement = scores[-1] - scores[0] if len(scores) > 1 else 0
            vocab_improvement = vocab_scores[-1] - vocab_scores[0] if len(vocab_scores) > 1 else 0
            
            if total_improvement > 0 or vocab_improvement > 0:
                html += '<div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 15px; border-radius: 8px; margin-bottom: 15px;">'
                html += '<h4 style="color: white; margin-top: 0;">🏆 Achievements Unlocked</h4>'
                html += '<div style="display: flex; gap: 10px; flex-wrap: wrap;">'
                
                if total_improvement >= 10:
                    html += '<span style="background: white; color: #f5576c; padding: 8px 15px; border-radius: 20px; font-weight: bold;">🎯 Score Climber (+10)</span>'
                if total_improvement >= 20:
                    html += '<span style="background: white; color: #f5576c; padding: 8px 15px; border-radius: 20px; font-weight: bold;">🚀 High Achiever (+20)</span>'
                if vocab_improvement >= 3:
                    html += '<span style="background: white; color: #9b59b6; padding: 8px 15px; border-radius: 20px; font-weight: bold;">📚 Vocabulary Master</span>'
                if len(draft_history) >= 3:
                    html += '<span style="background: white; color: #27ae60; padding: 8px 15px; border-radius: 20px; font-weight: bold;">✍️ Dedicated Writer (3+ Drafts)</span>'
                if any(d['score'] >= 85 for d in draft_history):
                    html += '<span style="background: white; color: #f39c12; padding: 8px 15px; border-radius: 20px; font-weight: bold;">⭐ Level 4 Excellence</span>'
                
                html += '</div></div>'
        
        # List of drafts with enhanced metrics
        for i, draft in enumerate(reversed(draft_history), 1):
            idx = len(draft_history) - i
            score_color = '#27ae60' if draft['score'] >= 80 else '#f39c12' if draft['score'] >= 70 else '#e74c3c'
            
            # Show improvement indicators
            improvement_indicator = ''
            if idx > 0:
                prev_score = draft_history[idx - 1]['score']
                diff = draft['score'] - prev_score
                if diff > 0:
                    improvement_indicator = f' <span style="color: #27ae60;">↑ +{diff}</span>'
                elif diff < 0:
                    improvement_indicator = f' <span style="color: #e74c3c;">↓ {diff}</span>'
            
            html += f'''
            <div style="background: #f8f9fa; padding: 12px; margin: 8px 0; border-radius: 8px; border-left: 4px solid {score_color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: #2c3e50;">Draft #{idx + 1}</strong>
                        <span style="color: #7f8c8d; margin-left: 10px; font-size: 0.9em;">{draft['timestamp']}</span>
                        {improvement_indicator}
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 1.5em; font-weight: bold; color: {score_color};">{draft['score']}</span>
                        <span style="color: #7f8c8d; font-size: 0.9em; margin-left: 5px;">/ 100</span>
                        <div style="color: #2c3e50; font-size: 0.9em;">{draft['level']}</div>
                    </div>
                </div>
                <div style="margin-top: 8px; font-size: 0.85em; color: #7f8c8d;">
                    📝 {draft.get('word_count', 'N/A')} words • 
                    📚 Vocab: {draft.get('vocab_score', 'N/A')}/20 • 
                    💭 Reflection: {draft.get('reflection_score', 'N/A')}/10 • 
                    🚫 Generic words: {draft.get('generic_word_count', 'N/A')}
                </div>
            </div>
            '''
        
        html += '</div>'
        return html
    
    def process_essay(essay_text, license_key, grade_level):
        if not license_key.strip():
            return "Please enter a valid license key.", "", "", "", "", "", "", ""
        
        license_result = douessay.validate_license_and_increment(license_key)
        if not license_result['valid']:
            return f"License Error: {license_result['message']}", "", "", "", "", "", "", ""
        
        if not essay_text.strip():
            return "Please enter an essay to analyze.", "", "", "", "", "", "", ""
        
        # v6.0.0: Pass grade_level to grading function
        result = douessay.grade_essay(essay_text, grade_level)
        
        # Save to draft history
        save_draft(essay_text, result)
        
        # Create annotated essay HTML
        annotated_essay = douessay.create_annotated_essay_html(essay_text, result['inline_feedback'])
        
        # Create vocabulary suggestions
        vocab_html = douessay.create_vocabulary_suggestions_html(result['inline_feedback'])
        
        # Create score breakdown
        score_breakdown = create_score_breakdown_html(result['detailed_analysis'], result['score'])
        
        # Create feedback HTML
        feedback = result['feedback']
        user_info = f"User: {license_result['user_type'].title()} | Usage: {license_result['daily_usage'] + 1}/{license_result['daily_limit']}"
        
        score_color = "#e74c3c"
        if result['score'] >= 85:
            score_color = "#27ae60"
        elif result['score'] >= 80:
            score_color = "#2ecc71"
        elif result['score'] >= 70:
            score_color = "#f39c12"
        elif result['score'] >= 65:
            score_color = "#e67e22"
        
        assessment_html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 1000px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px;">
                <h1 style="margin: 0 0 10px 0; font-size: 2.2em;">DouEssay Assessment System v6.0.0</h1>
                <p style="margin: 0; opacity: 0.9; font-size: 1.1em;">Ontario Standards • ≥99% Teacher Alignment • AI-Enhanced Analysis</p>
                <p style="margin: 10px 0 0 0; font-size: 0.9em; opacity: 0.7;">Created by changcheng967 • v6.0.0: Advanced AI Refinement & Professional Features • Doulet Media Copyright</p>
                <p style="margin: 5px 0 0 0; font-size: 0.8em; opacity: 0.9; background: rgba(255,255,255,0.2); padding: 5px; border-radius: 5px;">{user_info} | Grade: {grade_level}</p>
            </div>
            
            <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px;">
                <div style="text-align: center; margin-bottom: 15px;">
                    <div style="font-size: 3.5em; font-weight: bold; color: {score_color};">
                        {result['score']}/100
                    </div>
                    <div style="font-size: 1.4em; font-weight: bold; color: #2c3e50; margin: 10px 0;">
                        {result['rubric_level']['level']}
                    </div>
                    <div style="color: #7f8c8d; font-size: 1em;">
                        {result['rubric_level']['description']}
                    </div>
                </div>
            </div>
            
            <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <h3 style="margin-top: 0; color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">📝 Detailed Feedback</h3>
                <div style="line-height: 1.8;">
                    {''.join([f'<p style="margin: 10px 0;">{line}</p>' for line in feedback])}
                </div>
            </div>
        </div>
        """
        
        # Inline feedback summary
        inline_summary = f"<div style='padding: 15px; background: #f8f9fa; border-radius: 8px; margin-top: 10px;'>"
        inline_summary += f"<strong>Inline Annotations:</strong> "
        
        green_count = len([f for f in result['inline_feedback'] if f['severity'] == 'green'])
        yellow_count = len([f for f in result['inline_feedback'] if f['severity'] == 'yellow'])
        red_count = len([f for f in result['inline_feedback'] if f['severity'] == 'red'])
        
        inline_summary += f"<span style='color: #28a745;'>✅ {green_count} Strengths</span> • "
        inline_summary += f"<span style='color: #ffc107;'>⚠️ {yellow_count} Suggestions</span> • "
        inline_summary += f"<span style='color: #dc3545;'>❗ {red_count} Critical</span>"
        inline_summary += "</div>"
        
        draft_history_html = create_draft_history_html()
        
        # Apply grammar corrections
        corrected_essay = essay_text
        corrections = result['corrections']
        for correction in sorted(corrections, key=lambda x: x.get('offset', -1), reverse=True):
            # Validate correction structure and values
            offset = correction.get('offset')
            length = correction.get('length')
            suggestion = correction.get('suggestion', '')
            if (
                isinstance(offset, int) and isinstance(length, int) and
                offset >= 0 and length >= 0 and
                offset + length <= len(corrected_essay)
            ):
                start = offset
                end = offset + length
                corrected_essay = corrected_essay[:start] + suggestion + corrected_essay[end:]
            # else: skip invalid correction
        
        return (
            assessment_html,
            annotated_essay + inline_summary,
            score_breakdown,
            vocab_html,
            draft_history_html,
            corrected_essay,
            result['score'],
            result['rubric_level']['level']
        )
    

    with gr.Blocks(title="DouEssay Assessment System", theme=gr.themes.Soft(), css="""
        .gradio-container {max-width: 1400px !important;}
        .tab-nav button {font-size: 1.1em; font-weight: 500;}
        h1, h2, h3 {color: #2c3e50;}
    """) as demo:
        gr.Markdown("# 🎓 DouEssay Assessment System v6.0.0")
        gr.Markdown("### The #1 Professional Essay Grading Tool for Ontario Students")
        gr.Markdown("*≥99% Teacher Alignment • AI-Enhanced Analysis • Dynamic Scoring • Advanced Feedback*")
        gr.Markdown("**Created by changcheng967 • v6.0.0: Most Reliable & Accurate Essay Grading Platform • Supported by Doulet Media**")
        
        with gr.Row():
            license_input = gr.Textbox(
                label="🔑 License Key",
                placeholder="Enter your license key here...",
                type="password",
                scale=2
            )
            grade_level = gr.Dropdown(
                label="📚 Grade Level",
                choices=["Grade 9", "Grade 10", "Grade 11", "Grade 12"],
                value="Grade 10",
                scale=1
            )
        
        with gr.Tabs() as tabs:
            # Tab 1: Essay Input
            with gr.TabItem("📝 Essay Input", id=0):
                gr.Markdown("### Enter or paste your essay below")
                essay_input = gr.Textbox(
                    label="Your Essay",
                    placeholder="Paste your essay content here (250-500 words recommended)...\n\nTips:\n- Clear thesis statement in introduction\n- 3-5 body paragraphs with specific examples\n- Analysis connecting examples to your argument\n- Strong conclusion summarizing key points",
                    lines=15,
                    max_lines=20
                )
                
                with gr.Row():
                    grade_btn = gr.Button("📊 Grade Essay", variant="primary", size="lg")
                    clear_btn = gr.Button("🗑️ Clear", size="lg")
            
            # Tab 2: Assessment Results
            with gr.TabItem("📊 Assessment", id=1):
                gr.Markdown("### Your Essay Assessment")
                assessment_output = gr.HTML()
                
                with gr.Row():
                    with gr.Column():
                        score_display = gr.Number(label="Score", interactive=False)
                    with gr.Column():
                        level_display = gr.Textbox(label="Ontario Level", interactive=False)
            
            # Tab 3: Inline Feedback
            with gr.TabItem("💡 Inline Feedback", id=2):
                gr.Markdown("### Color-Coded Essay with Inline Suggestions")
                gr.Markdown("""
                **Legend:**
                - 🟢 **Green** = Strengths (keep these!)
                - 🟡 **Yellow** = Suggestions for improvement
                - 🔴 **Red** = Critical issues to address
                
                *Hover over highlighted sections for detailed suggestions.*
                """)
                annotated_output = gr.HTML()
            
            # Tab 4: Score Breakdown
            with gr.TabItem("📈 Score Breakdown", id=3):
                gr.Markdown("### Detailed Score Analysis")
                score_breakdown_output = gr.HTML()
            
            # Tab 5: Vocabulary & Style
            with gr.TabItem("📚 Vocabulary & Style", id=4):
                gr.Markdown("### Vocabulary Enhancement Suggestions")
                vocab_output = gr.HTML()
            
            # Tab 6: Draft History
            with gr.TabItem("📜 Draft History", id=5):
                gr.Markdown("### Track Your Progress Across Drafts")
                draft_history_output = gr.HTML()
            
            # Tab 7: Grammar Corrections
            with gr.TabItem("✏️ Grammar Check", id=6):
                gr.Markdown("### Grammar and Spelling Corrections")
                corrected_output = gr.Textbox(
                    label="Corrected Essay",
                    lines=12,
                    interactive=False,
                    show_copy_button=True
                )
        
        # Button actions
        grade_btn.click(
            process_essay,
            inputs=[essay_input, license_input, grade_level],
            outputs=[
                assessment_output,
                annotated_output,
                score_breakdown_output,
                vocab_output,
                draft_history_output,
                corrected_output,
                score_display,
                level_display
            ]
        )
        
        clear_btn.click(
            lambda: ("", "", "", "", "", "", 0, ""),
            outputs=[
                assessment_output,
                annotated_output,
                score_breakdown_output,
                vocab_output,
                draft_history_output,
                corrected_output,
                score_display,
                level_display
            ]
        )
    
    return demo

if __name__ == "__main__":
    demo = create_douessay_interface()
    demo.launch(server_name="0.0.0.0", server_port=7860)
