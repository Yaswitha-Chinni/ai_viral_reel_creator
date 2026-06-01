import streamlit as st
import os
import time
import json
import re
import tempfile
import requests
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
import google.generativeai as genai
from faker import Faker

# LangChain imports
from langchain_core.tools import tool
from langchain_core.runnables import RunnableLambda

# ML libraries
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

# Setup environment and page configuration
load_dotenv()
st.set_page_config(
    page_title="Ratefluencer AI Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("GEMINI_API_KEY not found. Please verify your .env file or configuration.")

# Detect available Gemini model
@st.cache_resource
def detect_gemini_model():
    """
    Checks if gemini-1.5-flash is available.
    If it's deprecated or 404s, falls back to gemini-2.5-flash.
    """
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

# Gemini call utility with rate-limiting error handling
def call_gemini_safe(prompt):
    """
    Executes a prompt on Gemini, catching rate limits (429/ResourceExhausted)
    and showing a retry warning.
    """
    try:
        model = genai.GenerativeModel(gemini_model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        err_msg = str(e).lower()
        if "429" in err_msg or "resourceexhausted" in err_msg or "rate limit" in err_msg or "quota" in err_msg:
            st.error("⏳ Gemini API Rate Limit Exceeded. Wait 4sec and retry.")
            time.sleep(4)
            st.stop()
        else:
            raise e

# MoviePy lazy loader
def get_moviepy_editor():
    try:
        import moviepy.editor as mp
        return mp
    except Exception as e:
        st.warning(f"MoviePy imports failed: {e}. Video generation will run in fallback audio-only mode.")
        return None

# ==========================================
# 1. Cached XGBoost training & Data Gen
# ==========================================
csv_train_path = os.path.join("data", "virality_train.csv")

def ensure_virality_training_data():
    """
    Generates a 50-row CSV file using Faker with columns:
    hook_words, trend_score, novelty, views (views represents virality score).
    """
    if not os.path.exists("data"):
        os.makedirs("data", exist_ok=True)
        
    if not os.path.exists(csv_train_path):
        fake = Faker()
        np.random.seed(42)
        rows = []
        for _ in range(50):
            hook_text = fake.sentence(nb_words=np.random.randint(6, 16))
            trend_val = float(np.random.uniform(50, 98))
            novel_val = float(np.random.uniform(30, 95))
            
            # Target views formula:
            # Optimal hook has around 11 words
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

# Train and Cache XGBoost Model on Startup
@st.cache_resource
def get_cached_xgboost_model():
    ensure_virality_training_data()
    df = pd.read_csv(csv_train_path)
    
    # Feature engineering: extract hook word count
    df["hook_word_count"] = df["hook_words"].apply(lambda x: len(str(x).split()))
    
    X = df[["trend_score", "hook_word_count", "novelty"]]
    y = df["views"]
    
    xgb = XGBRegressor(n_estimators=30, max_depth=3, learning_rate=0.1, random_state=42)
    xgb.fit(X, y)
    return xgb

# Initialize model cache on startup
cached_xgb_model = get_cached_xgboost_model()

# Heuristic sentiment scorer for RandomForest ranker
def compute_sentiment(title):
    pos_triggers = ["breakthrough", "new", "release", "future", "epic", "scale", "power", "unreal", "quantum", "openai", "verge", "techcrunch"]
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
# 2. Custom CSS Theme & Glassmorphism Design
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Outfit', sans-serif;
    background-color: #0b0c10;
    color: #c5c6c7;
}

.main-title {
    background: linear-gradient(135deg, #7b2cbf 0%, #ff007f 50%, #00f5d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3.2rem;
    font-weight: 800;
    text-align: center;
    margin-bottom: 0.2rem;
}

.subtitle {
    color: #8b9bb4;
    text-align: center;
    font-size: 1.1rem;
    margin-bottom: 2rem;
    font-weight: 300;
}

.glass-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    transition: transform 0.3s ease, border-color 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-2px);
    border-color: rgba(123, 44, 191, 0.4);
}

.agent-step {
    background: rgba(123, 44, 191, 0.05);
    border-left: 4px solid #7b2cbf;
    padding: 0.8rem 1.2rem;
    margin-bottom: 0.8rem;
    border-radius: 4px;
}

.stTextInput>div>div>input, .stTextArea>div>textarea, .stSelectbox>div>div>div {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #ffffff !important;
    border-radius: 8px !important;
}

.stButton>button {
    background: linear-gradient(135deg, #7b2cbf 0%, #ff007f 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.8rem 2.2rem !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 15px rgba(255, 0, 127, 0.2) !important;
    transition: all 0.3s ease !important;
    width: 100%;
}

.stButton>button:hover {
    transform: scale(1.02) !important;
    box-shadow: 0 6px 20px rgba(255, 0, 127, 0.4) !important;
}

[data-testid="stSidebar"] {
    background-color: #0f1016 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>RATEFLUENCER AI AGENT</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Orchestrated Content Engine with TechCrunch/Verge RSS & Cached XGBoost</div>", unsafe_allow_html=True)

# Initialize Session States
if "agent_run_complete" not in st.session_state:
    st.session_state.agent_run_complete = False
if "agent_logs" not in st.session_state:
    st.session_state.agent_logs = []
if "trend_results" not in st.session_state:
    st.session_state.trend_results = []
if "generated_script" not in st.session_state:
    st.session_state.generated_script = {}
if "video_path" not in st.session_state:
    st.session_state.video_path = ""
if "virality_data" not in st.session_state:
    st.session_state.virality_data = {}

# Sidebar details
with st.sidebar:
    st.markdown("### ⚙️ Engine Configurations")
    st.markdown(f"**LLM Model:** `{gemini_model_name}` ✅")
    st.markdown("**GCP Project:** `my-sample-project-495116`")
    st.markdown("---")
    
    st.markdown("### 📊 Cached Train CSV (/data/virality_train.csv)")
    if os.path.exists(csv_train_path):
        st.success("virality_train.csv created")
        df_show = pd.read_csv(csv_train_path)
        st.dataframe(df_show.head(8), height=250)
    else:
        st.error("CSV training file missing")
        
    st.markdown("---")
    st.markdown("### ℹ️ LangChain Agent Setup")
    st.info(
        "Chains 5 tools: Reddit+RSS Trends -> RandomForest Ranker -> Gemini ScriptWriter -> MoviePy VideoMaker -> Cached XGBoost ViralityPredictor."
    )

# ==========================================
# 3. LangChain Tool Definitions
# ==========================================

import feedparser

@tool
def reddit_and_rss_trend_tool(query: str = "") -> str:
    """
    Tool 1: RedditAndRSSTrendTool
    Gets the top 10 posts from r/MachineLearning, r/startups, r/technology from last 24h,
    and parses headlines from TechCrunch + The Verge RSS feeds. Merges all into a single list.
    """
    headers = {"User-Agent": "ratefluencer_bot/1.0"}
    all_posts = []
    
    # 1. Fetch Reddit trends (read-only)
    subreddits = ["MachineLearning", "startups", "technology"]
    for sub in subreddits:
        try:
            url = f"https://www.reddit.com/r/{sub}/top/.json?t=day&limit=10"
            res = requests.get(url, headers=headers, timeout=8)
            if res.status_code == 200:
                posts_data = res.json().get("data", {}).get("children", [])
                for p in posts_data:
                    pdata = p.get("data", {})
                    all_posts.append({
                        "title": pdata.get("title"),
                        "upvotes": pdata.get("score", 0),
                        "num_comments": pdata.get("num_comments", 0),
                        "created_utc": pdata.get("created_utc", 0),
                        "subreddit": f"r/{sub}"
                    })
        except Exception:
            pass
            
    # 2. Fetch TechCrunch + The Verge RSS Feeds
    rss_feeds = {
        "TechCrunch": "https://techcrunch.com/feed/",
        "The Verge": "https://www.theverge.com/rss/index.xml"
    }
    for source_name, rss_url in rss_feeds.items():
        try:
            feed = feedparser.parse(rss_url)
            for entry in feed.entries[:8]:
                created_utc = time.time()
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    created_utc = time.mktime(entry.published_parsed)
                all_posts.append({
                    "title": entry.title,
                    "upvotes": np.random.randint(150, 1000),  # simulate upvotes
                    "num_comments": np.random.randint(20, 150),  # simulate comments
                    "created_utc": created_utc,
                    "subreddit": source_name
                })
        except Exception:
            pass
            
    # Fallback to defaults if all remote calls fail
    if not all_posts:
        all_posts = [
            {"title": "OpenAI releases new locally executable lightweight model", "upvotes": 1250, "num_comments": 180, "created_utc": time.time() - 7200, "subreddit": "r/technology"},
            {"title": "How to scale your SaaS from $0 to $10k MRR in 3 months", "upvotes": 520, "num_comments": 95, "created_utc": time.time() - 14400, "subreddit": "r/startups"},
            {"title": "New Verge Report: Apple shifts focus towards fully Agentic Siri", "upvotes": 1600, "num_comments": 290, "created_utc": time.time() - 3600, "subreddit": "The Verge"},
            {"title": "TechCrunch analysis: SaaS VC funding rebound in mid-2026", "upvotes": 750, "num_comments": 80, "created_utc": time.time() - 18000, "subreddit": "TechCrunch"}
        ]
        
    return json.dumps(all_posts)

@tool
def trend_ranker(posts_json: str) -> str:
    """
    Tool 2: TrendRanker
    Scores each trend 0-100 using a RandomForest model.
    Features: upvotes, num_comments, title_sentiment, hours_since_post.
    Trains on dummy data dynamically.
    """
    posts = json.loads(posts_json)
    
    # Train RandomForest Regressor on dummy parameters
    np.random.seed(42)
    X_train = np.random.rand(100, 4)
    y_train = (X_train[:, 0] * 35 + X_train[:, 1] * 25 + X_train[:, 2] * 25 + (1.0 - X_train[:, 3]) * 15)
    
    rf = RandomForestRegressor(n_estimators=15, random_state=42)
    rf.fit(X_train, y_train)
    
    # Run predictions
    features = []
    current_time = time.time()
    for p in posts:
        up_norm = min(p.get("upvotes", 0), 3000) / 3000.0
        cm_norm = min(p.get("num_comments", 0), 500) / 500.0
        sent = (compute_sentiment(p.get("title", "")) + 1.0) / 2.0
        
        hours = max((current_time - p.get("created_utc", 0)) / 3600.0, 0.1)
        hours_norm = min(hours, 24.0) / 24.0
        
        features.append([up_norm, cm_norm, sent, hours_norm])
        
    preds = rf.predict(features) * 100.0
    preds = np.clip(preds, 10.0, 99.8)
    
    for i, p in enumerate(posts):
        p["score"] = round(preds[i], 1)
        p["sentiment"] = round(compute_sentiment(p.get("title")), 2)
        hours = max((current_time - p.get("created_utc", 0)) / 3600.0, 0.1)
        p["hours_since_post"] = round(hours, 1)
        
    ranked_posts = sorted(posts, key=lambda x: x["score"], reverse=True)
    return json.dumps(ranked_posts)

@tool
def script_writer(ranked_trends_json: str) -> str:
    """
    Tool 3: ScriptWriter
    Writes a 45-second script about the highest-scoring trend using Gemini.
    With robust error handling: catches rate limits (429/ResourceExhausted) and notifies the user.
    Output JSON format: {hook, insight1, insight2, insight3, cta}.
    """
    ranked_posts = json.loads(ranked_trends_json)
    top_post = ranked_posts[0]
    title = top_post.get("title")
    sub = top_post.get("subreddit")
    score = top_post.get("score")
    
    prompt = f"""
    You are an expert short-form content creator. Write a high-retention 45-second reel script about the trending topic:
    "{title}" (from source: {sub}).
    
    Format the response strictly as a JSON object with these exact keys. Do not include any markdown format tags like ```json or ```.
    JSON Keys:
    - "hook": An attention-grabbing hook (under 12 words) to stop the user from swiping.
    - "insight1": The first key fact or development about this topic.
    - "insight2": The second interesting point or consequence.
    - "insight3": The third key takeaway.
    - "cta": A punchy call-to-action (under 8 words).
    
    Keep the tone spoken, conversational, and energetic.
    """
    
    # Safe Gemini execution with 429 catches
    text = call_gemini_safe(prompt)
    
    try:
        script_data = json.loads(text)
        script_data["trend_score"] = float(score)
        script_data["topic"] = title
        return json.dumps(script_data)
    except Exception:
        fallback = {
            "hook": f"This new development in {sub} is changing everything.",
            "insight1": f"Everyone is looking into '{title}' right now.",
            "insight2": "It represents a significant milestone in modern tech integrations.",
            "insight3": "This is changing how developers compile and deploy projects.",
            "cta": "Like and follow for updates!",
            "trend_score": float(score),
            "topic": title
        }
        return json.dumps(fallback)

@tool
def video_maker(script_json: str) -> str:
    """
    Tool 4: VideoMaker
    Creates a 1080x1920 MP4 reel from the script.
    Displays white text overlays on beautiful gradient background.
    TTS voiceover reads the script sequentially.
    """
    script = json.loads(script_json)
    hook = script.get("hook", "")
    i1 = script.get("insight1", "")
    i2 = script.get("insight2", "")
    i3 = script.get("insight3", "")
    cta = script.get("cta", "")
    
    slides_text = [hook, i1, i2, i3, cta]
    full_narration = f"{hook} ... {i1} ... {i2} ... {i3} ... {cta}"
    
    temp_dir = tempfile.gettempdir()
    audio_path = os.path.join(temp_dir, "ratefluencer_lc_audio.mp3")
    video_path = os.path.join(temp_dir, "ratefluencer_lc_video.mp4")
    
    # 1. TTS
    tts = gTTS(text=full_narration, lang='en', tld='com', slow=False)
    tts.save(audio_path)
    
    mp = get_moviepy_editor()
    if not mp:
        with open(audio_path, "rb") as f:
            st.session_state.generated_voiceover = f.read()
        return "Video skipped: MoviePy missing. Audio generated."
        
    try:
        audio_clip = mp.AudioFileClip(audio_path)
        total_duration = audio_clip.duration
        
        slide_duration = total_duration / 5.0
        slide_clips = []
        
        windows_font_path = "C:\\Windows\\Fonts\\segoeuib.ttf"
        windows_font_path_reg = "C:\\Windows\\Fonts\\segoeui.ttf"
        
        for idx, text in enumerate(slides_text):
            img = Image.new("RGBA", (1080, 1920), (10, 11, 16, 255))
            draw = ImageDraw.Draw(img)
            
            # Slide gradients
            gradients = [
                ((99, 32, 238), (255, 0, 127)),   # violet-pink
                ((0, 245, 212), (99, 32, 238)),   # cyan-violet
                ((255, 0, 127), (0, 245, 212)),   # pink-cyan
                ((99, 32, 238), (0, 245, 212)),   # violet-cyan
                ((255, 0, 127), (99, 32, 238))    # pink-violet
            ]
            color_a, color_b = gradients[idx % len(gradients)]
            
            # Draw gradient circles
            for r in range(500, 0, -3):
                draw.ellipse([(150-r, 350-r), (150+r, 350+r)], fill=(color_a[0], color_a[1], color_a[2], int(15 * (1 - r/500))))
                draw.ellipse([(930-r, 1570-r), (930+r, 1570+r)], fill=(color_b[0], color_b[1], color_b[2], int(15 * (1 - r/500))))
                
            # Content Card
            draw.rounded_rectangle([(80, 480), (1000, 1440)], radius=35, fill=(0, 0, 0, 130), outline=(255, 255, 255, 25), width=2)
            
            if os.path.exists(windows_font_path):
                font_lbl = ImageFont.truetype(windows_font_path, 40)
                font_body = ImageFont.truetype(windows_font_path_reg, 48)
                font_footer = ImageFont.truetype(windows_font_path, 28)
            else:
                font_lbl = ImageFont.load_default()
                font_body = ImageFont.load_default()
                font_footer = ImageFont.load_default()
                
            labels = ["✨ HOOK", "💡 INSIGHT 1", "💡 INSIGHT 2", "💡 INSIGHT 3", "🎯 CTA"]
            draw.text((540, 580), labels[idx], fill=(0, 245, 212, 255), font=font_lbl, anchor="mm")
            
            # Word Wrap text
            lines = []
            words = text.split()
            current_line = ""
            for word in words:
                test_line = current_line + " " + word if current_line else word
                if os.path.exists(windows_font_path):
                    bbox = draw.textbbox((0, 0), test_line, font=font_body)
                    w = bbox[2] - bbox[0]
                else:
                    w = len(test_line) * 20
                if w < 760:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
                
            y_offset = 820
            for line in lines[:6]:
                draw.text((540, y_offset), line, fill=(255, 255, 255, 255), font=font_body, anchor="mm")
                y_offset += 80
                
            draw.text((540, 1340), "⚡ Ratefluencer AI Agent", fill=(139, 155, 180, 140), font=font_footer, anchor="mm")
            
            # Save slide
            slide_path = os.path.join(temp_dir, f"lc_slide_{idx}.png")
            img.save(slide_path)
            
            clip = mp.ImageClip(slide_path).set_duration(slide_duration)
            slide_clips.append(clip)
            
        video_clip = mp.concatenate_videoclips(slide_clips, method="compose")
        video_clip = video_clip.set_audio(audio_clip)
        
        video_clip.write_videofile(
            video_path,
            fps=12,
            codec='libx264',
            audio_codec='aac',
            preset='ultrafast',
            logger=None
        )
        
        audio_clip.close()
        for c in slide_clips:
            c.close()
        video_clip.close()
        
        with open(video_path, "rb") as f:
            st.session_state.generated_video = f.read()
        with open(audio_path, "rb") as f:
            st.session_state.generated_voiceover = f.read()
            
        return video_path
    except Exception as e:
        return f"MoviePy rendering failure: {e}"

@tool
def virality_predictor(script_json: str) -> str:
    """
    Tool 5: ViralityPredictor
    Uses the cached XGBoost model trained on startup to predict the virality score.
    Features: trend_score, hook_word_count, topic_novelty.
    """
    script = json.loads(script_json)
    trend_score = float(script.get("trend_score", 75.0))
    hook = script.get("hook", "")
    hook_word_count = len(hook.split())
    topic = script.get("topic", "")
    
    # Safely evaluate topic novelty using Gemini
    try:
        prompt = f"Rate the novelty of this topic on a scale of 0 to 100 where 100 is highly unique: '{topic}'. Answer with only the integer number."
        novelty_text = call_gemini_safe(prompt)
        topic_novelty = float(re.findall(r'\d+', novelty_text)[0])
    except Exception:
        topic_novelty = 65.0
        if any(w in topic.lower() for w in ["openai", "quantum", "llm", "agentic", "apple", "deepseek", "verge", "techcrunch"]):
            topic_novelty = 88.0
            
    # Load cached XGBoost Model
    xgb = get_cached_xgboost_model()
    
    # Run Inference
    input_data = pd.DataFrame([{
        "trend_score": trend_score,
        "hook_word_count": hook_word_count,
        "novelty": topic_novelty
    }])
    pred = xgb.predict(input_data)[0]
    pred = round(float(pred), 1)
    pred = min(max(pred, 10.0), 99.8)
    
    res = {
        "virality_score": pred,
        "features": {
            "trend_score": trend_score,
            "hook_word_count": hook_word_count,
            "topic_novelty": topic_novelty
        }
    }
    return json.dumps(res)

# Register tools as LangChain nodes
reddit_and_rss_node = RunnableLambda(lambda x: reddit_and_rss_trend_tool.invoke(""))
ranker_node = RunnableLambda(lambda x: trend_ranker.invoke(x))
writer_node = RunnableLambda(lambda x: script_writer.invoke(x))
video_node = RunnableLambda(lambda x: video_maker.invoke(x))
predictor_node = RunnableLambda(lambda x: virality_predictor.invoke(x))

# ==========================================
# 4. Streamlit UI Layout
# ==========================================

st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.markdown("### 🤖 LangChain Agent Flow Orchestration")
st.write("Click below to run the LangChain Agent. It merges Reddit + RSS feeds (TechCrunch & The Verge), ranks them, scripts the best topic using Gemini, compiles media, and evaluates virality using cached XGBoost.")

run_agent_btn = st.button("🚀 Run LangChain Agent Pipeline")
st.markdown("</div>", unsafe_allow_html=True)

if run_agent_btn:
    st.session_state.agent_logs = []
    st.session_state.agent_run_complete = False
    
    st.markdown("### 📋 Agent Execution Logs")
    log_container = st.container()
    
    with st.spinner("Agent running tools..."):
        # Tool 1: Reddit + RSS
        st.session_state.agent_logs.append("Executing RedditAndRSSTrendTool...")
        with log_container:
            st.markdown("<div class='agent-step'>🛠️ <b>Step 1: RedditAndRSSTrendTool</b> - Harvester querying Reddit, TechCrunch, and The Verge RSS...</div>", unsafe_allow_html=True)
        raw_trends = reddit_and_rss_node.invoke(None)
        st.session_state.trend_results = json.loads(raw_trends)
        
        # Tool 2: Trend Ranker
        st.session_state.agent_logs.append("Executing TrendRanker...")
        with log_container:
            st.markdown("<div class='agent-step'>🛠️ <b>Step 2: TrendRanker</b> - Scoring posts via RandomForest model...</div>", unsafe_allow_html=True)
        ranked_trends_json = ranker_node.invoke(raw_trends)
        st.session_state.trend_results = json.loads(ranked_trends_json)
        
        # Tool 3: Script Writer
        st.session_state.agent_logs.append("Executing ScriptWriter...")
        with log_container:
            st.markdown("<div class='agent-step'>🛠️ <b>Step 3: ScriptWriter</b> - Drafting script JSON using Gemini with 429 error handling...</div>", unsafe_allow_html=True)
        script_json = writer_node.invoke(ranked_trends_json)
        st.session_state.generated_script = json.loads(script_json)
        
        # Tool 4: Video Maker
        st.session_state.agent_logs.append("Executing VideoMaker...")
        with log_container:
            st.markdown("<div class='agent-step'>🛠️ <b>Step 4: VideoMaker</b> - Rendering 1080x1920 video with gTTS audio...</div>", unsafe_allow_html=True)
        video_path = video_node.invoke(script_json)
        st.session_state.video_path = video_path
        
        # Tool 5: Virality Predictor
        st.session_state.agent_logs.append("Executing ViralityPredictor...")
        with log_container:
            st.markdown("<div class='agent-step'>🛠️ <b>Step 5: ViralityPredictor</b> - Predicting final virality index using cached XGBoost...</div>", unsafe_allow_html=True)
        virality_json = predictor_node.invoke(script_json)
        st.session_state.virality_data = json.loads(virality_json)
        
        st.session_state.agent_run_complete = True
        st.success("LangChain agent execution complete!")

# Render Results
if st.session_state.agent_run_complete:
    st.markdown("---")
    st.markdown("### 📊 Agent Pipeline Outcomes")
    
    col_out1, col_out2 = st.columns([1, 1])
    
    with col_out1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### 🔥 Identified Trends (Reddit + TechCrunch + The Verge)")
        
        df_trends = pd.DataFrame(st.session_state.trend_results)
        df_trends = df_trends[["title", "subreddit", "upvotes", "num_comments", "hours_since_post", "score"]]
        df_trends.columns = ["Title", "Source", "Upvotes", "Comments", "Age (hrs)", "RF Score"]
        
        st.dataframe(df_trends, height=280)
        st.info(f"🏆 Top trend selected for production: **{st.session_state.generated_script.get('topic', '')}**")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### 📈 Predicted Virality Score (Cached XGBoost)")
        
        v_score = st.session_state.virality_data.get("virality_score", 0)
        v_feats = st.session_state.virality_data.get("features", {})
        
        score_color = "#00f5d4" if v_score >= 80 else ("#ff9f1c" if v_score >= 60 else "#ff007f")
        st.markdown(f"<div style='font-size: 3rem; font-weight: 800; color: {score_color}; text-align: center; margin: 1rem 0;'>{v_score}%</div>", unsafe_allow_html=True)
        
        st.write(f"**Extracted Predictor Features:**")
        st.write(f"- 🏆 RandomForest Trend Score: `{v_feats.get('trend_score', 0)}`")
        st.write(f"- 🪝 Hook Word Count: `{v_feats.get('hook_word_count', 0)}`")
        st.write(f"- 💡 Topic Novelty Rating: `{v_feats.get('topic_novelty', 0)}%`")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_out2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### 📝 Generated Script JSON")
        st.json({
            "hook": st.session_state.generated_script.get("hook", ""),
            "insight1": st.session_state.generated_script.get("insight1", ""),
            "insight2": st.session_state.generated_script.get("insight2", ""),
            "insight3": st.session_state.generated_script.get("insight3", ""),
            "cta": st.session_state.generated_script.get("cta", "")
        })
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### 🎬 Compiled Reel Preview")
        if "generated_video" in st.session_state and st.session_state.generated_video:
            st.video(st.session_state.generated_video, format="video/mp4")
            st.download_button(
                label="📥 Download Compiled Reel (MP4)",
                data=st.session_state.generated_video,
                file_name="ratefluencer_lc_reel.mp4",
                mime="video/mp4"
            )
        else:
            st.warning("Video rendering not completed or fell back to audio-only. Down below is the voiceover audio.")
            if "generated_voiceover" in st.session_state and st.session_state.generated_voiceover:
                st.audio(st.session_state.generated_voiceover, format="audio/mp3")
                st.download_button(
                    label="📥 Download Voiceover (MP3)",
                    data=st.session_state.generated_voiceover,
                    file_name="voiceover.mp3",
                    mime="audio/mp3"
                )
        st.markdown("</div>", unsafe_allow_html=True)
