import os
import time
import json
import re
import random
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
from faker import Faker
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
import feedparser
import requests

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Ratefluencer AI - API Server (Hackathon Edition)",
    description="API for the Viral Reel Creator platform aligning with Track 2 requirements",
    version="2.0.0"
)

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("WARNING: GEMINI_API_KEY not found. Safe mode or mock fallbacks will be used.")

# Model selection
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
print(f"Using Gemini Model: {gemini_model_name}")

def call_gemini_safe(prompt):
    if not api_key:
        return get_mock_gemini_response(prompt)
    try:
        model = genai.GenerativeModel(gemini_model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        err_msg = str(e).lower()
        if "429" in err_msg or "resourceexhausted" in err_msg or "rate limit" in err_msg or "quota" in err_msg:
            print("Gemini rate limit hit. Sleeping for 3s...")
            time.sleep(3)
            try:
                model = genai.GenerativeModel(gemini_model_name)
                response = model.generate_content(prompt)
                return response.text
            except Exception:
                return get_mock_gemini_response(prompt)
        else:
            print(f"Gemini call error: {e}. Falling back to mock generator.")
            return get_mock_gemini_response(prompt)

def get_mock_gemini_response(prompt):
    prompt_lower = prompt.lower()
    if "ideas" in prompt_lower or "target_audience" in prompt_lower:
        # Content ideas generation
        return json.dumps([
            {
                "title": "Why solo founders are deploying autonomous agent loops",
                "target_audience": "Solopreneurs & Indie Hackers",
                "virality_potential": "High",
                "estimated_engagement": "92%"
            },
            {
                "title": "The recursive API billing trap: audit your loops",
                "target_audience": "SaaS Engineers",
                "virality_potential": "Extreme",
                "estimated_engagement": "96%"
            },
            {
                "title": "Chatbots are dead, agent workspaces are taking over",
                "target_audience": "Tech Enthusiasts & Founders",
                "virality_potential": "Critical",
                "estimated_engagement": "89%"
            },
            {
                "title": "Auditing loop nodes in your vector database pipeline",
                "target_audience": "Data Architects",
                "virality_potential": "Moderate",
                "estimated_engagement": "74%"
            },
            {
                "title": "The ultimate framework for scaling Agentic AI in 2026",
                "target_audience": "CTOs & Product Owners",
                "virality_potential": "High",
                "estimated_engagement": "82%"
            }
        ])
    elif "scene" in prompt_lower or "voiceover_script" in prompt_lower:
        # Reel studio generation
        return json.dumps({
            "voiceover_script": "Stop coding chat panels. The future of software is autonomous loops. Indie hackers are deploying recursive agent nodes to build complete applications in minutes. But be careful: unchecked loops can spike your API bills by 10x overnight. Save this post to learn how to audit your agent pipelines!",
            "thumbnail_prompt": "A modern glow UI displaying recursive digital lines. Text overlay in bold Outfit typography: 'CHATS ARE DEAD: THE AGENTIC ERA.' Glowing cyan and purple accents, high tech dark background.",
            "b_roll_suggestions": "Close-up of keyboard typing, terminal code scrolling, floating agent loop diagram, credit card invoice showing high API usage, mobile screen warning alert.",
            "scenes": [
                {
                    "scene_number": 1,
                    "duration": "0-5s",
                    "title": "Scene 1: Hook visual",
                    "visual_prompt": "Close-up of a developer shutting down a standard chat screen. Transitioning to a glowing recursive database console.",
                    "b_roll": "Close-up of hands shutting laptop screen.",
                    "subtitle": "Stop coding chat panels. The future is autonomous loops."
                },
                {
                    "scene_number": 2,
                    "duration": "5-20s",
                    "title": "Scene 2: Problem visualization",
                    "visual_prompt": "Screen view showing a fast-scrolling terminal running agent scripts, with a high API usage overlay blinking in neon orange.",
                    "b_roll": "Fast scrolling code on terminal.",
                    "subtitle": "Indie hackers are deploying loop agents... but it can spike your API bills by 10x!"
                },
                {
                    "scene_number": 3,
                    "duration": "20-35s",
                    "title": "Scene 3: Main insight",
                    "visual_prompt": "A diagram mapping a loop node audit workflow. Highlights of database auditing tools glowing in neon purple.",
                    "b_roll": "Audit diagram workflow panning.",
                    "subtitle": "Audit your loops and scale agent workloads safely."
                },
                {
                    "scene_number": 4,
                    "duration": "35-45s",
                    "title": "Scene 4: Call to action",
                    "visual_prompt": "End screen showing social icon handles with a pulse effect. Text overlay: 'SAVE FOR LATER'.",
                    "b_roll": "Save icon animation pulsing.",
                    "subtitle": "Tap follow and save this post to audit your pipelines!"
                }
            ]
        })
    elif "hook" in prompt_lower and "insight1" in prompt_lower:
        # Reel script request
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
            "hook": "SaaS architecture is pivoting. Autonomous loops are replacing text prompts. 🤖"
        })
    elif "instagram" in prompt_lower:
        return json.dumps({
            "caption": "Chats are legacy. Loops are next. ⚡ Solo founders are scaling systems by deploying autonomous agent nodes. But beware of recursive API traps! Swipe left to read how to build loops safely! 👇",
            "hashtags": "#aidevelopment #agentic #saasstartup #codinglife #databaseaudit #indiehackers",
            "cta": "Save this reel to protect your vector pipelines! 📌"
        })
    elif "novelty" in prompt_lower:
        return "85"
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

# Request Models
class GenerateIdeasRequest(BaseModel):
    topic: str

class GenerateAssetsRequest(BaseModel):
    niche: str
    selected_trend: dict
    selected_idea: dict

# ====================================================
# STAGE 1 ENDPOINT: /api/generate-ideas
# ====================================================
@app.post("/api/generate-ideas")
async def generate_ideas(req: GenerateIdeasRequest):
    niche = req.topic.strip()
    if not niche:
        niche = "Technology"

    print(f"STAGE 1: Fetching trends & ideas for niche: {niche}")
    
    # Discovery
    headers = {"User-Agent": "ratefluencer_bot/1.0"}
    subreddits = ["MachineLearning", "startups", "technology"]
    all_posts = []
    
    for sub in subreddits:
        try:
            url = f"https://www.reddit.com/r/{sub}/top/.json?t=day&limit=5"
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

    rss_feeds = {
        "TechCrunch": "https://techcrunch.com/feed/",
        "The Verge": "https://www.theverge.com/rss/index.xml"
    }
    for source_name, rss_url in rss_feeds.items():
        try:
            feed = feedparser.parse(rss_url)
            for entry in feed.entries[:5]:
                all_posts.append({
                    "title": entry.title,
                    "upvotes": random.randint(150, 1000),
                    "num_comments": random.randint(20, 150),
                    "created_utc": time.time(),
                    "source": source_name
                })
        except Exception:
            pass

    filtered_posts = []
    for p in all_posts:
        if niche.lower() in p["title"].lower() or niche.lower() in p["source"].lower():
            filtered_posts.append(p)
            
    if len(filtered_posts) < 5:
        prompt = f"""
        Generate exactly 10 trending topics or news currently viral in the "{niche}" space.
        Format as a JSON array of objects. Do not include markdown code block tags.
        JSON Keys:
        - "title": Topic title.
        - "source": Platform source (e.g. TechCrunch, Reddit).
        - "upvotes": Integer score (100 to 3000).
        - "num_comments": Comments count (10 to 600).
        """
        gemini_res = call_gemini_safe(prompt)
        try:
            cleaned_res = re.sub(r'^```json\s*|```$', '', gemini_res.strip(), flags=re.MULTILINE)
            generated_trends = json.loads(cleaned_res)
            for gt in generated_trends:
                gt["created_utc"] = time.time() - random.randint(1000, 50000)
                filtered_posts.append(gt)
        except Exception as e:
            print(f"Failed to parse trends: {e}")

    if not filtered_posts:
        filtered_posts = [
            {"title": f"The rise of Agentic AI loops in {niche}", "upvotes": 1840, "num_comments": 310, "created_utc": time.time() - 3600, "source": "TechCrunch"},
            {"title": f"How startups are auditing recursive workflows in {niche}", "upvotes": 1100, "num_comments": 195, "created_utc": time.time() - 7200, "source": "r/startups"},
            {"title": f"New regulations impacting open-source developers building in {niche}", "upvotes": 950, "num_comments": 80, "created_utc": time.time() - 14400, "source": "The Verge"},
            {"title": f"Why vector databases are spiking across the {niche} space", "upvotes": 680, "num_comments": 52, "created_utc": time.time() - 21600, "source": "r/technology"},
            {"title": f"Hackers leverage multi-agent models to exploit {niche} pipelines", "upvotes": 1050, "num_comments": 160, "created_utc": time.time() - 28800, "source": "r/technology"}
        ]

    # RandomForest Ranking
    ranked_trends = []
    features = []
    current_time = time.time()
    
    for p in filtered_posts[:12]:
        up_norm = min(p.get("upvotes", 0), 3000) / 3000.0
        cm_norm = min(p.get("num_comments", 0), 500) / 500.0
        sent = (compute_sentiment(p.get("title", "")) + 1.0) / 2.0
        hours = max((current_time - p.get("created_utc", 0)) / 3600.0, 0.1)
        hours_norm = min(hours, 24.0) / 24.0
        features.append([up_norm, cm_norm, sent, hours_norm])

    preds = rf_model.predict(features) * 100.0
    preds = np.clip(preds, 20.0, 99.5)
    
    for i, p in enumerate(filtered_posts[:12]):
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
    top_trend = ranked_trends[0]

    # Generate 5 Content Ideas based on the winning trend
    print(f"STAGE 1: Generating ideas for trend: {top_trend['title']}")
    ideas_prompt = f"""
    Based on this trending topic: "{top_trend['title']}" in the "{niche}" niche,
    generate exactly 5 viral short-form content ideas.
    
    Format the response strictly as a JSON array of objects. Do not include markdown code block tags.
    JSON keys for each object:
    - "title": A catchy hook/title of the idea.
    - "target_audience": E.g. "Startup Founders", "Developers", "AI Creators".
    - "virality_potential": A rating (e.g. "High", "Critical", "Extreme", "Moderate").
    - "estimated_engagement": A percentage string (e.g. "88%", "94%").
    """
    ideas_text = call_gemini_safe(ideas_prompt)
    try:
        cleaned_ideas = re.sub(r'^```json\s*|```$', '', ideas_text.strip(), flags=re.MULTILINE)
        content_ideas = json.loads(cleaned_ideas)
    except Exception:
        content_ideas = get_mock_gemini_response("ideas")

    payload = {
        "niche": niche,
        "top_trend": top_trend,
        "trends": ranked_trends,
        "ideas": content_ideas
    }

    return JSONResponse(content=payload)


# ====================================================
# STAGE 2 ENDPOINT: /api/generate-assets
# ====================================================
@app.post("/api/generate-assets")
async def generate_assets(req: GenerateAssetsRequest):
    niche = req.niche
    top_trend = req.selected_trend
    selected_idea = req.selected_idea

    print(f"STAGE 2: Generating assets for content idea: {selected_idea['title']}")
    
    # 1. Reel Script Writer
    script_prompt = f"""
    Write a 45-second vertical reel script based on this selected content idea:
    Idea: "{selected_idea['title']}" (derived from trend: "{top_trend['title']}") in the "{niche}" niche.
    
    Format the response strictly as a JSON object. Do not include markdown code block tags.
    JSON Keys:
    - "hook": Attention grabbing hook (under 12 words).
    - "story": Spoken narrative (2-3 sentences).
    - "insights": JSON array of exactly 3 bullet insights.
    - "cta": Punchy call-to-action (under 8 words).
    """
    script_text = call_gemini_safe(script_prompt)
    try:
        cleaned_script = re.sub(r'^```json\s*|```$', '', script_text.strip(), flags=re.MULTILINE)
        script_data = json.loads(cleaned_script)
    except Exception:
        script_data = {
            "hook": f"Stop scrolling! This single development in {niche} is changing everything.",
            "story": f"We are officially moving from manual workflows to automated systems. The idea: '{selected_idea['title']}' is currently proving this transition across the creator economy.",
            "insights": [
                "It reduces deployment cycles from days to simple automation segments.",
                "It enables solo builders to scale reach at a corporate level.",
                "Auditing operational nodes prevents infinite loop billing traps."
            ],
            "cta": f"Comment '{niche.upper().replace(' ', '')}' for early access!"
        }

    # 2. Automated Reel Production Studio Assets
    production_prompt = f"""
    Create a complete automated reel production studio package based on this script:
    Hook: {script_data['hook']}
    Story: {script_data['story']}
    Insights: {', '.join(script_data['insights'])}
    CTA: {script_data['cta']}
    
    Format the response strictly as a JSON object. Do not include markdown code block tags.
    JSON Keys:
    - "voiceover_script": The complete vocal narration block.
    - "thumbnail_prompt": Visual text-to-image prompt for the reel cover.
    - "b_roll_suggestions": General description of b-roll flow.
    - "scenes": A JSON array of exactly 4 objects (Scene 1: Hook visual, Scene 2: Problem visualization, Scene 3: Main insight, Scene 4: Call to action).
      Each object must contain:
      - "scene_number": Integer (1, 2, 3, 4)
      - "duration": Duration string (e.g. "0-5s", "5-20s")
      - "title": Scene title (e.g. "Scene 1: Hook visual")
      - "visual_prompt": Concrete visual layout description for asset creators
      - "b_roll": B-roll footage suggestions
      - "subtitle": Exact subtitle overlay text
    """
    production_text = call_gemini_safe(production_prompt)
    try:
        cleaned_prod = re.sub(r'^```json\s*|```$', '', production_text.strip(), flags=re.MULTILINE)
        production_data = json.loads(cleaned_prod)
    except Exception:
        production_data = get_mock_gemini_response("scene")

    # 3. LinkedIn Post Generator
    linkedin_prompt = f"""
    Create an engaging, authority-building LinkedIn post based on this campaign:
    Topic: {selected_idea['title']}
    Insights: {', '.join(script_data['insights'])}
    Target Audience: {selected_idea['target_audience']}
    
    Format the response strictly as a JSON object. Do not include markdown code block tags.
    JSON Keys:
    - "post": Formatted multi-line post text.
    - "hashtags": Hashtags string.
    - "engagement_hook": Conversational question at the end.
    """
    linkedin_text = call_gemini_safe(linkedin_prompt)
    try:
        cleaned_li = re.sub(r'^```json\s*|```$', '', linkedin_text.strip(), flags=re.MULTILINE)
        linkedin_data = json.loads(cleaned_li)
    except Exception:
        linkedin_data = {
            "post": f"The landscape of {niche} is changing right before our eyes. 🚀\n\nIf your target is {selected_idea['target_audience']}, '{selected_idea['title']}' is gaining explosive momentum. Here are the core details you need to know:\n\n💡 Key takeaways:\n1. It reduces standard production timeframes drastically.\n2. Solo operators scale at enterprise level.\n3. Auditing loop iterations prevents recursive billing bottlenecks.\n\nThis marks a new era in creators leveraging AI to dominate their spaces.",
            "hashtags": f"#niche #StartupLife #BusinessGrowth #{niche.replace(' ', '')}",
            "engagement_hook": "Is this a temporary hype or the new normal? Let me know your thoughts!"
        }

    # 4. Instagram Caption Generator
    instagram_prompt = f"""
    Create an energetic Instagram post caption based on this script:
    Hook: {script_data['hook']}
    Story: {script_data['story']}
    
    Format the response strictly as a JSON object. Do not include markdown code block tags.
    JSON Keys:
    - "caption": Instagram caption copy.
    - "hashtags": Hashtags.
    - "cta": IG Call-to-action block.
    """
    instagram_text = call_gemini_safe(instagram_prompt)
    try:
        cleaned_ig = re.sub(r'^```json\s*|```$', '', instagram_text.strip(), flags=re.MULTILINE)
        instagram_data = json.loads(cleaned_ig)
    except Exception:
        instagram_data = {
            "caption": f"Huge news in the {niche} scene today! 🔥 '{selected_idea['title']}' is officially changing the game. If you're building in this space, you can't afford to ignore this. Let's discuss in the comments below! 👇",
            "hashtags": f"#viralreels #growthmindset #{niche.lower().replace(' ', '')} #digitalmarketing #trends",
            "cta": "Save this reel for later! 📌"
        }

    # 5. XGBoost Virality Scoring
    hook_word_count = len(script_data['hook'].split())
    input_data = pd.DataFrame([{
        "trend_score": top_trend["score"],
        "hook_word_count": hook_word_count,
        "novelty": top_trend["novelty"]
    }])
    pred_score = xgb_model.predict(input_data)[0]
    pred_score = round(float(pred_score), 1)
    # Give a tiny boost if engagement estimate was high
    est_engage_val = float(selected_idea["estimated_engagement"].replace("%",""))
    pred_score = pred_score * 0.9 + (est_engage_val * 0.1)
    pred_score = min(max(pred_score, 45.0), 99.8)

    expected_views = int(pred_score * 12500 + random.randint(10000, 35000))
    expected_likes = int(expected_views * 0.082 + random.randint(200, 800))
    expected_shares = int(expected_views * 0.028 + random.randint(30, 200))
    expected_saves = int(expected_views * 0.048 + random.randint(50, 300))

    hourly_engagement = []
    for hour in range(1, 25):
        multiplier = 1 / (1 + np.exp(-0.24 * (hour - 10)))
        current_views = int(expected_views * multiplier)
        hourly_engagement.append({
            "hour": f"{hour}h",
            "views": current_views,
            "likes": int(current_views * 0.082)
        })

    platform_performance = [
        {"platform": "Instagram Reels", "expected_reach": expected_views},
        {"platform": "TikTok", "expected_reach": int(expected_views * 1.55)},
        {"platform": "YouTube Shorts", "expected_reach": int(expected_views * 0.92)},
        {"platform": "LinkedIn Video", "expected_reach": int(expected_views * 0.14)}
    ]

    virality_dashboard = {
        "virality_score": pred_score,
        "expected_views": expected_views,
        "expected_likes": expected_likes,
        "expected_shares": expected_shares,
        "expected_saves": expected_saves,
        "hourly_engagement": hourly_engagement,
        "platform_performance": platform_performance
    }

    payload = {
        "script": script_data,
        "reel_studio": production_data,
        "linkedin": linkedin_data,
        "instagram": instagram_data,
        "virality": virality_dashboard
    }

    return JSONResponse(content=payload)


# Serve index.html as fallback or direct
@app.get("/")
async def root():
    return FileResponse("static/index.html")

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
