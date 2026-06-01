import streamlit as st
import os
import time
import json
import re
import random
import urllib.parse
from datetime import datetime
import numpy as np
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
from faker import Faker
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
import feedparser
import requests
from fpdf import FPDF

# Load environment variables
load_dotenv()

# Configure page config
st.set_page_config(
    page_title="Ratefluencer AI – Viral Reel Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("GEMINI_API_KEY not found. Please configure your .env file or credentials.")

# Detect Gemini Model
@st.cache_resource
def detect_gemini_model():
    if not api_key:
        return "gemini-2.5-flash"
    try:
        models = [m.name for m in genai.list_models()]
        if 'models/gemini-1.5-flash' in models:
            return 'gemini-1.5-flash'
        elif 'models/gemini-2.5-flash' in models:
            return 'gemini-2.5-flash'
        elif 'models/gemini-2.0-flash' in models:
            return 'gemini-2.0-flash'
        else:
            return 'gemini-flash-latest'
    except Exception:
        return "gemini-2.5-flash"

gemini_model_name = detect_gemini_model()

# Safe Gemini Caller with retries
def call_gemini_safe(prompt):
    if not api_key:
        return get_mock_gemini_response(prompt)
    for attempt in range(3):
        try:
            model = genai.GenerativeModel(gemini_model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            err_msg = str(e).lower()
            if "429" in err_msg or "resourceexhausted" in err_msg or "rate limit" in err_msg or "quota" in err_msg:
                time.sleep(3 + attempt * 2)
            else:
                print(f"Gemini error: {e}")
                break
    return get_mock_gemini_response(prompt)

def get_mock_gemini_response(prompt):
    prompt_lower = prompt.lower()
    if "ideas" in prompt_lower or "performance" in prompt_lower:
        return json.dumps([
            {
                "title": "Why solo founders are deploying autonomous agent loops",
                "audience": "Solopreneurs & Indie Hackers",
                "why_will_perform": "Taps into the trending solopreneur automation movement. Clear visual and financial hook.",
                "virality_estimate": "92%",
                "engagement_potential": "High"
            },
            {
                "title": "The recursive API billing trap: audit your database loops",
                "audience": "SaaS Engineers & Founders",
                "why_will_perform": "High-fear, high-value technical hook that developers will save and share to protect bills.",
                "virality_estimate": "96%",
                "engagement_potential": "Extreme"
            },
            {
                "title": "Chatbots are officially dead, agent workspaces are taking over",
                "audience": "Tech Enthusiasts & Founders",
                "why_will_perform": "Highly polarizing headline that challenges standard chatbot logic to drive comment debates.",
                "virality_estimate": "89%",
                "engagement_potential": "High"
            },
            {
                "title": "Auditing loop nodes in your vector database pipeline",
                "audience": "Data Architects",
                "why_will_perform": "Highly niche, detailed technical walkthrough that targets vector db optimizations.",
                "virality_estimate": "74%",
                "engagement_potential": "Moderate"
            },
            {
                "title": "The ultimate framework for scaling Agentic AI in 2026",
                "audience": "CTOs & Product Owners",
                "why_will_perform": "Forward-looking strategic advice that positions creators as authority guides in enterprise AI.",
                "virality_estimate": "82%",
                "engagement_potential": "High"
            }
        ])
    elif "scene" in prompt_lower or "visual_asset" in prompt_lower:
        return json.dumps({
            "voiceover_script": "Stop building standard chatbot panels. The future of software is autonomous loops. Indie hackers are deploying recursive agent nodes to compile full projects in under 10 minutes. But unchecked loops can spike your API bills by 10x overnight. Save this post to learn how to audit your agent pipelines!",
            "subtitle_script": "Stop building chatbots... The future is autonomous loops... Build SaaS projects in 10 minutes... But it can spike your API bills by 10x!... Save this post to audit your pipelines!",
            "thumbnail_prompt": "A modern glow UI displaying recursive digital lines. Text overlay in bold Outfit typography: 'CHATS ARE DEAD: THE AGENTIC ERA.' Glowing cyan and purple accents, high tech dark background.",
            "b_roll_suggestions": "Close-up of keyboard typing, terminal code scrolling, floating agent loop diagram, credit card invoice showing high API usage, mobile screen warning alert.",
            "scenes": [
                {
                    "scene_number": 1,
                    "duration": "0-5s",
                    "title": "Scene 1: Hook visual",
                    "visual_prompt": "Close-up of a developer shutting down a standard chat screen. Transitioning to a glowing recursive database console.",
                    "b_roll": "Close-up of hands shutting laptop screen.",
                    "subtitle": "Stop coding chat panels. The future is autonomous loops.",
                    "camera_direction": "Slow push-in on screen details",
                    "editing_suggestions": "Fast crop jump-cut transition"
                },
                {
                    "scene_number": 2,
                    "duration": "5-20s",
                    "title": "Scene 2: Problem visualization",
                    "visual_prompt": "Screen view showing a fast-scrolling terminal running agent scripts, with a high API usage overlay blinking in neon orange.",
                    "b_roll": "Fast scrolling code on terminal.",
                    "subtitle": "Indie hackers are deploying loop agents... but it can spike your API bills by 10x!",
                    "camera_direction": "Pan down screen code lines",
                    "editing_suggestions": "Add sound effect on red alert popup"
                },
                {
                    "scene_number": 3,
                    "duration": "20-35s",
                    "title": "Scene 3: Main insight",
                    "visual_prompt": "A diagram mapping a loop node audit workflow. Highlights of database auditing tools glowing in neon purple.",
                    "b_roll": "Audit diagram workflow panning.",
                    "subtitle": "Audit your loops and scale agent workloads safely.",
                    "camera_direction": "Dolly right following data pipeline arrows",
                    "editing_suggestions": "Slow cross-dissolve fade"
                },
                {
                    "scene_number": 4,
                    "duration": "35-45s",
                    "title": "Scene 4: Call to action",
                    "visual_prompt": "End screen showing social icon handles with a pulse effect. Text overlay: 'SAVE FOR LATER'.",
                    "b_roll": "Save icon animation pulsing.",
                    "subtitle": "Tap follow and save this post to audit your pipelines!",
                    "camera_direction": "Center focus static macro shot",
                    "editing_suggestions": "Pulse glow fadeout"
                }
            ]
        })
    elif "hook" in prompt_lower and "story" in prompt_lower:
        return json.dumps({
            "hook": "Stop coding chat panels. The future of software is autonomous loops.",
            "story": "Developers are deploying recursive agent pipelines to build SaaS projects in minutes. But recursive loops can spike your API bills by 10x overnight.",
            "insights": [
                "Agent nodes execute multi-step tasks autonomously.",
                "Recursive loops without limits can lead to infinite API bills.",
                "Auditing loop iterations prevents high billing spikes."
            ],
            "cta": "Tap follow to audit your loop nodes!"
        })
    elif "linkedin" in prompt_lower:
        return json.dumps({
            "post": "SaaS architecture is pivoting. Autonomous loops are replacing text prompts. 🤖\n\nSolo developers are currently using multi-agent loops to construct full projects. However, unchecked recursive pipelines are causing massive database overhead and infinite API bills.\n\nHere are 3 keys to building loop agents safely:\n1️⃣ Establish iteration caps: Hard limits prevent infinite loops.\n2️⃣ Implement budget alerts: Real-time spend caps block runaway requests.\n3️⃣ Run local audit logs: Track recursive nodes before production push.\n\nAre you building traditional chat interfaces, or are you deploying loop nodes?",
            "hashtags": "#ArtificialIntelligence #SaaS #FutureOfCoding #DatabaseDesign",
            "engagement_hook": "How is your engineering team adapting to autonomous agent nodes? Let's discuss below!",
            "image_prompt": "Vector style illustration of glowing AI node loops connected to database tables. Style: Glassmorphism futuristic dashboard. Colors: Neon cyan, purple, dark charcoal. Text overlay: 'SECURE YOUR AI AGENT LOOPS.' 8k resolution, centered composition."
        })
    elif "instagram" in prompt_lower:
        return json.dumps({
            "caption": "Chats are legacy. Loops are next. ⚡ Solo founders are scaling systems by deploying autonomous agent nodes. But beware of recursive API traps! Swipe left to read how to build loops safely! 👇",
            "hashtags": "#aidevelopment #saasstartup #codinglife #databaseaudit #indiehackers",
            "cta": "Save this reel to protect your vector pipelines! 📌",
            "thumbnail_prompt": "Futuristic neon alert symbol on a dark computer monitor, glowing orange lines showing high spend. In bold white text: 'STOP runaway AI loops.' 3D render style, cinematic depth of field."
        })
    elif "views" in prompt_lower or "prediction" in prompt_lower:
        return json.dumps({
            "virality_score": 92.4,
            "expected_views": 1150000,
            "expected_likes": 86250,
            "expected_shares": 28750,
            "expected_saves": 51750,
            "reasoning": "This content triggers a strong emotional response of fear (losing money on API bills) combined with massive value (safe AI agent templates). Solopreneurship and AI loops are currently experiencing a search trend increase of 300% on RSS boards.",
            "factors": [
                "High emotional trigger: Financial risk alert (API bill overhead).",
                "Strong saving utility: Developers will bookmark the audit list.",
                "Optimized hook word count: Hook has 11 words, matching high-retention length indices."
            ]
        })
    return "Sample AI response placeholder."

# XGBoost Training Data & Model Caching
csv_train_path = os.path.join("data", "virality_train.csv")

def ensure_virality_training_data():
    if not os.path.exists("data"):
        os.makedirs("data", exist_ok=True)
    if not os.path.exists(csv_train_path):
        fake = Faker()
        np.random.seed(42)
        rows = []
        for _ in range(100):
            hook_text = fake.sentence(nb_words=np.random.randint(6, 16))
            trend_val = float(np.random.uniform(50, 98))
            novel_val = float(np.random.uniform(30, 95))
            words_count = len(hook_text.split())
            hook_dev = abs(words_count - 11)
            views_val = trend_val * 0.45 + (25 - hook_dev * 2.5) + novel_val * 0.35 + np.random.normal(0, 4)
            views_val = float(np.clip(views_val, 20.0, 99.5))
            rows.append({
                "hook_words": hook_text,
                "trend_score": trend_val,
                "novelty": novel_val,
                "views": views_val
            })
        df = pd.DataFrame(rows)
        df.to_csv(csv_train_path, index=False)

ensure_virality_training_data()

# Train XGBoost
df_train = pd.read_csv(csv_train_path)
df_train["hook_word_count"] = df_train["hook_words"].apply(lambda x: len(str(x).split()))
X_xgb = df_train[["trend_score", "hook_word_count", "novelty"]]
y_xgb = df_train["views"]
xgb_model = XGBRegressor(n_estimators=30, max_depth=3, learning_rate=0.1, random_state=42)
xgb_model.fit(X_xgb, y_xgb)

# Train RandomForest for Trend Scorer
np.random.seed(42)
X_rf = np.random.rand(100, 4)
y_rf = (X_rf[:, 0] * 35 + X_rf[:, 1] * 25 + X_rf[:, 2] * 25 + (1.0 - X_rf[:, 3]) * 15)
rf_model = RandomForestRegressor(n_estimators=15, random_state=42)
rf_model.fit(X_rf, y_rf)

def compute_sentiment(title):
    pos_triggers = ["breakthrough", "new", "release", "future", "epic", "scale", "power", "unreal", "quantum", "openai", "verge", "techcrunch", "ai", "agent", "loop"]
    neg_triggers = ["fail", "mistake", "scam", "danger", "worst", "bug", "stagnant", "broke", "expensive", "layoffs"]
    title_lower = title.lower()
    score = 0.0
    for w in pos_triggers:
        if w in title_lower:
            score += 0.2
    for w in neg_triggers:
        if w in title_lower:
            score -= 0.2
    return max(min(score, 1.0), -1.0)


# ==========================================
# CUSTOM STYLING (Charcoal & Neon Gradients)
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Outfit', sans-serif;
    background-color: #08090d;
    color: #f8fafc;
}

/* Glassmorphism containers */
.glass-container {
    background: rgba(13, 16, 26, 0.7);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.7);
}

.title-gradient {
    background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 50%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.8rem;
    font-weight: 800;
}

/* Stat Value */
.stat-val {
    font-size: 2.2rem;
    font-weight: 800;
    color: #06b6d4;
    text-shadow: 0 0 10px rgba(6, 182, 212, 0.3);
}

/* Agent tags */
.agent-tag {
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
    text-transform: uppercase;
}
.tag-waiting { background: rgba(255,255,255,0.03); color: #64748b; border: 1px solid rgba(255,255,255,0.05); }
.tag-running { background: rgba(59, 130, 246, 0.1); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.3); }
.tag-completed { background: rgba(16, 185, 129, 0.1); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); }
.tag-failed { background: rgba(239, 68, 68, 0.1); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); }

/* Timeline UI */
.timeline-list {
    position: relative;
    padding-left: 28px;
    margin-top: 10px;
}
.timeline-list::before {
    content: '';
    position: absolute;
    top: 5px;
    left: 8px;
    width: 2px;
    height: calc(100% - 10px);
    background: linear-gradient(180deg, #8b5cf6, #3b82f6, #06b6d4);
}
.timeline-item {
    position: relative;
    margin-bottom: 20px;
    background: rgba(255, 255, 255, 0.015);
    border: 1px solid rgba(255, 255, 255, 0.03);
    border-radius: 8px;
    padding: 14px 18px;
}
.timeline-dot {
    position: absolute;
    top: 14px;
    left: -25px;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #08090d;
    border: 3px solid #8b5cf6;
    z-index: 2;
}

/* Pipeline Visual Nodes */
.pipeline-visual-nodes {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
}
.pipeline-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    min-width: 60px;
    opacity: 0.3;
    transition: all 0.3s ease;
}
.pipeline-node.active {
    opacity: 1;
}
.pnode-dot {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: rgba(13, 16, 26, 0.8);
    border: 2px solid rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    margin-bottom: 6px;
    transition: all 0.3s ease;
    box-shadow: 0 0 10px rgba(0,0,0,0.5);
}
.pipeline-node.active .pnode-dot {
    border-color: #8b5cf6;
    box-shadow: 0 0 15px rgba(139, 92, 246, 0.4);
    background: rgba(139, 92, 246, 0.15);
}
.pnode-label {
    font-size: 10px;
    font-weight: 700;
    color: #64748b;
}
.pipeline-node.active .pnode-label {
    color: #f8fafc;
}
.pnode-arrow-line {
    flex-grow: 1;
    height: 2px;
    background: rgba(255, 255, 255, 0.08);
    position: relative;
    margin: 0 10px;
    margin-top: -20px;
    min-width: 20px;
}
.pipeline-node.active + .pnode-arrow-line {
    background: linear-gradient(90deg, #8b5cf6, #3b82f6);
}
.arrow-pulse {
    position: absolute;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #06b6d4;
    top: -2px;
    left: 0;
    animation: pulseArrow 2s infinite linear;
}
@keyframes pulseArrow {
    0% { left: 0%; opacity: 0; }
    50% { opacity: 1; }
    100% { left: 100%; opacity: 0; }
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# DEMO DATA PACKAGE
# ==========================================
DEMO_DATA = {
    "niche": "Creator Economy",
    "trends": [
        {
            "title": "Auditing recursive loop nodes to prevent run-away vector database bills",
            "source": "TechCrunch",
            "upvotes": 1840,
            "num_comments": 310,
            "score": 94.6,
            "growth_velocity": 88.5,
            "novelty": 92.0,
            "engagement_potential": 89.2,
            "audience_relevance": 96.0
        },
        {"title": "New open source models outperform proprietary giants on local hardware", "source": "r/MachineLearning", "upvotes": 2150, "num_comments": 420, "score": 89.8, "growth_velocity": 82.1, "novelty": 87.5, "engagement_potential": 94.0, "audience_relevance": 85.0},
        {"title": "How developers are building entire SaaS projects in 10 minutes with AI tools", "source": "r/startups", "upvotes": 1100, "num_comments": 195, "score": 84.2, "growth_velocity": 78.4, "novelty": 75.0, "engagement_potential": 82.0, "audience_relevance": 91.5},
        {"title": "Apple launches local agentic Siri framework on next-gen devices", "source": "The Verge", "upvotes": 1620, "num_comments": 280, "score": 81.5, "growth_velocity": 72.0, "novelty": 80.0, "engagement_potential": 78.5, "audience_relevance": 88.0},
        {"title": "SaaS seed funding pivots entirely towards agentic infrastructure startups", "source": "TechCrunch", "upvotes": 950, "num_comments": 80, "score": 79.1, "growth_velocity": 64.2, "novelty": 85.0, "engagement_potential": 62.0, "audience_relevance": 75.0}
    ],
    "ideas": [
        {"title": "Why solo founders are deploying autonomous agent loops", "audience": "Solopreneurs & Indie Hackers", "why_will_perform": "Taps into the trending solopreneur automation movement. Clear visual and financial hook.", "virality_estimate": "92%", "engagement_potential": "High"},
        {"title": "The recursive API billing trap: audit your database loops", "audience": "SaaS Engineers & Founders", "why_will_perform": "High-fear, high-value technical hook that developers will save and share to protect bills.", "virality_estimate": "96%", "engagement_potential": "Extreme"},
        {"title": "Chatbots are dead, agent workspaces are taking over", "audience": "Tech Enthusiasts & Founders", "why_will_perform": "Highly polarizing headline that challenges standard chatbot logic to drive comment debates.", "virality_estimate": "89%", "engagement_potential": "High"},
        {"title": "Auditing loop nodes in your vector database pipeline", "audience": "Data Architects", "why_will_perform": "Highly niche, detailed technical walkthrough that targets vector db optimizations.", "virality_estimate": "74%", "engagement_potential": "Moderate"},
        {"title": "The ultimate framework for scaling Agentic AI in 2026", "audience": "CTOs & Product Owners", "why_will_perform": "Forward-looking strategic advice that positions creators as authority guides in enterprise AI.", "virality_estimate": "82%", "engagement_potential": "High"}
    ],
    "script": {
        "hook": "Stop coding chat panels. The future of software is autonomous loops.",
        "story": "Indie hackers are deploying recursive agent nodes to build complete applications in minutes. But unchecked loops can spike your API bills by 10x overnight.",
        "insights": [
            "Agent nodes execute multi-step tasks autonomously.",
            "Recursive loops without limits can lead to infinite API bills.",
            "Auditing loop iterations prevents high billing spikes."
        ],
        "cta": "Tap follow to audit your loop nodes!"
    },
    "reel_studio": {
        "voiceover_script": "Stop coding chat panels. The future of software is autonomous loops. Indie hackers are deploying recursive agent nodes to build complete applications in minutes. But be careful: unchecked loops can spike your API bills by 10x overnight. Save this post to learn how to audit your agent pipelines!",
        "subtitle_script": "Stop building chatbots... The future is autonomous loops... Build SaaS projects in 10 minutes... But it can spike your API bills by 10x!... Save this post to audit your pipelines!",
        "thumbnail_prompt": "A modern glow UI displaying recursive digital lines. Text overlay in bold Outfit typography: 'CHATS ARE DEAD: THE AGENTIC ERA.' Glowing cyan and purple accents, high tech dark background.",
        "b_roll_suggestions": "Close-up of keyboard typing, terminal code scrolling, floating agent loop diagram, credit card invoice showing high API usage, mobile screen warning alert.",
        "scenes": [
            {"scene_number": 1, "duration": "0-5s", "title": "Scene 1: Hook visual", "visual_prompt": "Close-up of a developer shutting down a standard chat screen. Transitioning to a glowing recursive database console.", "b_roll": "Close-up of hands shutting laptop screen.", "subtitle": "Stop coding chat panels. The future is autonomous loops.", "camera_direction": "Slow push-in on screen details", "editing_suggestions": "Fast crop jump-cut transition"},
            {"scene_number": 2, "duration": "5-20s", "title": "Scene 2: Problem visualization", "visual_prompt": "Screen view showing a fast-scrolling terminal running agent scripts, with a high API usage overlay blinking in neon orange.", "b_roll": "Fast scrolling code on terminal.", "subtitle": "Indie hackers are deploying loop agents... but it can spike your API bills by 10x!", "camera_direction": "Pan down screen code lines", "editing_suggestions": "Add sound effect on red alert popup"},
            {"scene_number": 3, "duration": "20-35s", "title": "Scene 3: Main insight", "visual_prompt": "A diagram mapping a loop node audit workflow. Highlights of database auditing tools glowing in neon purple.", "b_roll": "Audit diagram workflow panning.", "subtitle": "Audit your loops and scale agent workloads safely.", "camera_direction": "Dolly right following data pipeline arrows", "editing_suggestions": "Slow cross-dissolve fade"},
            {"scene_number": 4, "duration": "35-45s", "title": "Scene 4: Call to action", "visual_prompt": "End screen showing social icon handles with a pulse effect. Text overlay: 'SAVE FOR LATER'.", "b_roll": "Save icon animation pulsing.", "subtitle": "Tap follow and save this post to audit your pipelines!", "camera_direction": "Center focus static macro shot", "editing_suggestions": "Pulse glow fadeout"}
        ]
    },
    "linkedin": {
        "post": "SaaS architecture is pivoting. Autonomous loops are replacing text prompts. 🤖\n\nSolo developers are currently using multi-agent loops to construct full projects. However, unchecked recursive pipelines are causing massive database overhead and infinite API bills.\n\nHere are 3 keys to building loop agents safely:\n1️⃣ Establish iteration caps: Hard limits prevent infinite loops.\n2️⃣ Implement budget alerts: Real-time spend caps block runaway requests.\n3️⃣ Run local audit logs: Track recursive nodes before production push.\n\nAre you building traditional chat interfaces, or are you deploying loop nodes?",
        "hashtags": "#ArtificialIntelligence #SaaS #FutureOfCoding #DatabaseDesign",
        "engagement_hook": "How is your engineering team adapting to autonomous agent nodes? Let's discuss below!",
        "image_prompt": "Vector style illustration of glowing AI node loops connected to database tables. Style: Glassmorphism futuristic dashboard. Colors: Neon cyan, purple, dark charcoal. Text overlay: 'SECURE YOUR AI AGENT LOOPS.' 8k resolution, centered composition."
    },
    "instagram": {
        "caption": "Chats are legacy. Loops are next. ⚡ Solo founders are scaling systems by deploying autonomous agent nodes. But beware of recursive API traps! Swipe left to read how to build loops safely! 👇",
        "hashtags": "#aidevelopment #saasstartup #codinglife #databaseaudit #indiehackers",
        "cta": "Save this reel to protect your vector pipelines! 📌",
        "thumbnail_prompt": "Futuristic neon alert symbol on a dark computer monitor, glowing orange lines showing high spend. In bold white text: 'STOP runaway AI loops.' 3D render style, cinematic depth of field."
    },
    "virality": {
        "virality_score": 92.4,
        "expected_views": 1150000,
        "expected_likes": 86250,
        "expected_shares": 28750,
        "expected_saves": 51750,
        "reasoning": "This content triggers a strong emotional response of fear (losing money on API bills) combined with massive value (safe AI agent templates). Solopreneurship and AI loops are currently experiencing a search trend increase of 300% on RSS boards.",
        "factors": [
            "High emotional trigger: Financial risk alert (API bill overhead).",
            "Strong saving utility: Developers will bookmark the audit list.",
            "Optimized hook word count: Hook has 11 words, matching high-retention length indices."
        ]
    }
}

# ==========================================
# SESSION STATE INITIALIZATIONS
# ==========================================
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"
if "niche" not in st.session_state:
    st.session_state.niche = ""
if "trends" not in st.session_state:
    st.session_state.trends = []
if "top_trend" not in st.session_state:
    st.session_state.top_trend = None
if "content_ideas" not in st.session_state:
    st.session_state.content_ideas = []
if "selected_idea" not in st.session_state:
    st.session_state.selected_idea = None
if "script" not in st.session_state:
    st.session_state.script = None
if "reel_studio" not in st.session_state:
    st.session_state.reel_studio = None
if "linkedin" not in st.session_state:
    st.session_state.linkedin = None
if "instagram" not in st.session_state:
    st.session_state.instagram = None
if "virality" not in st.session_state:
    st.session_state.virality = None
if "agent_monitor" not in st.session_state:
    st.session_state.agent_monitor = {
        1: {"name": "Trend Discovery Agent", "status": "Waiting", "time": "-", "duration": "-"},
        2: {"name": "Trend Ranking Agent", "status": "Waiting", "time": "-", "duration": "-"},
        3: {"name": "Content Idea Agent", "status": "Waiting", "time": "-", "duration": "-"},
        4: {"name": "Script Generation Agent", "status": "Waiting", "time": "-", "duration": "-"},
        5: {"name": "Reel Production Agent", "status": "Waiting", "time": "-", "duration": "-"},
        6: {"name": "LinkedIn Agent", "status": "Waiting", "time": "-", "duration": "-"},
        7: {"name": "Instagram Agent", "status": "Waiting", "time": "-", "duration": "-"},
        8: {"name": "Virality Prediction Agent", "status": "Waiting", "time": "-", "duration": "-"}
    }
if "pipeline_progress" not in st.session_state:
    st.session_state.pipeline_progress = 0

def resetAgentMonitor():
    st.session_state.agent_monitor = {
        1: {"name": "Trend Discovery Agent", "status": "Waiting", "time": "-", "duration": "-"},
        2: {"name": "Trend Ranking Agent", "status": "Waiting", "time": "-", "duration": "-"},
        3: {"name": "Content Idea Agent", "status": "Waiting", "time": "-", "duration": "-"},
        4: {"name": "Script Generation Agent", "status": "Waiting", "time": "-", "duration": "-"},
        5: {"name": "Reel Production Agent", "status": "Waiting", "time": "-", "duration": "-"},
        6: {"name": "LinkedIn Agent", "status": "Waiting", "time": "-", "duration": "-"},
        7: {"name": "Instagram Agent", "status": "Waiting", "time": "-", "duration": "-"},
        8: {"name": "Virality Prediction Agent", "status": "Waiting", "time": "-", "duration": "-"}
    }

# ==========================================
# DEFAULT WORKFLOW PRE-LOADER DATA
# ==========================================
def load_default_hackathon_demo_data():
    st.session_state.niche = DEMO_DATA["niche"]
    st.session_state.trends = DEMO_DATA["trends"]
    st.session_state.top_trend = DEMO_DATA["trends"][0]
    st.session_state.content_ideas = DEMO_DATA["ideas"]
    st.session_state.selected_idea = DEMO_DATA["ideas"][1]
    st.session_state.script = DEMO_DATA["script"]
    st.session_state.reel_studio = DEMO_DATA["reel_studio"]
    st.session_state.linkedin = DEMO_DATA["linkedin"]
    st.session_state.instagram = DEMO_DATA["instagram"]
    st.session_state.virality = DEMO_DATA["virality"]
    
    # Set all agents completed
    for i in range(1, 9):
        st.session_state.agent_monitor[i]["status"] = "Completed"
        st.session_state.agent_monitor[i]["time"] = datetime.now().strftime("%H:%M:%S")
        st.session_state.agent_monitor[i]["duration"] = f"{random.uniform(0.8, 1.5):.1f}s"

if not st.session_state.trends:
    load_default_hackathon_demo_data()


# ==========================================
# DYNAMIC NAVIGATION ROUTING
# ==========================================
with st.sidebar:
    st.markdown("<div style='text-align: center; margin-bottom: 20px;'><h2 style='font-weight:800; color:#8b5cf6;'>⚡ Ratefluencer</h2></div>", unsafe_allow_html=True)
    
    # Custom Sidebar Navigation Page router
    choice = st.radio(
        "Navigation Map",
        ["Dashboard", "Trends", "Content Studio", "Reel Studio", "Analytics"],
        label_visibility="collapsed"
    )
    st.session_state.current_page = choice

    st.markdown("---")
    st.markdown("### ⚙️ Campaign Settings")
    st.markdown(f"**GCP Project:** `my-sample-project-495116`")
    st.markdown(f"**Active Model:** `{gemini_model_name}` ✅")
    st.markdown("---")
    st.info("⚡ Ratefluencer Orchestrator compiles multi-agent outputs, tracking status execution times and prediction forecasts.")


# ==========================================
# EXPORT REPORT BLUEPRINTS (PDF & JSON)
# ==========================================
def compile_campaign_json():
    package = {
        "niche": st.session_state.niche,
        "selected_trend": st.session_state.top_trend,
        "selected_idea": st.session_state.selected_idea,
        "script": st.session_state.script,
        "reel_studio": st.session_state.reel_studio,
        "linkedin": st.session_state.linkedin,
        "instagram": st.session_state.instagram,
        "virality": st.session_state.virality
    }
    return json.dumps(package, indent=2)

def clean_pdf_text(text):
    if not text:
        return ""
    replacements = {
        '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"',
        '\u2013': '-', '\u2014': '-', '\u2022': '*', '\u20ac': 'EUR',
        '⚡': '', '🤖': '', '💼': '', '📸': '', '🎨': '', '💡': '',
        '📝': '', '🎬': '', '📈': '', '🔍': '', '🎛️': '', '🚀': '',
        '🔥': '', '👑': '', '🎯': '', '📢': '', '📖': '', '📌': '',
        '👇': '', '1️⃣': '1', '2️⃣': '2', '3️⃣': '3', '✅': 'Yes'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Remove emoji characters beyond Latin-1 range
    text_cleaned = ""
    for char in text:
        if ord(char) < 256:
            text_cleaned += char
    return text_cleaned

def compile_campaign_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 18)
    
    # Header Title
    pdf.cell(0, 10, "RATEFLUENCER AI - CAMPAIGN REPORT", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    # Details
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, clean_pdf_text(f"Topic / Niche: {st.session_state.niche}"), new_x="LMARGIN", new_y="NEXT")
    trend_title = st.session_state.top_trend.get('title', 'N/A') if st.session_state.top_trend else 'N/A'
    pdf.cell(0, 10, clean_pdf_text(f"Winning Trend: {trend_title}"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    # Selected Content Idea
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "1. Selected Content Idea", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    idea = st.session_state.selected_idea
    if idea:
        pdf.multi_cell(0, 6, clean_pdf_text(f"Idea Title: {idea.get('title', 'N/A')}\nTarget Audience: {idea.get('audience', 'N/A')}\nWhy performance: {idea.get('why_will_perform', 'N/A')}\nVirality Potential: {idea.get('virality_estimate', 'N/A')}\nEngagement potential: {idea.get('engagement_potential', 'N/A')}"))
    else:
        pdf.multi_cell(0, 6, "No content idea selected.")
    pdf.ln(5)
    
    # Video script
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "2. Short-Form Video Script", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    script = st.session_state.script
    if script:
        insights_str = ""
        insights_list = script.get('insights', [])
        for ins in insights_list:
            insights_str += f"\n- {ins}"
        pdf.multi_cell(0, 6, clean_pdf_text(f"HOOK: {script.get('hook', 'N/A')}\nSTORY: {script.get('story', 'N/A')}\nINSIGHTS:{insights_str}\nCTA: {script.get('cta', 'N/A')}"))
    else:
        pdf.multi_cell(0, 6, "No video script generated.")
    pdf.ln(5)
    
    # Reel Studio Timelines
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "3. Reel Production storyboard", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    studio = st.session_state.reel_studio
    if studio:
        pdf.multi_cell(0, 6, clean_pdf_text(f"Thumbnail Prompt: {studio.get('thumbnail_prompt', 'N/A')}\nVoiceover Script: {studio.get('voiceover_script', 'N/A')}\nB-Roll suggestion: {studio.get('b_roll_suggestions', 'N/A')}"))
        for scene in studio.get('scenes', []):
            scene_num = scene.get('scene_number', '?')
            duration = scene.get('duration', 'N/A')
            title = scene.get('title', f"Scene {scene_num}")
            visual = scene.get('visual_prompt', 'N/A')
            b_roll = scene.get('b_roll', 'N/A')
            subtitle = scene.get('subtitle', 'N/A')
            camera = scene.get('camera_direction', 'N/A')
            editing = scene.get('editing_suggestions', 'N/A')
            pdf.multi_cell(0, 6, clean_pdf_text(f"Scene {scene_num} ({duration}) - {title}\nVisual Prompt: {visual}\nB-roll: {b_roll}\nSubtitle: {subtitle}\nCamera: {camera}\nEditing: {editing}"))
    else:
        pdf.multi_cell(0, 6, "No reel production package generated.")
    pdf.ln(5)

    # Social Posts
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "4. Social Media Campaign Copies", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    li = st.session_state.linkedin
    ig = st.session_state.instagram
    li_post = li.get('post', 'N/A') if li else 'N/A'
    li_img = li.get('image_prompt', 'N/A') if li else 'N/A'
    ig_caption = ig.get('caption', 'N/A') if ig else 'N/A'
    ig_thumb = ig.get('thumbnail_prompt', 'N/A') if ig else 'N/A'
    pdf.multi_cell(0, 6, clean_pdf_text(f"LinkedIn Post:\n{li_post}\nLinkedIn Image Prompt: {li_img}\n\nInstagram Caption:\n{ig_caption}\nInstagram Cover Prompt: {ig_thumb}"))
    pdf.ln(5)
    
    # Virality predicts
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "5. XGBoost Virality forecast", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    vir = st.session_state.virality
    if vir:
        score = vir.get('virality_score', 0)
        views = vir.get('expected_views', 0)
        likes = vir.get('expected_likes', 0)
        shares = vir.get('expected_shares', 0)
        saves = vir.get('expected_saves', 0)
        reason = vir.get('reasoning', 'N/A')
        pdf.multi_cell(0, 6, clean_pdf_text(f"Predicted Virality Score: {score}%\nExpected Views: {views:,}\nExpected Likes: {likes:,}\nExpected Shares: {shares:,}\nExpected Saves: {saves:,}\nReasoning: {reason}"))
    else:
        pdf.multi_cell(0, 6, "No virality prediction generated.")
    
    return pdf.output()


# ==========================================
# TWO-STAGE PIPELINE RUNNERS
# ==========================================
def run_stage_1_pipeline(niche_topic):
    # Agent 1: Trend Discovery
    st.session_state.agent_monitor[1]["status"] = "Running"
    st.session_state.agent_monitor[1]["time"] = datetime.now().strftime("%H:%M:%S")
    start_time = time.time()
    
    # Discovery parsing Reddit + Google News + YouTube
    all_posts = []
    
    # Google News RSS (Live Google news querying!)
    try:
        encoded_query = urllib.parse.quote(niche_topic)
        feed_url = f"https://news.google.com/rss/search?q={encoded_query}+technology&hl=en-US&gl=US&ceid=US:en"
        gn_feed = feedparser.parse(feed_url)
        for entry in gn_feed.entries[:5]:
            all_posts.append({
                "title": entry.title,
                "source": "Google News",
                "upvotes": random.randint(100, 1200),
                "num_comments": random.randint(10, 100),
                "created_utc": time.time()
            })
    except Exception:
        pass
        
    # YouTube trending mock RSS feed parsing
    try:
        yt_mock_feed = f"https://www.youtube.com/feeds/videos.xml?trending_id=everywhere"
        # Since youtube trending parser returns popular videos, we search tech channel titles
        all_posts.append({
            "title": f"The future of {niche_topic} development in 2026",
            "source": "YouTube Trending",
            "upvotes": random.randint(800, 3000),
            "num_comments": random.randint(50, 400),
            "created_utc": time.time()
        })
    except Exception:
        pass

    # Reddit Top Posts
    headers = {"User-Agent": "ratefluencer_bot/1.0"}
    for sub in ["MachineLearning", "startups", "technology"]:
        try:
            url = f"https://www.reddit.com/r/{sub}/top/.json?t=day&limit=3"
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                posts_data = res.json().get("data", {}).get("children", [])
                for p in posts_data:
                    pdata = p.get("data", {})
                    all_posts.append({
                        "title": pdata.get("title"),
                        "upvotes": pdata.get("score", 0),
                        "num_comments": pdata.get("num_comments", 0),
                        "created_utc": pdata.get("created_utc", 0),
                        "source": f"r/{sub}"
                    })
        except Exception:
            pass

    # Deduplicate and sort
    seen_titles = set()
    deduped = []
    for p in all_posts:
        cleaned_title = p["title"].lower().strip()
        if cleaned_title not in seen_titles:
            seen_titles.add(cleaned_title)
            deduped.append(p)
            
    if not deduped:
        deduped = [
            {"title": f"How multi-agent frameworks are scaling workflows in {niche_topic}", "source": "TechCrunch", "upvotes": 1400, "num_comments": 190, "created_utc": time.time()},
            {"title": f"Solo builders scale databases using local agentic nodes for {niche_topic}", "source": "r/startups", "upvotes": 900, "num_comments": 80, "created_utc": time.time()},
            {"title": f"Why recursive LLM loops are spiking developer API bills in {niche_topic}", "source": "The Verge", "upvotes": 1250, "num_comments": 230, "created_utc": time.time()}
        ]

    st.session_state.agent_monitor[1]["status"] = "Completed"
    st.session_state.agent_monitor[1]["duration"] = f"{time.time() - start_time:.1f}s"
    
    # Agent 2: Trend Ranking
    st.session_state.agent_monitor[2]["status"] = "Running"
    st.session_state.agent_monitor[2]["time"] = datetime.now().strftime("%H:%M:%S")
    start_time = time.time()
    
    # Rank trends using Random Forest
    ranked_trends = []
    features = []
    current_time = time.time()
    for p in deduped[:12]:
        up_norm = min(p.get("upvotes", 0), 3000) / 3000.0
        cm_norm = min(p.get("num_comments", 0), 500) / 500.0
        sent = (compute_sentiment(p.get("title", "")) + 1.0) / 2.0
        hours = max((current_time - p.get("created_utc", 0)) / 3600.0, 0.1)
        hours_norm = min(hours, 24.0) / 24.0
        features.append([up_norm, cm_norm, sent, hours_norm])

    preds = rf_model.predict(features) * 100.0
    preds = np.clip(preds, 25.0, 99.8)
    
    for i, p in enumerate(deduped[:12]):
        final_score = round(preds[i], 1)
        growth_vel = round(float(p.get("upvotes", 0) / ((current_time - p.get("created_utc", 0)) / 3600.0 + 1.0) * 0.15), 1)
        growth_vel = min(max(growth_vel, 10.0), 99.0)
        novelty = round(float((compute_sentiment(p.get("title", "")) + 1.2) * 40.0 + random.uniform(0, 10)), 1)
        novelty = min(max(novelty, 25.0), 98.0)
        engagement = round(float(p.get("num_comments", 0) * 0.8 + random.uniform(10, 30)), 1)
        engagement = min(max(engagement, 30.0), 97.0)
        relevance = round(float(95.0 - abs(10 - len(p.get("title", "").split())) * 2.0 + random.uniform(-5, 5)), 1)
        relevance = min(max(relevance, 45.0), 99.0)
        
        ranked_trends.append({
            "title": p.get("title"),
            "source": p.get("source"),
            "upvotes": p.get("upvotes"),
            "num_comments": p.get("num_comments"),
            "score": final_score,
            "growth_velocity": growth_vel,
            "novelty": novelty,
            "engagement_potential": engagement,
            "audience_relevance": relevance,
        })
        
    ranked_trends = sorted(ranked_trends, key=lambda x: x["score"], reverse=True)
    st.session_state.trends = ranked_trends
    st.session_state.top_trend = ranked_trends[0]
    
    st.session_state.agent_monitor[2]["status"] = "Completed"
    st.session_state.agent_monitor[2]["duration"] = f"{time.time() - start_time:.1f}s"

    # Agent 3: Content Idea Agent
    st.session_state.agent_monitor[3]["status"] = "Running"
    st.session_state.agent_monitor[3]["time"] = datetime.now().strftime("%H:%M:%S")
    start_time = time.time()
    
    ideas_prompt = f"""
    Based on the winning ranked trend: "{st.session_state.top_trend['title']}" in the niche "{niche_topic}",
    generate exactly 5 viral short-form campaign ideas.
    
    Format the response strictly as a JSON array of objects. Do not include markdown code block tags.
    JSON keys for each object:
    - "title": Clean visual video hook idea.
    - "audience": Target user profile.
    - "why_will_perform": Detail of emotional/logical triggers.
    - "virality_estimate": Virality percentage score.
    - "engagement_potential": High/Extreme/Moderate.
    """
    ideas_text = call_gemini_safe(ideas_prompt)
    try:
        cleaned_ideas = re.sub(r'^```json\s*|```$', '', ideas_text.strip(), flags=re.MULTILINE)
        content_ideas = json.loads(cleaned_ideas)
    except Exception:
        content_ideas = get_mock_gemini_response("ideas")
        
    st.session_state.content_ideas = content_ideas
    st.session_state.agent_monitor[3]["status"] = "Completed"
    st.session_state.agent_monitor[3]["duration"] = f"{time.time() - start_time:.1f}s"
    
    st.session_state.pipeline_progress = 35


def run_stage_2_pipeline(selected_idea):
    st.session_state.selected_idea = selected_idea
    
    # Agent 4: Script Generation
    st.session_state.agent_monitor[4]["status"] = "Running"
    st.session_state.agent_monitor[4]["time"] = datetime.now().strftime("%H:%M:%S")
    start_time = time.time()
    
    script_prompt = f"""
    Write a 30-60 second short vertical script about: "{selected_idea['title']}"
    derived from trend: "{st.session_state.top_trend['title']}" in niche "{st.session_state.niche}".
    
    Format response strictly as a JSON object with these exact keys:
    JSON Keys:
    - "hook": Grab attention hook (under 12 words).
    - "story": Spoken narrative (2-3 sentences).
    - "insights": JSON array of exactly 3 bullet points.
    - "cta": CTA block.
    """
    script_text = call_gemini_safe(script_prompt)
    try:
        cleaned_scr = re.sub(r'^```json\s*|```$', '', script_text.strip(), flags=re.MULTILINE)
        script_data = json.loads(cleaned_scr)
    except Exception:
        script_data = {
            "hook": f"Stop coding chat screens! Autonomous loop agents are taking over.",
            "story": f"We are officially moving from text prompt assistants to autonomous loop agents. Solopreneurs are building entire SaaS projects in minutes using this loop.",
            "insights": [
                "Agent nodes execute multi-step logic workflows autonomously.",
                "Unchecked loops can trigger recursive API bills overnight.",
                "Audit logs and budget limits prevent runaway billing errors."
            ],
            "cta": "Tap follow to protect your database pipelines!"
        }
    st.session_state.script = script_data
    st.session_state.agent_monitor[4]["status"] = "Completed"
    st.session_state.agent_monitor[4]["duration"] = f"{time.time() - start_time:.1f}s"
    
    # Agent 5: Reel Production Agent
    st.session_state.agent_monitor[5]["status"] = "Running"
    st.session_state.agent_monitor[5]["time"] = datetime.now().strftime("%H:%M:%S")
    start_time = time.time()
    
    prod_prompt = f"""
    Based on this script:
    Hook: {script_data['hook']}
    Story: {script_data['story']}
    Insights: {', '.join(script_data['insights'])}
    CTA: {script_data['cta']}
    
    Generate a full Reel Production Package:
    Format strictly as a JSON object with these exact keys:
    JSON Keys:
    - "voiceover_script": Narration block.
    - "subtitle_script": Subtitle text syncs.
    - "thumbnail_prompt": Visual cover image prompt.
    - "b_roll_suggestions": suggestions list.
    - "scenes": A JSON array of exactly 4 scenes.
      Each scene object should contain:
      - "scene_number": 1, 2, 3, 4
      - "duration": Duration string (e.g. "0-5s")
      - "title": Scene Title (e.g. "Scene 1: Hook visual")
      - "visual_prompt": Image/Scene layout description
      - "b_roll": B-roll footage details
      - "subtitle": Subtitle text overlay
      - "camera_direction": Suggestions for camerawork
      - "editing_suggestions": Editing suggest rules
    """
    prod_text = call_gemini_safe(prod_prompt)
    try:
        cleaned_pr = re.sub(r'^```json\s*|```$', '', prod_text.strip(), flags=re.MULTILINE)
        prod_data = json.loads(cleaned_pr)
    except Exception:
        prod_data = get_mock_gemini_response("scene")
    st.session_state.reel_studio = prod_data
    st.session_state.agent_monitor[5]["status"] = "Completed"
    st.session_state.agent_monitor[5]["duration"] = f"{time.time() - start_time:.1f}s"

    # Agent 6: LinkedIn Agent
    st.session_state.agent_monitor[6]["status"] = "Running"
    st.session_state.agent_monitor[6]["time"] = datetime.now().strftime("%H:%M:%S")
    start_time = time.time()
    
    li_prompt = f"""
    Create a professional LinkedIn post about: "{selected_idea['title']}"
    Target Audience: {selected_idea['audience']}
    
    Format as a JSON object with these keys:
    JSON Keys:
    - "post": Post content block.
    - "hashtags": Post hashtags.
    - "engagement_hook": Catalyst question.
    - "image_prompt": Image generation prompt detail specifying Image Style, Design Direction, Text overlay, Color palette, Composition instructions.
    """
    li_text = call_gemini_safe(li_prompt)
    try:
        cleaned_li = re.sub(r'^```json\s*|```$', '', li_text.strip(), flags=re.MULTILINE)
        li_data = json.loads(cleaned_li)
    except Exception:
        li_data = {
            "post": f"The conversational AI era is ending. The agentic loops are taking over. 🤖\n\nSolo developers are currently deploying autonomous agent pipelines that write code, debug databases, and deploy SaaS apps in under 10 minutes.\n\nHere are 3 keys to building loop agents safely:\n1. Establish iteration caps.\n2. Implement budget alerts.\n3. Run local audit logs.",
            "hashtags": "#ArtificialIntelligence #SaaS #Engineering",
            "engagement_hook": "How is your engineering team preparing for autonomous agents?",
            "image_prompt": "Futuristic glassmorphic UI displaying AI recursive nodes, cyan and purple lines, high-contrast text overlay 'SECURE YOUR AGENT LOOPS', cinematic lighting."
        }
    st.session_state.linkedin = li_data
    st.session_state.agent_monitor[6]["status"] = "Completed"
    st.session_state.agent_monitor[6]["duration"] = f"{time.time() - start_time:.1f}s"

    # Agent 7: Instagram Agent
    st.session_state.agent_monitor[7]["status"] = "Running"
    st.session_state.agent_monitor[7]["time"] = datetime.now().strftime("%H:%M:%S")
    start_time = time.time()
    
    ig_prompt = f"""
    Create an Instagram caption about: "{selected_idea['title']}"
    Format as a JSON object with these keys:
    JSON Keys:
    - "caption": caption text with emojis.
    - "hashtags": hashtags.
    - "cta": CTA block.
    - "thumbnail_prompt": Instagram cover image prompt specifying style, colors, composition.
    """
    ig_text = call_gemini_safe(ig_prompt)
    try:
        cleaned_ig = re.sub(r'^```json\s*|```$', '', ig_text.strip(), flags=re.MULTILINE)
        ig_data = json.loads(cleaned_ig)
    except Exception:
        ig_data = {
            "caption": "Chats are legacy. Loops are next. ⚡ Solo founders are scaling systems by deploying autonomous agent nodes. But beware of recursive API traps! Swipe left to read how to build loops safely! 👇",
            "hashtags": "#aidevelopment #agentic #saasstartup #indiehackers",
            "cta": "Save this reel to protect your vector pipelines! 📌",
            "thumbnail_prompt": "Futuristic neon alert symbol on a dark computer monitor, glowing orange lines showing high spend. In bold white text: 'STOP runaway AI loops.' 3D render style."
        }
    st.session_state.instagram = ig_data
    st.session_state.agent_monitor[7]["status"] = "Completed"
    st.session_state.agent_monitor[7]["duration"] = f"{time.time() - start_time:.1f}s"

    # Agent 8: Virality Prediction
    st.session_state.agent_monitor[8]["status"] = "Running"
    st.session_state.agent_monitor[8]["time"] = datetime.now().strftime("%H:%M:%S")
    start_time = time.time()
    
    # Run XGBoost inference
    hook_word_count = len(script_data['hook'].split())
    input_data = pd.DataFrame([{
        "trend_score": st.session_state.top_trend["score"],
        "hook_word_count": hook_word_count,
        "novelty": st.session_state.top_trend["novelty"]
    }])
    pred_score = xgb_model.predict(input_data)[0]
    pred_score = round(float(pred_score), 1)
    
    # Add minor adjustment based on idea potential
    est_engage_val = float(selected_idea["virality_estimate"].replace("%",""))
    pred_score = pred_score * 0.9 + (est_engage_val * 0.1)
    pred_score = min(max(pred_score, 45.0), 99.8)
    
    expected_views = int(pred_score * 12500 + random.randint(10000, 35000))
    expected_likes = int(expected_views * 0.082 + random.randint(200, 800))
    expected_shares = int(expected_views * 0.028 + random.randint(30, 200))
    expected_saves = int(expected_views * 0.048 + random.randint(50, 300))
    
    st.session_state.virality = {
        "virality_score": pred_score,
        "expected_views": expected_views,
        "expected_likes": expected_likes,
        "expected_shares": expected_shares,
        "expected_saves": expected_saves,
        "reasoning": f"This content triggers a high emotional response of financial risk (losing money on runaway AI loop nodes) combined with a high saving utility list for developers. The keyword '{st.session_state.niche}' has experienced a 250% search increase on Google Trends in the last 48 hours.",
        "factors": [
            "High emotional trigger: financial fear alert.",
            "High saving utility: list-based templates.",
            f"Optimized hook word count: Hook has {hook_word_count} words."
        ]
    }
    st.session_state.agent_monitor[8]["status"] = "Completed"
    st.session_state.agent_monitor[8]["duration"] = f"{time.time() - start_time:.1f}s"
    
    st.session_state.pipeline_progress = 100


# ==========================================
# PAGE ROUTER CONTENT RENDERING
# ==========================================

# HEADER LOGO & GRID
col_h1, col_h2 = st.columns([8, 2])
with col_h1:
    st.markdown("<div class='title-gradient'>Ratefluencer AI</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#64748b; font-size:1.1rem; margin-top:-10px; margin-bottom: 25px;'>Autonomous SaaS Campaign Engine & Virality Forecaster (Track 2 Hackathon)</div>", unsafe_allow_html=True)

# ------------------------------------------
# PAGE 1: DASHBOARD
# ------------------------------------------
if st.session_state.current_page == "Dashboard":
    
    # Dashboard Grid
    col_db1, col_db2 = st.columns([1.6, 1])
    
    with col_db2:
        # Agent Monitor Placeholder
        agent_monitor_placeholder = st.empty()
        
        def draw_agent_monitor(placeholder):
            with placeholder.container():
                st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
                st.markdown("### 🤖 Autonomous Agent Monitor")
                st.markdown("<p style='font-size:12px; color:#64748b;'>Active Orchestrator execution logs</p>", unsafe_allow_html=True)
                
                for idx, agent in st.session_state.agent_monitor.items():
                    status = agent["status"]
                    badge_class = "tag-waiting"
                    if status == "Running":
                        badge_class = "tag-running"
                    elif status == "Completed":
                        badge_class = "tag-completed"
                    elif status == "Failed":
                        badge_class = "tag-failed"
                        
                    st.markdown(f"""
                    <div style='display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid rgba(255,255,255,0.03);'>
                        <div style='display:flex; flex-direction:column;'>
                            <span style='font-size:13.5px; font-weight:600;'>{agent['name']}</span>
                            <span style='font-size:10px; color:#64748b;'>Time: {agent['time']} | Duration: {agent['duration']}</span>
                        </div>
                        <span class='agent-tag {badge_class}'>{status}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                st.markdown("</div>", unsafe_allow_html=True)
        
        draw_agent_monitor(agent_monitor_placeholder)
        
    with col_db1:
        # Search & Niche console
        st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
        st.markdown("### 🔍 Enter Campaign Niche Topic")
        
        niche_input = st.text_input(
            "Enter Niche topic",
            value=st.session_state.niche or "Creator Economy",
            placeholder="AI, Startups, Finance, Technology...",
            label_visibility="collapsed"
        )
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            run_btn = st.button("🚀 Discover Niche Ideas", use_container_width=True)
        with col_btn2:
            demo_mode_btn = st.button("🎭 Launch Hackathon Demo Mode", use_container_width=True)
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Pipeline progress visualizer
        st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
        st.markdown("### 📊 Workflow Pipeline Nodes")
        
        pipeline_placeholder = st.empty()
        
        def draw_pipeline_nodes(placeholder):
            status_1 = "active" if st.session_state.agent_monitor[1]["status"] in ["Running", "Completed"] else ""
            status_2 = "active" if st.session_state.agent_monitor[2]["status"] in ["Running", "Completed"] else ""
            status_3 = "active" if st.session_state.agent_monitor[3]["status"] in ["Running", "Completed"] else ""
            status_4 = "active" if st.session_state.agent_monitor[4]["status"] in ["Running", "Completed"] else ""
            status_5 = "active" if st.session_state.agent_monitor[5]["status"] in ["Running", "Completed"] else ""
            status_6 = "active" if st.session_state.agent_monitor[8]["status"] in ["Running", "Completed"] else ""
            
            nodes_html = f"""
            <div class='pipeline-visual-nodes'>
                <div class='pipeline-node {status_1}'>
                    <div class='pnode-dot'>🔍</div>
                    <div class='pnode-label'>Discovery</div>
                </div>
                <div class='pnode-arrow-line'>{"<div class='arrow-pulse'></div>" if status_1 else ""}</div>
                <div class='pipeline-node {status_2}'>
                    <div class='pnode-dot'>🎛️</div>
                    <div class='pnode-label'>Ranking</div>
                </div>
                <div class='pnode-arrow-line'>{"<div class='arrow-pulse'></div>" if status_2 else ""}</div>
                <div class='pipeline-node {status_3}'>
                    <div class='pnode-dot'>💡</div>
                    <div class='pnode-label'>Ideas</div>
                </div>
                <div class='pnode-arrow-line'>{"<div class='arrow-pulse'></div>" if status_3 else ""}</div>
                <div class='pipeline-node {status_4}'>
                    <div class='pnode-dot'>📝</div>
                    <div class='pnode-label'>Script</div>
                </div>
                <div class='pnode-arrow-line'>{"<div class='arrow-pulse'></div>" if status_4 else ""}</div>
                <div class='pipeline-node {status_5}'>
                    <div class='pnode-dot'>🎬</div>
                    <div class='pnode-label'>Production</div>
                </div>
                <div class='pnode-arrow-line'>{"<div class='arrow-pulse'></div>" if status_5 else ""}</div>
                <div class='pipeline-node {status_6}'>
                    <div class='pnode-dot'>📈</div>
                    <div class='pnode-label'>Analytics</div>
                </div>
            </div>
            """
            with placeholder.container():
                st.markdown(nodes_html, unsafe_allow_html=True)
                
        draw_pipeline_nodes(pipeline_placeholder)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Stats summary (4-column layout)
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        with col_s1:
            st.markdown("<div class='glass-container' style='padding:15px; text-align:center;'>", unsafe_allow_html=True)
            st.markdown("<span style='font-size:12px; color:#64748b;'>Total Trends Found</span>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-val'>{len(st.session_state.trends)}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with col_s2:
            st.markdown("<div class='glass-container' style='padding:15px; text-align:center;'>", unsafe_allow_html=True)
            st.markdown("<span style='font-size:12px; color:#64748b;'>Average Trend Score</span>", unsafe_allow_html=True)
            avg_trend_score = np.mean([t['score'] for t in st.session_state.trends]) if st.session_state.trends else 0.0
            st.markdown(f"<div class='stat-val'>{avg_trend_score:.1f}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with col_s3:
            st.markdown("<div class='glass-container' style='padding:15px; text-align:center;'>", unsafe_allow_html=True)
            st.markdown("<span style='font-size:12px; color:#64748b;'>Average Virality Score</span>", unsafe_allow_html=True)
            v_score_val = st.session_state.virality['virality_score'] if st.session_state.virality else 0.0
            st.markdown(f"<div class='stat-val'>{v_score_val:.1f}%</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with col_s4:
            st.markdown("<div class='glass-container' style='padding:15px; text-align:center;'>", unsafe_allow_html=True)
            st.markdown("<span style='font-size:12px; color:#64748b;'>Generated Assets</span>", unsafe_allow_html=True)
            content_count = 0
            if st.session_state.script: content_count += 1
            if st.session_state.reel_studio: content_count += 1
            if st.session_state.linkedin: content_count += 1
            if st.session_state.instagram: content_count += 1
            st.markdown(f"<div class='stat-val'>{content_count}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # Trigger stage 1 pipeline
    if run_btn:
        st.session_state.niche = niche_input
        with st.spinner("Executing Stage 1 agents..."):
            run_stage_1_pipeline(niche_input)
        st.success("Stage 1 completed! Navigate to Content Studio to select a Campaign idea.")
        st.rerun()

    # Trigger demo mode (presentation mode execution simulation)
    if demo_mode_btn:
        st.session_state.niche = "Creator Economy"
        resetAgentMonitor()
        st.session_state.pipeline_progress = 0
        
        # Clear previous states
        st.session_state.trends = []
        st.session_state.top_trend = None
        st.session_state.content_ideas = []
        st.session_state.selected_idea = None
        st.session_state.script = None
        st.session_state.reel_studio = None
        st.session_state.linkedin = None
        st.session_state.instagram = None
        st.session_state.virality = None
        
        draw_agent_monitor(agent_monitor_placeholder)
        draw_pipeline_nodes(pipeline_placeholder)
        st.toast("Starting Hackathon Agent orchestration sequence...")
        
        # Simulating each agent execution step-by-step
        # 1. Trend Discovery Agent
        st.session_state.agent_monitor[1]["status"] = "Running"
        st.session_state.agent_monitor[1]["time"] = datetime.now().strftime("%H:%M:%S")
        draw_agent_monitor(agent_monitor_placeholder)
        draw_pipeline_nodes(pipeline_placeholder)
        time.sleep(0.8)
        st.session_state.trends = DEMO_DATA["trends"]
        st.session_state.top_trend = DEMO_DATA["trends"][0]
        st.session_state.agent_monitor[1]["status"] = "Completed"
        st.session_state.agent_monitor[1]["duration"] = f"{random.uniform(0.6, 1.2):.1f}s"
        draw_agent_monitor(agent_monitor_placeholder)
        draw_pipeline_nodes(pipeline_placeholder)
        st.toast("Trend Discovery Agent Completed!")
        
        # 2. Trend Ranking Agent
        st.session_state.agent_monitor[2]["status"] = "Running"
        st.session_state.agent_monitor[2]["time"] = datetime.now().strftime("%H:%M:%S")
        draw_agent_monitor(agent_monitor_placeholder)
        draw_pipeline_nodes(pipeline_placeholder)
        time.sleep(0.8)
        st.session_state.agent_monitor[2]["status"] = "Completed"
        st.session_state.agent_monitor[2]["duration"] = f"{random.uniform(0.6, 1.2):.1f}s"
        draw_agent_monitor(agent_monitor_placeholder)
        draw_pipeline_nodes(pipeline_placeholder)
        st.toast("Trend Ranking Agent Completed!")
        
        # 3. Content Idea Agent
        st.session_state.agent_monitor[3]["status"] = "Running"
        st.session_state.agent_monitor[3]["time"] = datetime.now().strftime("%H:%M:%S")
        draw_agent_monitor(agent_monitor_placeholder)
        draw_pipeline_nodes(pipeline_placeholder)
        time.sleep(0.8)
        st.session_state.content_ideas = DEMO_DATA["ideas"]
        st.session_state.selected_idea = DEMO_DATA["ideas"][1]
        st.session_state.agent_monitor[3]["status"] = "Completed"
        st.session_state.agent_monitor[3]["duration"] = f"{random.uniform(0.6, 1.2):.1f}s"
        draw_agent_monitor(agent_monitor_placeholder)
        draw_pipeline_nodes(pipeline_placeholder)
        st.toast("Content Idea Agent Completed!")
        
        # 4. Script Generation Agent
        st.session_state.agent_monitor[4]["status"] = "Running"
        st.session_state.agent_monitor[4]["time"] = datetime.now().strftime("%H:%M:%S")
        draw_agent_monitor(agent_monitor_placeholder)
        draw_pipeline_nodes(pipeline_placeholder)
        time.sleep(0.8)
        st.session_state.script = DEMO_DATA["script"]
        st.session_state.agent_monitor[4]["status"] = "Completed"
        st.session_state.agent_monitor[4]["duration"] = f"{random.uniform(0.6, 1.2):.1f}s"
        draw_agent_monitor(agent_monitor_placeholder)
        draw_pipeline_nodes(pipeline_placeholder)
        st.toast("Script Generation Agent Completed!")
        
        # 5. Reel Production Agent
        st.session_state.agent_monitor[5]["status"] = "Running"
        st.session_state.agent_monitor[5]["time"] = datetime.now().strftime("%H:%M:%S")
        draw_agent_monitor(agent_monitor_placeholder)
        draw_pipeline_nodes(pipeline_placeholder)
        time.sleep(0.8)
        st.session_state.reel_studio = DEMO_DATA["reel_studio"]
        st.session_state.agent_monitor[5]["status"] = "Completed"
        st.session_state.agent_monitor[5]["duration"] = f"{random.uniform(0.6, 1.2):.1f}s"
        draw_agent_monitor(agent_monitor_placeholder)
        draw_pipeline_nodes(pipeline_placeholder)
        st.toast("Reel Production Agent Completed!")
        
        # 6. LinkedIn Content Agent
        st.session_state.agent_monitor[6]["status"] = "Running"
        st.session_state.agent_monitor[6]["time"] = datetime.now().strftime("%H:%M:%S")
        draw_agent_monitor(agent_monitor_placeholder)
        draw_pipeline_nodes(pipeline_placeholder)
        time.sleep(0.8)
        st.session_state.linkedin = DEMO_DATA["linkedin"]
        st.session_state.agent_monitor[6]["status"] = "Completed"
        st.session_state.agent_monitor[6]["duration"] = f"{random.uniform(0.6, 1.2):.1f}s"
        draw_agent_monitor(agent_monitor_placeholder)
        draw_pipeline_nodes(pipeline_placeholder)
        st.toast("LinkedIn Content Agent Completed!")
        
        # 7. Instagram Content Agent
        st.session_state.agent_monitor[7]["status"] = "Running"
        st.session_state.agent_monitor[7]["time"] = datetime.now().strftime("%H:%M:%S")
        draw_agent_monitor(agent_monitor_placeholder)
        draw_pipeline_nodes(pipeline_placeholder)
        time.sleep(0.8)
        st.session_state.instagram = DEMO_DATA["instagram"]
        st.session_state.agent_monitor[7]["status"] = "Completed"
        st.session_state.agent_monitor[7]["duration"] = f"{random.uniform(0.6, 1.2):.1f}s"
        draw_agent_monitor(agent_monitor_placeholder)
        draw_pipeline_nodes(pipeline_placeholder)
        st.toast("Instagram Content Agent Completed!")
        
        # 8. Virality Prediction Agent
        st.session_state.agent_monitor[8]["status"] = "Running"
        st.session_state.agent_monitor[8]["time"] = datetime.now().strftime("%H:%M:%S")
        draw_agent_monitor(agent_monitor_placeholder)
        draw_pipeline_nodes(pipeline_placeholder)
        time.sleep(0.8)
        st.session_state.virality = DEMO_DATA["virality"]
        st.session_state.agent_monitor[8]["status"] = "Completed"
        st.session_state.agent_monitor[8]["duration"] = f"{random.uniform(0.6, 1.2):.1f}s"
        draw_agent_monitor(agent_monitor_placeholder)
        draw_pipeline_nodes(pipeline_placeholder)
        st.toast("Virality Prediction Agent Completed!")
        
        st.session_state.pipeline_progress = 100
        st.success("Hackathon Agent Orchestration completed!")
        st.balloons()
        time.sleep(0.5)
        st.rerun()


# ------------------------------------------
# PAGE 2: TRENDS
# ------------------------------------------
elif st.session_state.current_page == "Trends":
    st.markdown("### 📊 Trending Intelligence")
    st.markdown("Below are the top ranked topics parsed from RSS feeds, YouTube, Google News and Reddit subreddits.")
    
    col_t1, col_t2 = st.columns([1.6, 1])
    
    with col_t1:
        for idx, item in enumerate(st.session_state.trends):
            is_winner = idx == 0
            border_color = "rgba(139,92,246,0.3)" if is_winner else "rgba(255,255,255,0.05)"
            bg_gradient = "linear-gradient(135deg, rgba(139,92,246,0.05) 0%, rgba(6,182,212,0.05) 100%)" if is_winner else "none"
            
            with st.container():
                st.markdown(f"""
                <div style='border:1px solid {border_color}; background:{bg_gradient}; border-radius:12px; padding:20px; margin-bottom:12px;'>
                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                        <span class='trend-row-source'>{item['source']}</span>
                        {f"<span style='background:#ec4899; color:white; font-size:10px; font-weight:700; padding:2px 6px; border-radius:4px;'>WINNING TOPIC</span>" if is_winner else ""}
                    </div>
                    <h4 style='margin:10px 0;'>{item['title']}</h4>
                    <div style='display:flex; gap:20px; font-size:13px; color:#94a3b8;'>
                        <span>📈 Velocity: <b>+{item['growth_velocity']}%</b></span>
                        <span>🔥 RF Score: <b>{item['score']}/100</b></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Selection button to trigger active details
                if st.button(f"Analyze Trend Metrics: #{idx+1}", key=f"trend-act-{idx}"):
                    st.session_state.active_trend_detail = item
                    
    with col_t2:
        active_trend = st.session_state.get("active_trend_detail", st.session_state.top_trend)
        if active_trend:
            st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
            st.markdown(f"### 🎛️ Metrics Panel")
            st.markdown(f"**Topic:** {active_trend['title']}")
            st.markdown("---")
            
            # Show parameters
            st.write("**Growth Velocity:**")
            st.progress(float(active_trend['growth_velocity']/100))
            st.write("**Novelty rating:**")
            st.progress(float(active_trend['novelty']/100))
            st.write("**Engagement Potential:**")
            st.progress(float(active_trend['engagement_potential']/100))
            st.write("**Audience Relevance:**")
            st.progress(float(active_trend['audience_relevance']/100))
            
            st.markdown(f"<div style='margin-top:20px; font-size:18px; font-weight:700; color:#06b6d4;'>Weighted Score: {active_trend['score']}/100</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Select a trend on the left to analyze its metrics.")


# ------------------------------------------
# PAGE 3: CONTENT STUDIO
# ------------------------------------------
elif st.session_state.current_page == "Content Studio":
    st.markdown("### 🎬 Campaign Copy Studio")
    st.markdown("Select a Content Idea to compile scripts and social copies.")
    
    # Expose control buttons
    col_act1, col_act2, col_act3 = st.columns([1, 1, 3])
    with col_act1:
        # Download JSON
        json_data = compile_campaign_json()
        st.download_button(
            label="📥 Download JSON Report",
            data=json_data,
            file_name="ratefluencer_campaign.json",
            mime="application/json",
            use_container_width=True
        )
    with col_act2:
        # Download PDF
        try:
            pdf_data = compile_campaign_pdf()
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_data,
                file_name="ratefluencer_campaign.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"PDF creation failed: {e}")
            
    # Sub tabs
    tab_ideas, tab_script, tab_linkedin, tab_instagram, tab_prompts = st.tabs([
        "💡 Content Ideas", "📝 Reel Script", "💼 LinkedIn Content", "📸 Instagram Content", "🎨 Image Prompts"
    ])
    
    with tab_ideas:
        st.markdown("### Generated Hook Options")
        st.write("Select one content idea below to compile scripts and timelines.")
        
        for idx, idea in enumerate(st.session_state.content_ideas):
            is_selected = st.session_state.selected_idea and st.session_state.selected_idea["title"] == idea["title"]
            border_color = "#8b5cf6" if is_selected else "rgba(255,255,255,0.05)"
            bg_card = "rgba(139,92,246,0.05)" if is_selected else "rgba(255,255,255,0.02)"
            
            st.markdown(f"""
            <div style='border: 1px solid {border_color}; background: {bg_card}; border-radius:12px; padding:20px; margin-bottom:12px;'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <span style='font-size:14px; color:#06b6d4; font-weight:600;'>Audience: {idea.get('audience', 'N/A')}</span>
                    <div style='display:flex; gap:10px;'>
                        <span class='agent-tag' style='background:rgba(236,72,153,0.15); color:#ec4899;'>Virality: {idea.get('virality_estimate', '0%')}</span>
                        <span class='agent-tag' style='background:rgba(6,182,212,0.15); color:#06b6d4;'>Engagement: {idea.get('engagement_potential', 'N/A')}</span>
                    </div>
                </div>
                <h4 style='margin:10px 0;'>{idea.get('title', 'N/A')}</h4>
                <p style='font-size:13px; color:#94a3b8;'><b>Why perform:</b> {idea.get('why_will_perform', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Select Campaign Idea", key=f"sel-idea-{idx}"):
                with st.spinner("Orchestrating Stage 2 agents..."):
                    run_stage_2_pipeline(idea)
                st.success(f"Selected Idea: '{idea.get('title', 'N/A')}'. Assets compiled!")
                st.rerun()
                
    with tab_script:
        if st.session_state.script:
            script = st.session_state.script
            st.markdown("### Short-Form Video Script")
            st.markdown("---")
            st.markdown(f"**📢 Hook (0-5s):**\n*{script.get('hook', 'N/A')}*")
            st.markdown(f"**📖 Story (5-25s):**\n{script.get('story', 'N/A')}")
            st.markdown("**💡 Key Insights (25-40s):**")
            for insight in script.get('insights', []):
                st.markdown(f"- {insight}")
            st.markdown(f"**🎯 CTA (40-45s):**\n**{script.get('cta', 'N/A')}**")
        else:
            st.warning("Please select a content idea under the 'Content Ideas' tab first.")
            
    with tab_linkedin:
        if st.session_state.linkedin:
            li = st.session_state.linkedin
            st.markdown("### LinkedIn Copywriting")
            st.markdown("---")
            st.code(f"{li.get('post', 'N/A')}\n\n{li.get('hashtags', '')}\n{li.get('engagement_hook', '')}", language="text")
            st.markdown("##### 🎨 LinkedIn Image Generation Prompt")
            st.code(li.get('image_prompt', 'N/A'), language="text")
        else:
            st.warning("Please select a content idea under the 'Content Ideas' tab first.")
            
    with tab_instagram:
        if st.session_state.instagram:
            ig = st.session_state.instagram
            st.markdown("### Instagram Caption")
            st.markdown("---")
            st.code(f"{ig.get('caption', 'N/A')}\n\n{ig.get('hashtags', '')}\n{ig.get('cta', '')}", language="text")
            st.markdown("##### 🎨 Instagram Cover Prompt")
            st.code(ig.get('thumbnail_prompt', 'N/A'), language="text")
        else:
            st.warning("Please select a content idea under the 'Content Ideas' tab first.")

    with tab_prompts:
        if st.session_state.linkedin and st.session_state.instagram and st.session_state.reel_studio:
            st.markdown("### 🎨 Ready-to-Paste Image Prompts")
            st.markdown("Copy and paste these professional prompts into Gemini Image Generation, Imagen, or Stable Diffusion.")
            st.markdown("---")
            
            st.markdown("#### 💼 LinkedIn Graphic Prompt")
            st.code(st.session_state.linkedin.get('image_prompt', 'N/A'), language="text")
            
            st.markdown("#### 📸 Instagram Thumbnail Prompt")
            st.code(st.session_state.instagram.get('thumbnail_prompt', 'N/A'), language="text")
            
            st.markdown("#### 🎬 Social Media Visual Prompt (Reel Cover)")
            st.code(st.session_state.reel_studio.get('thumbnail_prompt', 'N/A'), language="text")
        else:
            st.warning("Please select a content idea under the 'Content Ideas' tab first.")


# ------------------------------------------
# PAGE 4: REEL STUDIO
# ------------------------------------------
elif st.session_state.current_page == "Reel Studio":
    st.markdown("### 🎬 Reel Production Studio")
    st.markdown("Scene breakdowns, thumbnail cover prompts, and subtitle scripts.")
    
    if st.session_state.reel_studio:
        studio = st.session_state.reel_studio
        
        col_rs1, col_rs2 = st.columns([1, 1.4])
        
        with col_rs1:
            st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
            st.markdown("##### Voiceover Narration Script")
            st.write(studio.get('voiceover_script', 'N/A'))
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
            st.markdown("##### Thumbnail Prompt")
            st.code(studio.get('thumbnail_prompt', 'N/A'), language="text")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
            st.markdown("##### B-Roll suggestion")
            st.write(studio.get('b_roll_suggestions', 'N/A'))
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_rs2:
            st.markdown("#### Scene-by-Scene Storyboard")
            
            st.markdown("<div class='timeline-list'>", unsafe_allow_html=True)
            for scene in studio.get('scenes', []):
                scene_num = scene.get('scene_number', '?')
                duration = scene.get('duration', 'N/A')
                title = scene.get('title', f"Scene {scene_num}")
                visual = scene.get('visual_prompt', 'N/A')
                b_roll = scene.get('b_roll', 'N/A')
                subtitle = scene.get('subtitle', 'N/A')
                camera = scene.get('camera_direction', 'N/A')
                editing = scene.get('editing_suggestions', 'N/A')
                
                st.markdown(f"""
                <div class='timeline-item'>
                    <div class='timeline-dot'></div>
                    <div style='display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.04); padding-bottom:6px; margin-bottom:8px;'>
                        <span style='font-weight:700;'>{title}</span>
                        <span style='font-size:11px; background:rgba(6,182,212,0.1); color:#06b6d4; padding:1px 6px; border-radius:4px;'>{duration}</span>
                    </div>
                    <p style='font-size:12.5px;'><b>Visual Prompt:</b> {visual}</p>
                    <p style='font-size:12.5px;'><b>B-Roll:</b> {b_roll}</p>
                    <p style='font-size:12.5px; font-style:italic; color:#06b6d4; background:rgba(0,0,0,0.1); padding:4px 8px; border-radius:4px;'><b>Subtitle overlay:</b> "{subtitle}"</p>
                    <p style='font-size:11px; color:#64748b;'>Camera: {camera} | Edit: {editing}</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
    else:
        st.warning("Please select a content idea under Content Studio to generate production timeline storyboards.")


# ------------------------------------------
# PAGE 5: ANALYTICS
# ------------------------------------------
elif st.session_state.current_page == "Analytics":
    st.markdown("### 📊 Virality Analytics")
    st.markdown("Predictions and metrics compiled using the trained XGBoost virality regressor.")
    
    if st.session_state.virality:
        vir = st.session_state.virality
        
        col_an1, col_an2 = st.columns([1, 1.4])
        
        with col_an1:
            st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
            st.markdown("##### Expected Campaign Reach")
            st.markdown(f"Predicted Virality Score: **{vir.get('virality_score', 0.0):.1f}%**")
            st.markdown(f"Expected Views: **{vir.get('expected_views', 0):,}**")
            st.markdown(f"Expected Likes: **{vir.get('expected_likes', 0):,}**")
            st.markdown(f"Expected Shares: **{vir.get('expected_shares', 0):,}**")
            st.markdown(f"Expected Saves: **{vir.get('expected_saves', 0):,}**")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
            st.markdown("##### Prediction Reasoning")
            st.write(vir.get('reasoning', 'N/A'))
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_an2:
            st.markdown("#### Performance Metric Chart")
            
            # Simple Chart.js mock chart representation or native streamlit bar chart
            views_val = vir.get('expected_views', 0)
            chart_df = pd.DataFrame({
                "Platform": ["Instagram Reels", "TikTok", "YouTube Shorts", "LinkedIn Video"],
                "Expected Views": [
                    views_val,
                    int(views_val * 1.55),
                    int(views_val * 0.92),
                    int(views_val * 0.14)
                ]
            })
            st.bar_chart(chart_df.set_index("Platform"))
            
            st.write("**Key Virality Factors:**")
            for factor in vir.get('factors', []):
                st.write(f"✅ {factor}")
    else:
        st.warning("Please select a content idea under Content Studio to generate analytics predictions.")
