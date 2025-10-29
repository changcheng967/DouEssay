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
        self.setup_enhancement_resources()
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
        self.thesis_keywords = [
            'important', 'essential', 'crucial', 'significant', 'key', 'vital',
            'necessary', 'valuable', 'beneficial', 'should', 'must', 'need to',
            'critical', 'plays a role', 'contributes to', 'impacts', 'affects',
            'influences', 'matters because', 'is important because'
        ]
        
        self.example_indicators = [
            'for example', 'for instance', 'such as', 'like when', 'as an example',
            'specifically', 'including', 'case in point', 'to illustrate',
            'as evidence', 'demonstrated by', 'shown by', 'evidenced by'
        ]
        
        self.analysis_indicators = [
            'because', 'this shows', 'therefore', 'as a result', 'thus', 'so',
            'which means', 'this demonstrates', 'consequently', 'this indicates',
            'this suggests', 'for this reason', 'due to', 'owing to', 'leads to',
            'results in', 'implies that', 'suggests that', 'indicates that'
        ]
        
        self.insight_indicators = [
            'in my experience', 'from my perspective', 'personally', 'i have learned',
            'this taught me', 'i realized', 'what this means for me', 'my understanding',
            'this applies to', 'real-world application', 'in real life', 'this reminds me',
            'similar to how', 'just like when', 'in my opinion', 'from my viewpoint',
            'i believe that', 'i feel that', 'in my view'
        ]
        
        self.emotional_indicators = [
            'important', 'valuable', 'meaningful', 'significant', 'challenging',
            'difficult', 'rewarding', 'inspiring', 'painful', 'confident', 'proud',
            'grateful', 'frustrating', 'encouraging', 'motivating', 'impactful'
        ]

    def setup_enhancement_resources(self):
        self.level4_transitions = [
            'however', 'although', 'despite', 'while', 'whereas', 'conversely',
            'furthermore', 'moreover', 'additionally', 'in addition', 'not only',
            'but also', 'on the one hand', 'on the other hand', 'in contrast',
            'similarly', 'likewise', 'by comparison', 'nevertheless', 'nonetheless'
        ]
        
        self.sophisticated_vocab = {
            'hard': ['challenging', 'demanding', 'rigorous', 'arduous'],
            'important': ['significant', 'crucial', 'vital', 'essential', 'paramount'],
            'good': ['beneficial', 'advantageous', 'valuable', 'productive'],
            'bad': ['detrimental', 'counterproductive', 'ineffective', 'problematic'],
            'big': ['substantial', 'considerable', 'significant', 'extensive'],
            'small': ['minimal', 'negligible', 'modest', 'limited'],
            'show': ['demonstrate', 'illustrate', 'exemplify', 'manifest'],
            'think': ['contend', 'maintain', 'assert', 'posit'],
            'because': ['due to', 'owing to', 'as a consequence of', 'resulting from']
        }
        
        self.analysis_boosters = [
            'this demonstrates that', 'this reveals the importance of',
            'this underscores the need for', 'this highlights the significance of',
            'this exemplifies how', 'this illustrates the connection between'
        ]
        
        self.personal_insight_boosters = [
            'from my personal experience', 'through my own observations',
            'what I have come to understand is', 'this has taught me that',
            'reflecting on this, I realize', 'this experience has shown me'
        ]

    def setup_feedback_templates(self):
        self.teacher_feedback_templates = {
            'thesis': [
                "Your main idea is clear but could be more explicit",
                "The thesis is present but could be stronger with specific language",
                "Good start on the main idea; make it more focused and direct"
            ],
            'examples': [
                "Your examples are relevant; add more specific details",
                "Good use of examples; include examples from different contexts",
                "Examples work well; connect them more clearly to your main points"
            ],
            'analysis': [
                "You explain points well; deepen analysis by discussing the why",
                "Good analysis; connect each example back to your thesis",
                "Clear explanations; expand on how examples support your argument"
            ],
            'structure': [
                "Solid structure; use more sophisticated transitions",
                "Good organization; ensure clear topic sentences",
                "Clear structure; vary sentence structure for better flow"
            ],
            'application': [
                "Good real-world connections; add more personal reflection",
                "Nice application; connect ideas to broader implications",
                "Valid insights; add more profound personal connections"
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

    def grade_essay(self, essay_text: str) -> Dict:
        if not essay_text or len(essay_text.strip()) < 100:
            return self.handle_short_essay(essay_text)
        
        stats = self.analyze_basic_stats(essay_text)
        structure = self.analyze_essay_structure_semantic(essay_text)
        content = self.analyze_essay_content_semantic(essay_text)
        grammar = self.check_grammar_errors(essay_text)
        application = self.analyze_personal_application_semantic(essay_text)
        
        score = self.calculate_calibrated_ontario_score(stats, structure, content, grammar, application)
        rubric_level = self.get_accurate_rubric_level(score)
        feedback = self.generate_ontario_teacher_feedback(score, rubric_level, stats, structure, content, grammar, application, essay_text)
        corrections = self.get_grammar_corrections(essay_text)
        
        return {
            "score": score,
            "rubric_level": rubric_level,
            "feedback": feedback,
            "corrections": corrections,
            "detailed_analysis": {
                "statistics": stats,
                "structure": structure,
                "content": content,
                "grammar": grammar,
                "application": application
            }
        }

    def enhance_to_level4(self, original_essay: str) -> str:
        if not original_essay.strip():
            return original_essay
            
        themes = self.analyze_essay_themes(original_essay)
        enhanced_intro = self.enhance_introduction(original_essay, themes)
        enhanced_body = self.enhance_body_paragraphs(original_essay, themes)
        enhanced_conclusion = self.enhance_conclusion(original_essay, themes)
        enhanced_essay = f"{enhanced_intro}\n\n{enhanced_body}\n\n{enhanced_conclusion}"
        enhanced_essay = self.apply_vocabulary_enhancement(enhanced_essay)
        enhanced_essay = self.apply_grammar_enhancement(enhanced_essay)
        return enhanced_essay

    def analyze_essay_themes(self, essay: str) -> Dict:
        text_lower = essay.lower()
        themes = {
            'workload': any(word in text_lower for word in ['work', 'homework', 'assignment', 'busy']),
            'tests': any(word in text_lower for word in ['test', 'exam', 'stress', 'nervous']),
            'boring': any(word in text_lower for word in ['boring', 'not interesting', 'pay attention']),
            'difficult': any(word in text_lower for word in ['hard', 'difficult', 'challenging']),
            'school_negative': any(word in text_lower for word in ['not fun', 'don\'t like', 'hate', 'dislike'])
        }
        return themes

    def enhance_introduction(self, original_essay: str, themes: Dict) -> str:
        introduction_templates = [
            "While education is universally recognized as {positive_adj}, many students find the academic journey to be {challenge_adj}. This essay will explore {topic_focus} and examine {specific_aspects}.",
            "The educational experience, though {positive_adj}, presents significant {challenges} for students. This analysis will delve into {key_issues} and consider {broader_implications}.",
            "Despite the {positive_aspects} of formal education, many learners encounter substantial {difficulties}. This discussion will address {main_points} and reflect on {personal_significance}."
        ]
        
        template = random.choice(introduction_templates)
        positive_adjs = ['essential', 'valuable', 'important', 'crucial']
        challenge_adjs = ['challenging', 'demanding', 'complex', 'multifaceted']
        challenges = ['challenges', 'difficulties', 'obstacles', 'hurdles']
        positive_aspects = ['benefits', 'advantages', 'positive aspects', 'merits']
        
        if themes['workload']:
            topic_focus = "the challenges of academic workload management"
            specific_aspects = "strategies for balancing academic demands"
        elif themes['tests']:
            topic_focus = "the psychological impact of assessment methods"
            specific_aspects = "alternative approaches to student evaluation"
        else:
            topic_focus = "the complex nature of the educational experience"
            specific_aspects = "both the challenges and rewards of learning"
        
        enhanced_intro = template.format(
            positive_adj=random.choice(positive_adjs),
            challenge_adj=random.choice(challenge_adjs),
            challenges=random.choice(challenges),
            positive_aspects=random.choice(positive_aspects),
            topic_focus=topic_focus,
            specific_aspects=specific_aspects,
            key_issues=topic_focus,
            broader_implications=specific_aspects,
            main_points=topic_focus,
            personal_significance=specific_aspects
        )
        
        if random.random() > 0.5:
            transition = random.choice(self.level4_transitions)
            enhanced_intro = f"{transition.capitalize()}, {enhanced_intro.lower()}"
        
        return enhanced_intro

    def enhance_body_paragraphs(self, original_essay: str, themes: Dict) -> str:
        paragraphs = []
        
        if themes['workload']:
            paragraphs.append(self.create_enhanced_paragraph('workload'))
        if themes['tests']:
            paragraphs.append(self.create_enhanced_paragraph('tests'))
        if themes['boring']:
            paragraphs.append(self.create_enhanced_paragraph('boring'))
        
        if not paragraphs:
            paragraphs.extend([
                self.create_generic_enhanced_paragraph("academic challenges"),
                self.create_generic_enhanced_paragraph("learning experiences"),
                self.create_generic_enhanced_paragraph("personal growth")
            ])
        
        enhanced_body = ""
        for i, paragraph in enumerate(paragraphs):
            if i > 0:
                transition = random.choice(['Furthermore,', 'Additionally,', 'Moreover,'])
                paragraph = f"{transition} {paragraph[0].lower()}{paragraph[1:]}"
            enhanced_body += paragraph + "\n\n"
        
        return enhanced_body.strip()

    def create_enhanced_paragraph(self, paragraph_type: str) -> str:
        paragraph_enhancements = {
            'workload': {
                'template': "The substantial academic workload presents a significant challenge. {specific_example} This demanding schedule {analysis_connection} {personal_impact}",
                'examples': [
                    "For instance, balancing multiple advanced courses while participating in extracurricular activities requires exceptional time management skills.",
                    "Specifically, the cumulative effect of daily homework assignments, projects, and exam preparation creates considerable pressure."
                ]
            },
            'tests': {
                'template': "Assessment methods, particularly standardized testing, create considerable anxiety. {specific_example} This evaluation approach {analysis_connection} {broader_implication}",
                'examples': [
                    "High-stakes examinations often fail to capture students' true understanding and can induce significant stress that affects performance.",
                    "The pressure of timed tests can undermine learning by prioritizing memorization over genuine comprehension."
                ]
            },
            'boring': {
                'template': "Certain aspects of the curriculum may lack engagement for some students. {specific_example} However, this {alternative_perspective} {deeper_understanding}",
                'examples': [
                    "While traditional lecture-based instruction may seem monotonous, it's important to recognize the foundational knowledge it provides.",
                    "Subjects that appear less immediately relevant often develop critical thinking skills essential for future success."
                ]
            }
        }
        
        enhancement = paragraph_enhancements[paragraph_type]
        template = enhancement['template']
        example = random.choice(enhancement['examples'])
        
        if paragraph_type == 'workload':
            analysis = "not only tests academic abilities but also teaches valuable time management and prioritization skills"
            personal = "From personal experience, learning to manage this workload has been instrumental in developing organizational habits that extend beyond academics."
        elif paragraph_type == 'tests':
            analysis = "raises important questions about how we measure learning and whether alternative assessment methods might better serve educational goals"
            personal = "This has led me to appreciate assessments that focus on understanding rather than memorization."
        else:
            analysis = "challenges us to find personal relevance in all learning opportunities"
            personal = "I've discovered that even seemingly dry subjects contain valuable lessons when approached with curiosity."
        
        return template.format(
            specific_example=example,
            analysis_connection=analysis,
            personal_impact=personal,
            broader_implication=personal,
            alternative_perspective=analysis,
            deeper_understanding=personal
        )

    def create_generic_enhanced_paragraph(self, topic: str) -> str:
        perspectives = [
            f"On one hand, {topic} present obvious difficulties that can discourage students.",
            f"However, a deeper examination reveals that these very challenges often provide the most valuable learning opportunities.",
            f"This duality underscores the complex nature of education as both demanding and rewarding."
        ]
        
        example = random.choice([
            "For example, struggling with a difficult concept initially can lead to a more profound understanding once mastered.",
            "Consider how overcoming academic obstacles builds resilience and problem-solving abilities.",
            "Research shows that moderate challenge is essential for cognitive growth and skill development."
        ])
        
        insight = random.choice(self.personal_insight_boosters) + " " + random.choice([
            "the most meaningful learning often occurs outside our comfort zones.",
            "education is as much about developing character as it is about acquiring knowledge.",
            "true understanding comes from engaging deeply with challenging material."
        ])
        
        return f"{perspectives[0]} {perspectives[1]} {example} {perspectives[2]} {insight}"

    def enhance_conclusion(self, original_essay: str, themes: Dict) -> str:
        conclusion_templates = [
            "In conclusion, while {acknowledge_challenges}, the {value} of education cannot be overstated. The {lessons} learned extend far beyond the classroom.",
            "Ultimately, the {challenges} of schooling are balanced by its {rewards}. This balance teaches us about {deeper_meaning} and prepares us for {future_applications}.",
            "Therefore, despite the {difficulties} encountered, education remains {fundamentally_important}. The {skills} and {insights} gained have lasting {significance}."
        ]
        
        template = random.choice(conclusion_templates)
        challenges = ['demanding workload', 'assessment pressures', 'engagement challenges']
        values = ['transformative power', 'lasting value', 'fundamental importance']
        lessons = ['resilience', 'critical thinking', 'self-discipline']
        rewards = ['intellectual rewards', 'personal growth', 'skill development']
        deeper_meanings = ['perseverance', 'lifelong learning', 'personal development']
        future_applications = ['future challenges', 'professional endeavors', 'life decisions']
        difficulties = ['academic pressures', 'learning obstacles', 'educational demands']
        fundamentally_important = ['essential for success', 'fundamentally important', 'critical for development']
        skills = ['analytical skills', 'communication abilities', 'problem-solving capabilities']
        insights = ['personal insights', 'academic discoveries', 'educational revelations']
        significance = ['personal significance', 'lasting impact', 'enduring value']
        
        enhanced_conclusion = template.format(
            acknowledge_challenges=random.choice(challenges),
            value=random.choice(values),
            lessons=random.choice(lessons),
            challenges=random.choice(challenges),
            rewards=random.choice(rewards),
            deeper_meaning=random.choice(deeper_meanings),
            future_applications=random.choice(future_applications),
            difficulties=random.choice(difficulties),
            fundamentally_important=random.choice(fundamentally_important),
            skills=random.choice(skills),
            insights=random.choice(insights),
            significance=random.choice(significance)
        )
        
        reflection = random.choice([
            "This reflection has deepened my appreciation for the educational journey.",
            "These insights will continue to inform my approach to learning.",
            "The lessons extend far beyond academic settings into all aspects of life."
        ])
        
        return f"{enhanced_conclusion} {reflection}"

    def apply_vocabulary_enhancement(self, text: str) -> str:
        enhanced_text = text
        for simple_word, sophisticated_options in self.sophisticated_vocab.items():
            if simple_word in enhanced_text.lower():
                replacement = random.choice(sophisticated_options)
                enhanced_text = re.sub(
                    re.escape(simple_word), 
                    replacement, 
                    enhanced_text, 
                    flags=re.IGNORECASE
                )
        return enhanced_text

    def apply_grammar_enhancement(self, text: str) -> str:
        if not self.grammar_enabled:
            return text
            
        try:
            matches = self.grammar_tool.check(text)
            corrected_text = self.grammar_tool.correct(text)
            return corrected_text
        except:
            return text

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
        structure_score = (intro_score + conclusion_score + coherence_score) / 3 * 10
        
        return {
            "score": min(10, structure_score),
            "has_introduction": intro_score >= 0.6,
            "has_conclusion": conclusion_score >= 0.6,
            "paragraph_count": len(paragraphs),
            "intro_quality": round(intro_score, 2),
            "conclusion_quality": round(conclusion_score, 2),
            "coherence_score": round(coherence_score, 2)
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
        content_score = (thesis_score + example_score + analysis_score) / 3 * 10
        
        return {
            "score": min(10, content_score),
            "has_thesis": thesis_score >= 0.6,
            "example_count": example_count,
            "analysis_count": int(analysis_score * 5),
            "thesis_quality": round(thesis_score, 2),
            "example_quality": round(example_score, 2),
            "analysis_quality": round(analysis_score, 2)
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

    def analyze_personal_application_semantic(self, text: str) -> Dict:
        text_lower = text.lower()
        insight_score = self.assess_personal_insight_semantic(text)
        real_world_score = self.assess_real_world_connections_semantic(text)
        lexical_score = self.assess_lexical_diversity_semantic(text)
        application_score = (insight_score + real_world_score + lexical_score) / 3 * 10
        
        return {
            "score": min(10, application_score),
            "insight_score": round(insight_score, 2),
            "real_world_score": round(real_world_score, 2),
            "lexical_score": round(lexical_score, 2)
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
                                         grammar: Dict, application: Dict) -> int:
        weights = {
            'content': 0.30,
            'structure': 0.20,
            'grammar': 0.15,
            'application': 0.35
        }
        
        base_score = (
            content['score'] * weights['content'] * 10 +
            structure['score'] * weights['structure'] * 10 +
            grammar['score'] * weights['grammar'] * 10 +
            application['score'] * weights['application'] * 10
        )
        
        word_count = stats['word_count']
        if word_count >= 320:
            length_bonus = 3
        elif word_count >= 280:
            length_bonus = 2
        elif word_count >= 240:
            length_bonus = 1
        else:
            length_bonus = -1
            
        calibration_factor = 1.1
        final_score = (base_score + length_bonus) * calibration_factor
        
        if content['has_thesis'] and structure['has_introduction'] and grammar['score'] >= 8:
            final_score += 2
            
        return max(65, min(95, int(final_score)))

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
            
        feedback.append("")
        feedback.append("🎯 NEXT STEPS:")
        next_steps = self.get_ontario_next_steps(score, structure, content, application)
        for step in next_steps:
            feedback.append(f"• {step}")
            
        return feedback

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

    def identify_improvements_semantic(self, structure: Dict, content: Dict, grammar: Dict, 
                                    application: Dict, stats: Dict, essay_text: str) -> List[str]:
        improvements = []
        
        if content['thesis_quality'] < 0.6:
            improvements.append("Strengthen your thesis statement in the introduction")
        if content['example_count'] < 2:
            improvements.append("Add more specific examples to support each main point")
        if content['analysis_quality'] < 0.6:
            improvements.append("Deepen your analysis by explaining how examples prove your points")
            
        if structure['intro_quality'] < 0.6:
            improvements.append("Work on creating a more engaging introduction")
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
            }
        }

def create_douessay_interface():
    douessay = DouEssay()
    
    def process_essay(essay_text, action, license_key):
        if not license_key.strip():
            return "Please enter a valid license key.", "", "", "", ""
        
        license_result = douessay.validate_license_and_increment(license_key)
        if not license_result['valid']:
            return f"License Error: {license_result['message']}", "", "", "", ""
        
        if not essay_text.strip():
            return "Please enter an essay to analyze.", "", "", "", ""
        
        if action == "Grade":
            result = douessay.grade_essay(essay_text)
            feedback = result['feedback']
            corrections = result['corrections']
            corrected_essay = essay_text
            
            for correction in sorted(corrections, key=lambda x: x['offset'], reverse=True):
                start = correction['offset']
                end = correction['offset'] + correction['length']
                corrected_essay = corrected_essay[:start] + correction['suggestion'] + corrected_essay[end:]
            
            score_color = "#e74c3c"
            if result['score'] >= 85:
                score_color = "#27ae60"
            elif result['score'] >= 80:
                score_color = "#2ecc71"
            elif result['score'] >= 70:
                score_color = "#f39c12"
            elif result['score'] >= 65:
                score_color = "#e67e22"
            
            user_info = f"User: {license_result['user_type'].title()} | Usage: {license_result['daily_usage'] + 1}/{license_result['daily_limit']}"
            
            assessment_html = f"""
            <div style="font-family: Arial, sans-serif; max-width: 1000px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px;">
                    <h1 style="margin: 0 0 10px 0; font-size: 2.2em;">DouEssay Assessment System</h1>
                    <p style="margin: 0; opacity: 0.9; font-size: 1.1em;">Ontario Standards • Intelligent Scoring • Level 4+ Enhancement</p>
                    <p style="margin: 10px 0 0 0; font-size: 0.9em; opacity: 0.7;">Created by changcheng967 • Doulet Media Copyright</p>
                    <p style="margin: 5px 0 0 0; font-size: 0.8em; opacity: 0.9; background: rgba(255,255,255,0.2); padding: 5px; border-radius: 5px;">{user_info}</p>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 20px; margin-bottom: 20px;">
                    <div style="background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center;">
                        <div style="font-size: 3.5em; font-weight: bold; color: {score_color}; margin-bottom: 10px;">
                            {result['score']}/100
                        </div>
                        <div style="font-size: 1.4em; font-weight: bold; color: #2c3e50; margin-bottom: 5px;">
                            {result['rubric_level']['level']}
                        </div>
                        <div style="color: #7f8c8d; font-size: 1em;">
                            {result['rubric_level']['description']}
                        </div>
                    </div>
                    
                    <div style="background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h3 style="margin-top: 0; color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">Detailed Feedback</h3>
                        <div style="max-height: 400px; overflow-y: auto; line-height: 1.6;">
                            {''.join([f'<p style="margin: 10px 0;">{line}</p>' for line in feedback])}
                        </div>
                    </div>
                </div>
            </div>
            """
            
            return assessment_html, essay_text, corrected_essay, result['score'], result['rubric_level']['level']
        
        else:
            enhanced_essay = douessay.enhance_to_level4(essay_text)
            user_info = f"User: {license_result['user_type'].title()} | Usage: {license_result['daily_usage'] + 1}/{license_result['daily_limit']}"
            
            enhancement_html = f"""
            <div style="font-family: Arial, sans-serif; max-width: 1000px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px;">
                    <h1 style="margin: 0 0 10px 0; font-size: 2.2em;">DouEssay Enhancement System</h1>
                    <p style="margin: 0; opacity: 0.9; font-size: 1.1em;">Level 4+ Standards • Intelligent Enhancement • Professional Quality</p>
                    <p style="margin: 10px 0 0 0; font-size: 0.9em; opacity: 0.7;">Created by changcheng967 • Doulet Media Copyright</p>
                    <p style="margin: 5px 0 0 0; font-size: 0.8em; opacity: 0.9; background: rgba(255,255,255,0.2); padding: 5px; border-radius: 5px;">{user_info}</p>
                </div>
                
                <div style="background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center;">
                    <div style="font-size: 2.5em; font-weight: bold; color: #27ae60; margin-bottom: 10px;">
                        ✓ Enhanced to Level 4+
                    </div>
                    <div style="font-size: 1.2em; color: #2c3e50; margin-bottom: 20px;">
                        Your essay has been enhanced to meet Ontario Level 4+ standards
                    </div>
                </div>
            </div>
            """
            
            return enhancement_html, essay_text, enhanced_essay, "N/A", "Level 4+"
    
    with gr.Blocks(title="DouEssay Assessment System", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🎓 DouEssay Assessment System")
        gr.Markdown("### Professional Essay Grading and Level 4+ Enhancement Tool")
        gr.Markdown("*Ontario Standards • Intelligent Scoring • Real-time Enhancement*")
        gr.Markdown("**Created by changcheng967 • This is the main DouEssay project combining DouEssayGrader and DouEssayEnhancer, supported by Doulet Media**")
        
        with gr.Row():
            with gr.Column(scale=2):
                license_input = gr.Textbox(
                    label="License Key",
                    placeholder="Enter your license key here...",
                    type="password"
                )
                
                essay_input = gr.Textbox(
                    label="Enter Your Essay",
                    placeholder="Paste your essay content here (250-500 words recommended)...",
                    lines=12
                )
                
                with gr.Row():
                    action_radio = gr.Radio(
                        choices=["Grade", "Enhance to Level 4+"],
                        label="Select Action",
                        value="Grade"
                    )
                    process_btn = gr.Button("🚀 Process Essay", variant="primary")
                    clear_btn = gr.Button("Clear All")
            
            with gr.Column(scale=1):
                output_html = gr.HTML()
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 📝 Original Essay")
                original_output = gr.Textbox(
                    lines=6,
                    interactive=False,
                    show_copy_button=True
                )
            
            with gr.Column():
                gr.Markdown("### 💫 Processed Result")
                processed_output = gr.Textbox(
                    lines=6,
                    interactive=True,
                    show_copy_button=True
                )
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 📊 Assessment Results")
                score_output = gr.Number(label="Score", interactive=False)
                level_output = gr.Textbox(label="Level", interactive=False)
        
        process_btn.click(
            process_essay, 
            inputs=[essay_input, action_radio, license_input], 
            outputs=[output_html, original_output, processed_output, score_output, level_output]
        )
        
        clear_btn.click(
            lambda: ("", "", "", 0, ""), 
            outputs=[output_html, original_output, processed_output, score_output, level_output]
        )
        
    return demo

if __name__ == "__main__":
    demo = create_douessay_interface()
    demo.launch(server_name="0.0.0.0", server_port=7860)
