# 🎓 DouEssay Assessment System

**Professional Essay Grading and Level 4+ Enhancement Tool**

*Ontario Standards • Intelligent Scoring • Real-time Enhancement • Draft Tracking • Advanced Analytics*

**Version 3.0.0** - Now with Reflection Detection, Semantic Similarity Checking, Achievement Badges, and Context-Aware Enhancements!

Created by [changcheng967](https://github.com/changcheng967) • Supported by Doulet Media

---

## ✨ Features

### 1. 📊 Comprehensive Assessment
- **Ontario Curriculum Aligned**: Grades essays according to Ontario high school standards (Levels 1-4+)
- **Multi-Dimensional Scoring**: Evaluates content, structure, grammar, and personal application
- **Real-time Feedback**: Instant assessment with detailed breakdowns

### 2. 💡 Inline Feedback with Color Coding
- **Color-Coded Annotations**: 
  - 🟢 **Green**: Strengths to maintain
  - 🟡 **Yellow**: Areas for improvement
  - 🔴 **Red**: Critical issues requiring attention
- **Sentence-Level Suggestions**: Hover over highlighted text for specific, actionable feedback
- **"How-to" Guidance**: Practical suggestions on improving vague statements and weak analysis

### 3. 📚 Vocabulary & Style Enhancement
- **Active Vocabulary Suggester**: Identifies generic words and provides sophisticated alternatives
- **Sentence Variety Analysis**: Detects repetitive sentence structures and suggests improvements
- **Passive Voice Detection**: Recommends active voice alternatives for stronger writing
- **Transition Suggestions**: Helps improve essay flow and coherence

### 4. 📈 Visual Score Breakdown
- **Component Scoring**: Detailed breakdown of:
  - Content & Analysis
  - Structure & Organization
  - Grammar & Mechanics
  - Application & Insight
- **Progress Bars**: Visual representation of each score component
- **Overall Performance**: Combined score with Ontario level classification

### 5. 📜 Draft History & Progress Tracking
- **Draft Versioning**: Automatically saves each essay submission
- **Score Evolution**: Visual graph showing score improvements over time
- **Historical Comparison**: Track your writing progress across multiple drafts
- **Timestamp Tracking**: See when each draft was submitted

### 6. ✨ Level 4+ Enhancement Feature
- **Intelligent Enhancement**: Automatically elevates essays to Level 4+ standards
- **Before/After Comparison**: Side-by-side view of original and enhanced versions
- **Transparent Changes**: Detailed explanation of enhancements made:
  - Vocabulary elevation
  - Sentence structure sophistication
  - Analytical depth strengthening
  - Transition improvements
  - Personal insight deepening
- **Learning Tool**: Use enhancements as examples for future writing

### 7. ✏️ Grammar & Spell Check
- **Automated Corrections**: Powered by LanguageTool for comprehensive grammar checking
- **Detailed Error Reports**: Shows exact corrections with explanations
- **Corrected Version**: Provides a clean copy with all grammar issues fixed

### 8. 🎯 Personalization
- **Grade-Level Customization**: Adjust feedback complexity based on student grade (9-12)
- **User Type Support**: Free, Plus, Premium, and Unlimited license tiers
- **Usage Tracking**: Monitor daily usage against your license limit

---

## 🚀 Getting Started

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/changcheng967/DouEssay.git
   cd DouEssay
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file with your Supabase credentials:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the interface**:
   Open your browser and navigate to `http://localhost:7860`

### Usage

1. **Enter License Key**: Input your license key for access
2. **Select Grade Level**: Choose your current grade (9-12)
3. **Write/Paste Essay**: Enter your essay in the input tab (250-500 words recommended)
4. **Choose Action**:
   - **Grade Essay**: Get comprehensive assessment with inline feedback
   - **Enhance to Level 4+**: Automatically improve essay to Level 4+ standards
5. **Review Feedback**: Navigate through tabs to explore different aspects:
   - **Assessment**: Overall score and detailed feedback
   - **Inline Feedback**: Color-coded annotations with suggestions
   - **Score Breakdown**: Visual component analysis
   - **Vocabulary & Style**: Specific word alternatives
   - **Draft History**: Track progress over time
   - **Level 4+ Enhancer**: Before/after comparison
   - **Grammar Check**: Corrected version of your essay

---

## 📋 Essay Writing Tips

### For Level 4+ Achievement:

1. **Strong Thesis Statement**:
   - Clear, specific, and arguable main idea
   - Stated explicitly in the introduction
   - Referenced throughout the essay

2. **Rich Examples**:
   - 3-5 specific, detailed examples
   - From varied sources (literature, personal experience, current events)
   - Clearly connected to thesis

3. **Deep Analysis**:
   - Explain *why* and *how*, not just *what*
   - Connect examples back to thesis
   - Discuss broader implications

4. **Sophisticated Vocabulary**:
   - Avoid generic words (very, really, a lot, many)
   - Use precise, academic language
   - Vary word choice throughout

5. **Strong Structure**:
   - Clear introduction with thesis
   - Well-organized body paragraphs with topic sentences
   - Effective transitions between ideas
   - Conclusive ending that synthesizes main points

6. **Personal Insight**:
   - Connect to real-world experiences
   - Show reflection and critical thinking
   - Demonstrate understanding beyond surface level

---

## 🛠️ Technical Details

### Architecture
- **Framework**: Gradio (Python web interface)
- **NLP Tools**: NLTK, LanguageTool
- **Backend**: Supabase (license management and usage tracking)
- **Analysis Engine**: Custom semantic analyzers for Ontario curriculum standards

### Key Components

1. **DouEssay Class**: Core assessment engine
   - Semantic analyzers for thesis, examples, analysis
   - Grammar and style checkers
   - Enhancement algorithms for Level 4+ transformation

2. **Inline Feedback System**:
   - Sentence-level analysis
   - Pattern matching for common issues
   - Context-aware suggestions

3. **Vocabulary Enhancer**:
   - Comprehensive word mapping
   - Contextual alternatives
   - Sophistication scoring

4. **Draft Management**:
   - Session-based history tracking
   - Score evolution visualization
   - Comparative analysis

### Scoring Algorithm

Weighted scoring system:
- **Content & Analysis**: 30%
- **Application & Insight**: 35%
- **Structure & Organization**: 20%
- **Grammar & Mechanics**: 15%

Bonus factors:
- Essay length (optimal: 280-320+ words)
- Complete structure (intro, body, conclusion)
- High grammar accuracy

---

## 📊 License Tiers

| Tier | Daily Limit | Features |
|------|-------------|----------|
| Free | 5 essays | Basic assessment, grading, feedback |
| Plus | 100 essays | All features + draft history |
| Premium | 1000 essays | All features + priority support |
| Unlimited | ∞ | All features + API access |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📝 License

Copyright © 2025 Doulet Media. All rights reserved.

This project combines DouEssayGrader and DouEssayEnhancer into a unified assessment system.

---

## 🔗 Links

- **Repository**: [github.com/changcheng967/DouEssay](https://github.com/changcheng967/DouEssay)
- **Issues**: [Report bugs or request features](https://github.com/changcheng967/DouEssay/issues)
- **Author**: [changcheng967](https://github.com/changcheng967)

---

## 🙏 Acknowledgments

- Ontario Ministry of Education for curriculum standards
- LanguageTool for grammar checking
- NLTK for natural language processing
- Gradio for the amazing UI framework
- Supabase for backend infrastructure

---

## 📞 Support

For support, please:
1. Check the documentation above
2. Search existing [GitHub issues](https://github.com/changcheng967/DouEssay/issues)
3. Create a new issue with detailed information

---

**Made with ❤️ for students striving for Level 4+ excellence**
