# 🚀 Ratefluencer AI

### AI Viral Reel Creator & Virality Prediction Platform

Ratefluencer AI is an end-to-end AI-powered content creation platform that automatically discovers trends, generates viral content ideas, creates short-form reel scripts, produces downloadable MP4 reels, generates LinkedIn and Instagram content, and predicts content virality before publishing.

Built for **Track 2: AI Viral Reel Creator Agent Hackathon Challenge**.

---

# 🎯 Problem Statement

Content creators spend hours:

* Searching for trends
* Finding content ideas
* Writing scripts
* Creating reels
* Writing captions
* Publishing content
* Predicting performance

Ratefluencer AI automates the complete workflow using AI agents.

---

# 💡 Solution

Ratefluencer AI provides a one-click workflow:

Topic Input
→ Trend Discovery
→ Trend Ranking
→ Content Ideas
→ Reel Script Generation
→ Reel Production
→ LinkedIn Content
→ Instagram Content
→ Virality Prediction

The platform transforms a simple topic into a complete social media campaign package.

---

# ✨ Features

## 🔍 Trend Discovery Agent

Collects and analyzes trends from:

* Reddit
* TechCrunch RSS
* The Verge RSS
* Google News RSS

Generates:

* Trend Score
* Growth Velocity
* Engagement Potential
* Audience Relevance

---

## 📈 Trend Ranking Agent

Ranks discovered trends using:

* Growth Velocity
* Search Interest
* Engagement Potential
* Novelty
* Audience Relevance

Outputs:

* Top Ranked Trends
* Trend Scores (0–100)

---

## 💡 Content Idea Agent

Generates:

* Viral Content Ideas
* Audience Targeting
* Engagement Potential
* Virality Estimates

Provides multiple content directions for creators.

---

## ✍️ Script Generation Agent

Creates short-form content scripts containing:

* Hook
* Story
* Key Insights
* Call-To-Action

Optimized for:

* Instagram Reels
* YouTube Shorts
* LinkedIn Video Content

---

## 🎬 Reel Generation Agent

Automatically creates:

* Scene Breakdown
* Voiceover Script
* Subtitle Script
* Thumbnail Prompt
* Storyboard
* Downloadable MP4 Reel

Workflow:

Script
→ Storyboard
→ Visual Slides
→ Voiceover
→ MoviePy Rendering
→ MP4 Export

---

## 💼 LinkedIn Content Agent

Generates:

* Professional LinkedIn Posts
* Engagement Hooks
* Hashtags
* Call-To-Actions

Also creates:

* LinkedIn Graphic Prompt

---

## 📱 Instagram Content Agent

Generates:

* Instagram Captions
* Hashtags
* Engagement CTAs

Also creates:

* Thumbnail Prompts

---

## 📊 Virality Prediction Agent

Predicts:

* Expected Views
* Expected Likes
* Expected Shares
* Expected Saves
* Virality Score

Provides reasoning behind predictions.

---

# 🏗️ System Architecture

```text
User Topic
    ↓
Trend Discovery Agent
    ↓
Trend Ranking Agent
    ↓
Content Idea Agent
    ↓
Script Generation Agent
    ↓
Reel Generation Agent
    ↓
LinkedIn Agent
    ↓
Instagram Agent
    ↓
Virality Prediction Agent
    ↓
Export Package
```

# 🛠️ Tech Stack

Frontend

* Streamlit

Backend

* Python

AI

* Google Gemini 2.5 Flash

Content Sources

* Reddit Public APIs
* TechCrunch RSS
* The Verge RSS
* Google News RSS

Video Generation

* MoviePy
* gTTS

Machine Learning

* XGBoost

Deployment

* Google Cloud Run

Version Control

* GitHub

# 📁 Project Structure

```text
ratefluencer-ai/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── README.md
├── .env.example
│
├── agents/
│   ├── trend_discovery.py
│   ├── trend_ranking.py
│   ├── content_ideas.py
│   ├── script_generator.py
│   ├── reel_generator.py
│   ├── linkedin_agent.py
│   ├── instagram_agent.py
│   └── virality_predictor.py
│
├── assets/
│
├── exports/
│
├── data/
│
└── docs/
```

# ⚙️ Environment Variables

Create a `.env` file:

```env
PROJECT_ID=my-sample-project-495116
```

# 🚀 Local Installation

Clone repository:

```bash
git clone <repository-url>
cd ratefluencer-ai
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run application:

```bash
streamlit run app.py
```

# ☁️ Google Cloud Deployment

Build Docker image:

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/ratefluencer-ai
```

Deploy to Cloud Run:

```bash
gcloud run deploy ratefluencer-ai \
--image gcr.io/PROJECT_ID/ratefluencer-ai \
--platform managed \
--region us-central1 \
--allow-unauthenticated
```

# 🎥 Demo Workflow

1. Enter a topic
2. Click "Generate Viral Campaign"
3. Discover trends
4. Select content idea
5. Generate reel
6. Download MP4
7. Generate LinkedIn post
8. Generate Instagram caption
9. Review virality score
10. Export campaign package

# 📦 Export Package

The platform exports:

* Trend Analysis
* Selected Content Idea
* Reel Script
* Voiceover Script
* Storyboard
* LinkedIn Post
* Instagram Caption
* Virality Prediction

Available formats:

* PDF
* JSON
* Text Summary

# 🔮 Future Improvements

* Real-time YouTube trend discovery
* AI image generation integration
* LinkedIn direct publishing
* Instagram direct publishing
* Multi-language support
* Team collaboration
* Creator analytics dashboard
* AI video scene generation

# 👨‍💻 Team

Built for the AI Viral Reel Creator Hackathon.

Ratefluencer AI demonstrates how autonomous AI agents can automate the entire content creation lifecycle from trend discovery to publishing-ready assets.

# ⭐ Conclusion

Ratefluencer AI enables creators, marketers, startups, and businesses to transform a single topic into a complete viral content campaign within minutes using AI-powered automation.
