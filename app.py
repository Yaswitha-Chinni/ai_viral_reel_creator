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
    title="Ratefluencer AI - API Server",
    description="API for the Viral Reel Creator platform",
    version="1.0.0"
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
            # Try once more
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
    if "hook" in prompt_lower and "insight1" in prompt_lower:
        # Reel script request
        return json.dumps({
            "hook": "Stop scrolling! This single AI tool is disrupting a $10B industry.",
            "insight1": "A new autonomous coding agent has just been released with 90% accuracy.",
            "insight2": "Developers are using it to build full applications in under 5 minutes.",
            "insight3": "Major tech companies are already integrating this into their core pipelines.",
            "cta": "Comment 'AGENT' and I'll send it to you!"
        })
    elif "linkedin" in prompt_lower:
        return json.dumps({
            "post": "AI is evolving faster than anyone predicted. 🤯\n\nA new autonomous coding agent was just released, demonstrating 90% accuracy on real-world engineering tasks. Developers are now building complete applications in minutes.\n\nHere are 3 key takeaways:\n1️⃣ The barrier to entry for software development is hitting zero.\n2️⃣ AI agents are transitioning from simple completion tools to fully autonomous collaborators.\n3️⃣ Companies that fail to integrate agentic workflows within the next 6 months will fall behind.\n\nHow is your team preparing for the agentic era? Let's discuss in the comments 👇",
            "hashtags": "#ArtificialIntelligence #TechTrends #SoftwareEngineering #FutureOfWork #SaaS",
            "hook": "AI is evolving faster than anyone predicted. 🤯"
        })
    elif "instagram" in prompt_lower:
        return json.dumps({
            "caption": "The future of coding is here and it is fully autonomous. ⚡ This new AI coding agent is solving complex tasks in seconds, putting application building in the hands of everyone. Is software engineering changing forever? Let me know your thoughts!",
            "hashtags": "#ai #tech #startups #developer #coding #futureoftech #viralreels",
            "cta": "Link in bio to read the full breakdown!"
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
    pos_triggers = ["breakthrough", "new", "release", "future", "epic", "scale", "power", "unreal", "quantum", "openai", "verge", "techcrunch", "ai", "agent"]
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
class GenerateRequest(BaseModel):
    topic: str

# API Endpoints
@app.post("/api/generate")
async def generate_workflow(req: GenerateRequest):
    niche = req.topic.strip()
    if not niche:
        niche = "Technology"

    print(f"Starting pipeline execution for niche: {niche}")
    
    # ----------------------------------------------------
    # STEP 1 & 2: TREND DISCOVERY AND RANKING
    # ----------------------------------------------------
    trends = []
    
    # Let's try RSS & Reddit fetch first
    headers = {"User-Agent": "ratefluencer_bot/1.0"}
    subreddits = ["MachineLearning", "startups", "technology"]
    all_posts = []
    
    # Try fetching subreddits
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

    # Try TechCrunch/Verge RSS
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

    # Filter posts by keyword match or generate using Gemini if list is empty or niche is highly specific
    filtered_posts = []
    for p in all_posts:
        if niche.lower() in p["title"].lower() or niche.lower() in p["source"].lower():
            filtered_posts.append(p)
            
    # If we have very few matches or niche is specific, we ask Gemini to generate 10 trending topics for this niche!
    if len(filtered_posts) < 5:
        print(f"Generating niche-specific trends via Gemini for: {niche}")
        prompt = f"""
        Generate exactly 10 trending news, topics, or debates currently viral in the "{niche}" niche.
        For each topic, provide:
        - "title": A short, viral headline/topic.
        - "source": A simulated news source or platform (e.g. TechCrunch, Reddit r/finance, Twitter, Wired).
        - "upvotes": An integer between 100 and 3000 representing engagement.
        - "num_comments": An integer between 20 and 800.
        
        Respond with a JSON array of objects. Do not include markdown formatting like ```json.
        """
        gemini_res = call_gemini_safe(prompt)
        try:
            # Clean up potential markdown formatting if returned
            cleaned_res = re.sub(r'^```json\s*|```$', '', gemini_res.strip(), flags=re.MULTILINE)
            generated_trends = json.loads(cleaned_res)
            for gt in generated_trends:
                gt["created_utc"] = time.time() - random.randint(1000, 50000)
                filtered_posts.append(gt)
        except Exception as e:
            print(f"Failed to parse Gemini generated trends: {e}")

    # If still empty, use fallback defaults
    if not filtered_posts:
        filtered_posts = [
            {"title": f"The rise of Agentic AI in {niche}", "upvotes": 1420, "num_comments": 290, "created_utc": time.time() - 3600, "source": "TechCrunch"},
            {"title": f"How startups are automating {niche} workflows", "upvotes": 850, "num_comments": 120, "created_utc": time.time() - 7200, "source": "r/startups"},
            {"title": f"New regulations impacting {niche} developers", "upvotes": 610, "num_comments": 85, "created_utc": time.time() - 14400, "source": "The Verge"},
            {"title": f"Open source tools taking over the {niche} space", "upvotes": 2100, "num_comments": 410, "created_utc": time.time() - 21600, "source": "r/technology"},
            {"title": f"Why VC investment in {niche} is doubling in 2026", "upvotes": 540, "num_comments": 95, "created_utc": time.time() - 28800, "source": "TechCrunch"},
            {"title": f"Mistakes you must avoid when building in {niche}", "upvotes": 990, "num_comments": 150, "created_utc": time.time() - 36000, "source": "r/technology"},
            {"title": f"The ultimate framework for scaling your {niche} application", "upvotes": 1200, "num_comments": 180, "created_utc": time.time() - 43200, "source": "r/startups"},
            {"title": f"Top 5 open-source libraries for {niche} development", "upvotes": 770, "num_comments": 65, "created_utc": time.time() - 50400, "source": "Wired"},
            {"title": f"How the creator economy is changing {niche}", "upvotes": 490, "num_comments": 50, "created_utc": time.time() - 57600, "source": "Twitter"},
            {"title": f"Is this new tool the death of standard practices in {niche}?", "upvotes": 1850, "num_comments": 310, "created_utc": time.time() - 64800, "source": "Reddit"}
        ]

    # Rank them using the RandomForest model
    ranked_trends = []
    features = []
    current_time = time.time()
    
    for p in filtered_posts[:15]:  # Limit to top 15 candidates
        up_norm = min(p.get("upvotes", 0), 3000) / 3000.0
        cm_norm = min(p.get("num_comments", 0), 500) / 500.0
        sent = (compute_sentiment(p.get("title", "")) + 1.0) / 2.0
        hours = max((current_time - p.get("created_utc", 0)) / 3600.0, 0.1)
        hours_norm = min(hours, 24.0) / 24.0
        features.append([up_norm, cm_norm, sent, hours_norm])

    preds = rf_model.predict(features) * 100.0
    preds = np.clip(preds, 15.0, 99.5)
    
    for i, p in enumerate(filtered_posts[:15]):
        final_score = round(preds[i], 1)
        growth_vel = round(float(p.get("upvotes", 0) / ( (current_time - p.get("created_utc", 0)) / 3600.0 + 1.0 ) * 0.15), 1)
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
        
    ranked_trends = sorted(ranked_trends, key=lambda x: x["score"], reverse=True)[:10]
    top_trend = ranked_trends[0]

    # ----------------------------------------------------
    # STEP 3: VIRAL REEL GENERATION
    # ----------------------------------------------------
    print(f"Writing script for top trend: {top_trend['title']}")
    script_prompt = f"""
    Write a 45-second high-retention social media reel script about the trending topic:
    "{top_trend['title']}" in the niche: "{niche}".
    
    Format the response strictly as a JSON object with these exact keys. Do not include any markdown format tags like ```json or ```.
    JSON Keys:
    - "hook": An attention-grabbing hook (under 12 words) to stop the user from swiping.
    - "story": A conversational 2-3 sentence explanation/narrative.
    - "insights": A JSON array of exactly 3 bullet points/insights.
    - "cta": A punchy call-to-action (under 8 words).
    """
    script_text = call_gemini_safe(script_prompt)
    try:
        cleaned_script = re.sub(r'^```json\s*|```$', '', script_text.strip(), flags=re.MULTILINE)
        script_data = json.loads(cleaned_script)
    except Exception:
        script_data = {
            "hook": f"Here is why '{top_trend['title']}' is currently taking over {niche}!",
            "story": f"Everyone in the creator space is talking about this development. It changes the way we look at {niche} scaling, paving the way for rapid, automated implementation.",
            "insights": [
                "It reduces deployment cycles from weeks to just a few seconds.",
                "It requires virtually zero upfront capital to kickstart production.",
                "Pioneering creators are scaling engagement by 300% using this methodology."
            ],
            "cta": "Tap follow for daily insights!"
        }

    # ----------------------------------------------------
    # STEP 4: LINKEDIN CONTENT GENERATOR
    # ----------------------------------------------------
    print("Generating LinkedIn post...")
    linkedin_prompt = f"""
    Create a highly professional, engaging LinkedIn post based on this viral script:
    Hook: {script_data['hook']}
    Story: {script_data['story']}
    Insights: {', '.join(script_data['insights'])}
    
    Format the response strictly as a JSON object. Do not include markdown code block tags.
    JSON Keys:
    - "post": A formatted multi-line post with line breaks and appropriate emojis.
    - "hashtags": 4-5 relevant LinkedIn hashtags (e.g. #Technology).
    - "engagement_hook": A question at the end to spark debate.
    """
    linkedin_text = call_gemini_safe(linkedin_prompt)
    try:
        cleaned_li = re.sub(r'^```json\s*|```$', '', linkedin_text.strip(), flags=re.MULTILINE)
        linkedin_data = json.loads(cleaned_li)
    except Exception:
        linkedin_data = {
            "post": f"The landscape of {niche} is changing right before our eyes. 🚀\n\nRecent developments show that '{top_trend['title']}' is gaining explosive momentum. Here are the core details you need to know:\n\n💡 Key takeaways:\n1. It reduces standard production timeframes drastically.\n2. Access is democratized, letting solo operators scale at enterprise level.\n3. The growth velocity is outpacing traditional methods by 3x.\n\nThis marks a new era in creators leveraging AI to dominate their spaces.",
            "hashtags": f"#niche #StartupLife #BusinessGrowth #{niche.replace(' ', '')}",
            "engagement_hook": "Is this a temporary hype or the new normal? Let me know your thoughts!"
        }

    # ----------------------------------------------------
    # STEP 5: INSTAGRAM CONTENT GENERATOR
    # ----------------------------------------------------
    print("Generating Instagram post...")
    instagram_prompt = f"""
    Create an energetic Instagram post caption based on this viral script:
    Hook: {script_data['hook']}
    Story: {script_data['story']}
    
    Format the response strictly as a JSON object. Do not include markdown code block tags.
    JSON Keys:
    - "caption": A conversational caption (under 150 words) with emojis.
    - "hashtags": 5-10 relevant hashtags.
    - "cta": A call to action (e.g. Save this for later!).
    """
    instagram_text = call_gemini_safe(instagram_prompt)
    try:
        cleaned_ig = re.sub(r'^```json\s*|```$', '', instagram_text.strip(), flags=re.MULTILINE)
        instagram_data = json.loads(cleaned_ig)
    except Exception:
        instagram_data = {
            "caption": f"Huge news in the {niche} scene today! 🔥 '{top_trend['title']}' is officially changing the game. If you're building in this space, you can't afford to ignore this. Let's discuss in the comments below! 👇",
            "hashtags": f"#viralreels #growthmindset #{niche.lower().replace(' ', '')} #digitalmarketing #trends",
            "cta": "Save this reel for later! 📌"
        }

    # ----------------------------------------------------
    # STEP 6: VIRALITY PREDICTION
    # ----------------------------------------------------
    print("Running XGBoost virality prediction...")
    hook_word_count = len(script_data['hook'].split())
    
    # Run XGBoost inference
    input_data = pd.DataFrame([{
        "trend_score": top_trend["score"],
        "hook_word_count": hook_word_count,
        "novelty": top_trend["novelty"]
    }])
    pred_score = xgb_model.predict(input_data)[0]
    pred_score = round(float(pred_score), 1)
    pred_score = min(max(pred_score, 35.0), 99.4)  # Clamp to reasonable virality scores

    # Generate analytics cards metrics
    expected_views = int(pred_score * 11500 + random.randint(5000, 25000))
    expected_likes = int(expected_views * 0.075 + random.randint(100, 500))
    expected_shares = int(expected_views * 0.025 + random.randint(15, 100))
    expected_saves = int(expected_views * 0.045 + random.randint(30, 200))

    # Generate charts data
    # 1. Projected engagement over 24 hours (accumulated views)
    hourly_engagement = []
    accumulated_views = 0
    for hour in range(1, 25):
        # S-curve shape for viral views accumulation
        multiplier = 1 / (1 + np.exp(-0.25 * (hour - 10)))
        current_views = int(expected_views * multiplier)
        hourly_engagement.append({
            "hour": f"{hour}h",
            "views": current_views,
            "likes": int(current_views * 0.075)
        })

    # 2. Performance metrics comparison across platforms
    platform_performance = [
        {"platform": "Instagram Reels", "expected_reach": expected_views},
        {"platform": "TikTok", "expected_reach": int(expected_views * 1.45)},
        {"platform": "YouTube Shorts", "expected_reach": int(expected_views * 0.85)},
        {"platform": "LinkedIn Video", "expected_reach": int(expected_views * 0.12)}
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

    # Compile the final result
    payload = {
        "niche": niche,
        "top_trend": top_trend,
        "trends": ranked_trends,
        "script": script_data,
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
