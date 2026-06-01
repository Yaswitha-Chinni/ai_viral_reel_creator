/* --------------------------------------------------------------------------
   Ratefluencer AI - Core Frontend Logic (Hackathon Track 2 Edition)
   -------------------------------------------------------------------------- */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize Lucide Icons
    lucide.createIcons();

    // DOM Elements - Navigation & Routing
    const navItems = document.querySelectorAll('.nav-item');
    const viewSections = document.querySelectorAll('.view-section');

    // DOM Elements - Search Console
    const nicheInput = document.getElementById('niche-input');
    const generateBtn = document.getElementById('generate-button');
    const quickTags = document.querySelectorAll('.tag-btn');
    const demoBtn = document.getElementById('hackathon-demo-button');

    // DOM Elements - Wizard modal
    const wizardModal = document.getElementById('wizard-modal');
    const wizardProgressBar = document.getElementById('wizard-progress-bar');
    const wizardGlobalStatus = document.getElementById('wizard-global-status');

    // DOM Elements - Trends Panel Drawer
    const trendsCardsContainer = document.getElementById('trends-cards-container');
    const trendsSidePanel = document.getElementById('trends-side-panel');
    const drawerBackdrop = document.getElementById('drawer-backdrop-overlay');
    const closeDrawerBtn = document.getElementById('close-drawer-button');
    const drawerContent = document.getElementById('drawer-content-container');

    // DOM Elements - Studio Tabs & Panels
    const studioTabs = document.querySelectorAll('.studio-tab-item');
    const studioPanels = document.querySelectorAll('.studio-tab-panel');
    const copyStudioBtn = document.getElementById('studio-copy-btn');
    const regenStudioBtn = document.getElementById('studio-regenerate-btn');
    const exportStudioBtn = document.getElementById('studio-export-btn');
    const studioToast = document.getElementById('studio-toast');
    const ideasContainer = document.getElementById('studio-ideas-container');

    // DOM Elements - Reel Production Studio
    const rstudioVoiceover = document.getElementById('rstudio-voiceover-text');
    const rstudioThumbnail = document.getElementById('rstudio-thumbnail-prompt');
    const rstudioBroll = document.getElementById('rstudio-broll-text');
    const rstudioTimeline = document.getElementById('rstudio-scenes-timeline');
    const copyThumbPromptBtn = document.getElementById('copy-thumb-prompt-btn');

    // Chart instances
    let gaugeChartInstance = null;
    let lineChartInstance = null;
    let barChartInstance = null;

    // Generated data store
    let generatedData = null;
    let generatedIdeasPayload = null; // Store trends and ideas from Stage 1
    let activeNiche = "Creator Economy";

    // Premium Demo Data (Loaded on startup & used in Demo Mode)
    const demoData = {
        niche: "Creator Economy",
        top_trend: {
            title: "Auditing recursive loop nodes to prevent run-away vector database bills",
            source: "TechCrunch",
            upvotes: 1840,
            num_comments: 310,
            score: 94.6,
            growth_velocity: 88.5,
            novelty: 92.0,
            engagement_potential: 89.2,
            audience_relevance: 96.0
        },
        ideas: [
            {
                title: "Why solo founders are deploying autonomous agent loops",
                target_audience: "Solopreneurs & Indie Hackers",
                virality_potential: "High",
                estimated_engagement: "92%"
            },
            {
                title: "The recursive API billing trap: audit your loops",
                target_audience: "SaaS Engineers",
                virality_potential: "Extreme",
                estimated_engagement: "96%"
            },
            {
                title: "Chatbots are dead, agent workspaces are taking over",
                target_audience: "Tech Enthusiasts & Founders",
                virality_potential: "Critical",
                estimated_engagement: "89%"
            },
            {
                title: "Auditing loop nodes in your vector database pipeline",
                target_audience: "Data Architects",
                virality_potential: "Moderate",
                estimated_engagement: "74%"
            },
            {
                title: "The ultimate framework for scaling Agentic AI in 2026",
                target_audience: "CTOs & Product Owners",
                virality_potential: "High",
                estimated_engagement: "82%"
            }
        ],
        script: {
            hook: "Stop coding chat panels. The future of software is autonomous loops.",
            story: "Indie hackers are deploying recursive agent nodes to build complete applications in minutes. But unchecked loops can spike your API bills by 10x overnight.",
            insights: [
                "Agent nodes execute multi-step tasks autonomously.",
                "Recursive loops without limits can lead to infinite API bills.",
                "Auditing loop iterations prevents high billing spikes."
            ],
            cta: "Tap follow to audit your loop nodes!"
        },
        reel_studio: {
            voiceover_script: "Stop coding chat panels. The future of software is autonomous loops. Indie hackers are deploying recursive agent nodes to build complete applications in minutes. But be careful: unchecked loops can spike your API bills by 10x overnight. Save this post to learn how to audit your agent pipelines!",
            thumbnail_prompt: "A modern glow UI displaying recursive digital lines. Text overlay in bold Outfit typography: 'CHATS ARE DEAD: THE AGENTIC ERA.' Glowing cyan and purple accents, high tech dark background.",
            b_roll_suggestions: "Close-up of keyboard typing, terminal code scrolling, floating agent loop diagram, credit card invoice showing high API usage, mobile screen warning alert.",
            scenes: [
                {
                    scene_number: 1,
                    duration: "0-5s",
                    title: "Scene 1: Hook visual",
                    visual_prompt: "Close-up of a developer shutting down a standard chat screen. Transitioning to a glowing recursive database console.",
                    b_roll: "Close-up of hands shutting laptop screen.",
                    subtitle: "Stop coding chat panels. The future is autonomous loops."
                },
                {
                    scene_number: 2,
                    duration: "5-20s",
                    title: "Scene 2: Problem visualization",
                    visual_prompt: "Screen view showing a fast-scrolling terminal running agent scripts, with a high API usage overlay blinking in neon orange.",
                    b_roll: "Fast scrolling code on terminal.",
                    subtitle: "Indie hackers are deploying loop agents... but it can spike your API bills by 10x!"
                },
                {
                    scene_number: 3,
                    duration: "20-35s",
                    title: "Scene 3: Main insight",
                    visual_prompt: "A diagram mapping a loop node audit workflow. Highlights of database auditing tools glowing in neon purple.",
                    b_roll: "Audit diagram workflow panning.",
                    subtitle: "Audit your loops and scale agent workloads safely."
                },
                {
                    scene_number: 4,
                    duration: "35-45s",
                    title: "Scene 4: Call to action",
                    visual_prompt: "End screen showing social icon handles with a pulse effect. Text overlay: 'SAVE FOR LATER'.",
                    b_roll: "Save icon animation pulsing.",
                    subtitle: "Tap follow and save this post to audit your pipelines!"
                }
            ]
        },
        linkedin: {
            post: "SaaS architecture is pivoting. Autonomous loops are replacing text prompts. 🤖\n\nSolo developers are currently using multi-agent loops to construct full projects. However, unchecked recursive pipelines are causing massive database overhead and infinite API bills.\n\nHere are 3 keys to building loop agents safely:\n1️⃣ Establish iteration caps: Hard limits prevent infinite loops.\n2️⃣ Implement budget alerts: Real-time spend caps block runaway requests.\n3️⃣ Run local audit logs: Track recursive nodes before production push.\n\nAre you building traditional chat interfaces, or are you deploying loop nodes?",
            hashtags: "#ArtificialIntelligence #SaaS #FutureOfCoding #DatabaseDesign",
            engagement_hook: "How is your engineering team adapting to autonomous agent nodes? Let's discuss below!"
        },
        instagram: {
            caption: "Chats are legacy. Loops are next. ⚡ Solo founders are scaling systems by deploying autonomous agent nodes. But beware of recursive API traps! Swipe left to read how to build loops safely! 👇",
            hashtags: "#aidevelopment #agentic #saasstartup #codinglife #databaseaudit #indiehackers",
            cta: "Save this reel to protect your vector pipelines! 📌"
        },
        virality: {
            virality_score: 92.4,
            expected_views: 1150000,
            expected_likes: 86250,
            expected_shares: 28750,
            expected_saves: 51750,
            hourly_engagement: [
                { hour: "1h", views: 24000, likes: 1800 },
                { hour: "2h", views: 58000, likes: 4350 },
                { hour: "4h", views: 180000, likes: 13500 },
                { hour: "6h", views: 420000, likes: 31500 },
                { hour: "8h", views: 680000, likes: 51000 },
                { hour: "12h", views: 920000, likes: 69000 },
                { hour: "16h", views: 1050000, likes: 78750 },
                { hour: "20h", views: 1120000, likes: 84000 },
                { hour: "24h", views: 1150000, likes: 86250 }
            ],
            platform_performance: [
                { platform: "Instagram Reels", expected_reach: 1150000 },
                { platform: "TikTok", expected_reach: 1667500 },
                { platform: "YouTube Shorts", expected_reach: 977500 },
                { platform: "LinkedIn Video", expected_reach: 138000 }
            ]
        }
    };

    // ==========================================
    // 1. ROUTER SYSTEM (Hash-based)
    // ==========================================
    function handleRouting() {
        const hash = window.location.hash || '#dashboard';
        
        // Remove active class from links and hide sections
        navItems.forEach(item => item.classList.remove('active'));
        viewSections.forEach(section => section.classList.add('hide'));
        
        // Find matching view container
        let targetViewId = '';
        if (hash === '#reel-studio') {
            targetViewId = 'reel-studio-view';
        } else {
            targetViewId = `${hash.slice(1)}-view`;
        }
        
        const targetSection = document.getElementById(targetViewId);
        let navId = `nav-${hash.slice(1)}`;
        if (hash === '#reel-studio') navId = 'nav-reel-studio';
        const targetNavLink = document.getElementById(navId);
        
        if (targetSection && targetNavLink) {
            targetSection.classList.remove('hide');
            targetNavLink.classList.add('active');
            window.scrollTo(0, 0);
        } else {
            document.getElementById('dashboard-view').classList.remove('hide');
            document.getElementById('nav-dashboard').classList.add('active');
        }

        closeDrawer();
    }

    window.addEventListener('hashchange', handleRouting);
    
    // Quick tags
    quickTags.forEach(tag => {
        tag.addEventListener('click', () => {
            nicheInput.value = tag.getAttribute('data-topic');
            nicheInput.focus();
        });
    });

    // ==========================================
    // 2. TWO-STAGE WORKFLOW ENGINE
    // ==========================================
    
    // Agent Monitor status updates
    function setAgentStatus(agentIndex, status) {
        // status is 'waiting', 'running', 'completed', 'failed'
        const row = document.getElementById(`monitor-agent-${agentIndex}`);
        if (!row) return;
        const tag = row.querySelector('.agent-status-tag');
        
        tag.className = `agent-status-tag ${status}`;
        tag.innerText = status;
    }

    function resetAgentMonitor() {
        for (let i = 1; i <= 8; i++) {
            setAgentStatus(i, 'waiting');
        }
    }

    // STAGE 1: Generate Ideas
    generateBtn.addEventListener('click', () => {
        const topic = nicheInput.value.trim() || "Creator Economy";
        activeNiche = topic;
        runStage1Pipeline(topic);
    });

    nicheInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const topic = nicheInput.value.trim() || "Creator Economy";
            activeNiche = topic;
            runStage1Pipeline(topic);
        }
    });

    function runStage1Pipeline(niche) {
        wizardModal.classList.remove('hide');
        wizardProgressBar.style.width = '0%';
        resetWizardSteps();
        resetAgentMonitor();
        
        // Stage 1 Endpoint
        const apiPromise = fetch('/api/generate-ideas', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic: niche })
        }).then(res => {
            if (!res.ok) throw new Error("Stage 1 failed");
            return res.json();
        });

        executeStage1Animations(apiPromise);
    }

    function resetWizardSteps() {
        for (let i = 1; i <= 8; i++) {
            const node = document.getElementById(`wstep-${i}`);
            node.classList.remove('active', 'done');
            node.querySelector('.spinner-mini').classList.add('hide');
            node.querySelector('.check-icon').classList.add('hide');
        }
    }

    async function executeStage1Animations(apiPromise) {
        const stepTimings = [1000, 1200, 1200];
        const statusPhrases = [
            "Agent 1: Scanning RSS feeds and Reddit indices...",
            "Agent 2: Scoring metrics via RandomForest weights...",
            "Agent 3: Generating viral content idea options..."
        ];

        // Step 1 active
        activateWizardStepNode(1);
        setAgentStatus(1, 'running');

        for (let i = 1; i <= 3; i++) {
            wizardGlobalStatus.innerText = statusPhrases[i-1];
            await new Promise(resolve => setTimeout(resolve, stepTimings[i-1]));
            
            // Mark step i as done
            completeWizardStepNode(i);
            setAgentStatus(i, 'completed');
            wizardProgressBar.style.width = `${Math.round((i / 8) * 100)}%`;
            
            if (i < 3) {
                activateWizardStepNode(i+1);
                setAgentStatus(i+1, 'running');
            }
        }

        try {
            const data = await apiPromise;
            generatedIdeasPayload = data;
            
            // Populate Stage 1 outputs
            populateStage1Outputs(data);
            
            // Hide wizard, open Content Studio Ideas
            setTimeout(() => {
                wizardModal.classList.add('hide');
                window.location.hash = '#content-studio';
                showToast("Content ideas generated! Click on a card below to compile assets.");
            }, 400);

        } catch (err) {
            console.error(err);
            wizardModal.classList.add('hide');
            alert("Error in Stage 1 content discovery. Check backend connection.");
        }
    }

    function activateWizardStepNode(index) {
        const card = document.getElementById(`wstep-${index}`);
        card.classList.add('active');
        card.querySelector('.spinner-mini').classList.remove('hide');
    }

    function completeWizardStepNode(index) {
        const card = document.getElementById(`wstep-${index}`);
        card.classList.remove('active');
        card.classList.add('done');
        card.querySelector('.spinner-mini').classList.add('hide');
        card.querySelector('.check-icon').classList.remove('hide');
    }

    function populateStage1Outputs(data) {
        // Update Dashboard Stats
        document.getElementById('stat-total-trends').innerText = data.trends.length;
        const avgTrendScore = (data.trends.reduce((sum, item) => sum + item.score, 0) / data.trends.length).toFixed(1);
        document.getElementById('stat-avg-trend-score').innerText = `${avgTrendScore}`;
        
        // Populate Trends Cards Grid
        trendsCardsContainer.innerHTML = '';
        data.trends.forEach((item, index) => {
            const isWinner = index === 0;
            const card = document.createElement('div');
            card.className = `glassmorphism trend-card ${isWinner ? 'top-winner-card' : ''}`;
            card.innerHTML = `
                <div class="trend-card-left">
                    <div class="trend-card-source-row">
                        <span class="trend-source-badge">${item.source}</span>
                        ${isWinner ? '<span class="top-star-badge"><i data-lucide="star"></i> WINNER</span>' : ''}
                    </div>
                    <h3 class="trend-card-title">${item.title}</h3>
                    <span class="trend-card-growth"><i data-lucide="trending-up"></i> +${item.growth_velocity}% Velocity</span>
                </div>
                <div class="trend-card-right">
                    <span class="trend-card-score-lbl">Score</span>
                    <span class="trend-card-score-val">${item.score}</span>
                </div>
            `;
            card.addEventListener('click', () => openSidePanel(item));
            trendsCardsContainer.appendChild(card);
        });

        // Populate Content Ideas list
        ideasContainer.innerHTML = '';
        data.ideas.forEach((idea, index) => {
            const card = document.createElement('div');
            card.className = "idea-card-item";
            card.innerHTML = `
                <div class="idea-card-left">
                    <h4 class="idea-card-title">${idea.title}</h4>
                    <span class="idea-card-audience"><i data-lucide="users" style="width:12px;height:12px;display:inline-block;vertical-align:middle;margin-right:4px;"></i> Audience: ${idea.target_audience}</span>
                </div>
                <div class="idea-card-right">
                    <span class="idea-badge virality">Virality: ${idea.virality_potential}</span>
                    <span class="idea-badge engagement">Engagement: ${idea.estimated_engagement}</span>
                    <button class="idea-select-btn">Select Idea</button>
                </div>
            `;
            
            // Selection event triggers Stage 2
            card.querySelector('.idea-select-btn').addEventListener('click', (e) => {
                e.stopPropagation();
                // Toggle select UI
                document.querySelectorAll('.idea-card-item').forEach(c => c.classList.remove('selected'));
                card.classList.add('selected');
                
                runStage2Pipeline(idea);
            });

            ideasContainer.appendChild(card);
        });
        
        lucide.createIcons();
    }

    // STAGE 2: Generate script, Reel Studio, social copies, virality prediction
    function runStage2Pipeline(selectedIdea) {
        wizardModal.classList.remove('hide');
        // Resume progress from 37.5% (3/8 completed)
        wizardProgressBar.style.width = '37.5%';
        
        // Complete nodes 1-3
        for (let i = 1; i <= 3; i++) {
            const node = document.getElementById(`wstep-${i}`);
            node.classList.add('done');
            node.querySelector('.check-icon').classList.remove('hide');
            setAgentStatus(i, 'completed');
        }

        // Call Stage 2 API
        const apiPromise = fetch('/api/generate-assets', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                niche: activeNiche,
                selected_trend: generatedIdeasPayload.top_trend,
                selected_idea: selectedIdea
            })
        }).then(res => {
            if (!res.ok) throw new Error("Stage 2 failed");
            return res.json();
        });

        executeStage2Animations(apiPromise, selectedIdea);
    }

    async function executeStage2Animations(apiPromise, selectedIdea) {
        const stepTimings = [800, 1000, 800, 800, 1000];
        const statusPhrases = [
            "Agent 4: Writing vertical script via Gemini...",
            "Agent 5: Building scene timelines and thumbnail layouts...",
            "Agent 6: Structuring LinkedIn professional post...",
            "Agent 7: Framing Instagram feed hashtags...",
            "Agent 8: Running virality prediction index on XGBoost..."
        ];

        for (let i = 4; i <= 8; i++) {
            wizardGlobalStatus.innerText = statusPhrases[i-4];
            activateWizardStepNode(i);
            setAgentStatus(i, 'running');
            
            await new Promise(resolve => setTimeout(resolve, stepTimings[i-4]));
            
            completeWizardStepNode(i);
            setAgentStatus(i, 'completed');
            wizardProgressBar.style.width = `${Math.round((i / 8) * 100)}%`;
        }

        try {
            const assets = await apiPromise;
            
            // Combine data payloads
            generatedData = {
                niche: activeNiche,
                top_trend: generatedIdeasPayload.top_trend,
                ideas: generatedIdeasPayload.ideas,
                selected_idea: selectedIdea,
                script: assets.script,
                reel_studio: assets.reel_studio,
                linkedin: assets.linkedin,
                instagram: assets.instagram,
                virality: assets.virality
            };

            // Populate Stage 2 views
            populateStage2Outputs(generatedData);
            
            setTimeout(() => {
                wizardModal.classList.add('hide');
                // Auto route to Content Studio Script tab so they see what they generated
                window.location.hash = '#content-studio';
                // Activate Script tab
                document.getElementById('tab-reel').click();
                showToast("Automated Creator Package completed successfully!");
            }, 400);

        } catch (err) {
            console.error(err);
            wizardModal.classList.add('hide');
            alert("Error compiling campaign assets.");
        }
    }

    function populateStage2Outputs(data) {
        // Average virality score
        const viralityScore = Math.round(data.virality.virality_score);
        document.getElementById('stat-avg-virality-score').innerText = `${viralityScore}%`;
        document.getElementById('stat-content-count').innerText = "4 Assets";

        // Tab 1: Script
        document.getElementById('studio-script-hook').innerText = `"${data.script.hook}"`;
        document.getElementById('studio-script-story').innerText = `"${data.script.story}"`;
        const insightsUl = document.getElementById('studio-script-insights');
        insightsUl.innerHTML = '';
        data.script.insights.forEach(insight => {
            const li = document.createElement('li');
            li.innerText = insight;
            insightsUl.appendChild(li);
        });
        document.getElementById('studio-script-cta').innerText = `"${data.script.cta}"`;

        // Tab 2: LinkedIn
        document.getElementById('studio-linkedin-body').innerText = data.linkedin.post;
        document.getElementById('studio-linkedin-hashtags').innerText = data.linkedin.hashtags;
        document.getElementById('studio-linkedin-engagement').innerText = `🎯 Catalyst: ${data.linkedin.engagement_hook}`;

        // Tab 3: Instagram
        document.getElementById('studio-instagram-body').innerText = data.instagram.caption;
        document.getElementById('studio-instagram-hashtags').innerText = data.instagram.hashtags;
        document.getElementById('studio-instagram-cta').innerText = `📌 CTA: ${data.instagram.cta}`;

        // Populate Reel Studio Panel
        rstudioVoiceover.innerText = data.reel_studio.voiceover_script;
        rstudioThumbnail.innerText = data.reel_studio.thumbnail_prompt;
        rstudioBroll.innerText = data.reel_studio.b_roll_suggestions;

        // Populate Vertical Storyboard Timeline
        rstudioTimeline.innerHTML = '';
        data.reel_studio.scenes.forEach(scene => {
            const card = document.createElement('div');
            card.className = "timeline-scene-card";
            card.innerHTML = `
                <div class="timeline-scene-node-dot"></div>
                <div class="timeline-scene-header">
                    <span class="timeline-scene-title">${scene.title}</span>
                    <span class="timeline-scene-duration">${scene.duration}</span>
                </div>
                <div class="timeline-scene-detail-row">
                    <div class="timeline-scene-group">
                        <span class="timeline-scene-lbl">Visual Asset Prompt</span>
                        <p class="timeline-scene-text">${scene.visual_prompt}</p>
                    </div>
                    <div class="timeline-scene-group">
                        <span class="timeline-scene-lbl">B-Roll Footage suggestion</span>
                        <p class="timeline-scene-text">${scene.b_roll}</p>
                    </div>
                    <div class="timeline-scene-group">
                        <span class="timeline-scene-lbl">Subtitle Content overlay</span>
                        <p class="timeline-scene-text subtitle-text">"${scene.subtitle}"</p>
                    </div>
                </div>
            `;
            rstudioTimeline.appendChild(card);
        });

        // Populate Analytics elements
        document.getElementById('virality-percentage').innerText = `${viralityScore}%`;
        document.getElementById('metric-views').innerText = formatCounter(data.virality.expected_views);
        document.getElementById('metric-likes').innerText = formatCounter(data.virality.expected_likes);
        document.getElementById('metric-shares').innerText = formatCounter(data.virality.expected_shares);
        document.getElementById('metric-saves').innerText = formatCounter(data.virality.expected_saves);
        
        const verdictLbl = document.getElementById('status-verdict');
        const verdictDot = verdictLbl.previousElementSibling;
        
        if (viralityScore >= 80) {
            verdictLbl.innerText = "Highly Viral Potential";
            verdictLbl.style.color = "#10b981";
            verdictDot.style.backgroundColor = "#10b981";
        } else if (viralityScore >= 60) {
            verdictLbl.innerText = "Moderate Viral Potential";
            verdictLbl.style.color = "#f59e0b";
            verdictDot.style.backgroundColor = "#f59e0b";
        } else {
            verdictLbl.innerText = "Low Viral Potential";
            verdictLbl.style.color = "#red";
            verdictDot.style.backgroundColor = "#red";
        }

        // Render Charts
        renderCharts(data.virality);

        // Refresh icons
        lucide.createIcons();
    }

    // ==========================================
    // 3. HACKATHON DEMO MODE SIMULATION
    // ==========================================
    demoBtn.addEventListener('click', runHackathonDemoMode);

    async function runHackathonDemoMode() {
        console.log("Launching automated demo mode...");
        
        // Reset navigation back to Dashboard
        window.location.hash = '#dashboard';
        resetAgentMonitor();
        
        // Trigger modal overlay
        wizardModal.classList.remove('hide');
        wizardProgressBar.style.width = '0%';
        resetWizardSteps();
        
        const stepTimings = [1200, 1000, 1400, 900, 900, 800, 800, 1000];
        const statusPhrases = [
            "Demo Mode - Agent 1: Crawling daily technology newsletters & r/startups...",
            "Demo Mode - Agent 2: Sorting RandomForest ranking metrics...",
            "Demo Mode - Agent 3: Brainstorming content ideas cards...",
            "Demo Mode - Agent 4: Writing hook and Insights scripts...",
            "Demo Mode - Agent 5: Layouting scene production boards...",
            "Demo Mode - Agent 6: Optimization of LinkedIn copy text...",
            "Demo Mode - Agent 7: Tagging Instagram captions and CTAs...",
            "Demo Mode - Agent 8: Simulating XGBoost virality forecasting model..."
        ];

        // Animate all 8 steps sequentially, updating the Dashboard monitor rows
        for (let i = 1; i <= 8; i++) {
            wizardGlobalStatus.innerText = statusPhrases[i-1];
            activateWizardStepNode(i);
            setAgentStatus(i, 'running');
            
            await new Promise(resolve => setTimeout(resolve, stepTimings[i-1]));
            
            completeWizardStepNode(i);
            setAgentStatus(i, 'completed');
            wizardProgressBar.style.width = `${Math.round((i / 8) * 100)}%`;
            
            // Special middle transition: when Agent 3 finishes, simulate selecting an Idea!
            if (i === 3) {
                wizardGlobalStatus.innerText = "Demo Mode - System: Automatically selecting winning content idea...";
                // Load Stage 1 outputs
                generatedIdeasPayload = {
                    trends: demoData.trends,
                    top_trend: demoData.top_trend,
                    ideas: demoData.ideas
                };
                populateStage1Outputs(generatedIdeasPayload);
                
                // Visual delay
                await new Promise(resolve => setTimeout(resolve, 800));
            }
        }

        // Save demoData in memory
        generatedData = demoData;
        
        // Populate all views
        populateStage2Outputs(demoData);
        
        // Select the second card visually in Content Studio
        setTimeout(() => {
            const secondCard = document.querySelectorAll('.idea-card-item')[1];
            if (secondCard) secondCard.classList.add('selected');
        }, 1000);

        // Close wizard modal and route directly to Analytics
        setTimeout(() => {
            wizardModal.classList.add('hide');
            window.location.hash = '#analytics';
            showToast("Hackathon Demo complete! Panning analytics dashboard.");
        }, 600);
    }

    // ==========================================
    // 4. TREND SIDE PANEL DRAWER
    // ==========================================
    function openSidePanel(trend) {
        drawerContent.innerHTML = `
            <div class="drawer-title-group">
                <h2>${trend.title}</h2>
                <span class="trend-source-badge">${trend.source}</span>
            </div>
            
            <div class="drawer-metrics-list">
                <div class="drawer-metric-card">
                    <span class="drawer-metric-lbl">Growth Velocity</span>
                    <div class="drawer-metric-right">
                        <div class="drawer-metric-bar">
                            <div class="drawer-metric-bar-fill" style="width: ${trend.growth_velocity}%; background-color: var(--purple);"></div>
                        </div>
                        <span class="drawer-metric-val">${trend.growth_velocity}%</span>
                    </div>
                </div>

                <div class="drawer-metric-card">
                    <span class="drawer-metric-lbl">Novelty index</span>
                    <div class="drawer-metric-right">
                        <div class="drawer-metric-bar">
                            <div class="drawer-metric-bar-fill" style="width: ${trend.novelty}%; background-color: var(--blue);"></div>
                        </div>
                        <span class="drawer-metric-val">${trend.novelty}%</span>
                    </div>
                </div>

                <div class="drawer-metric-card">
                    <span class="drawer-metric-lbl">Engagement Potential</span>
                    <div class="drawer-metric-right">
                        <div class="drawer-metric-bar">
                            <div class="drawer-metric-bar-fill" style="width: ${trend.engagement_potential}%; background-color: var(--cyan);"></div>
                        </div>
                        <span class="drawer-metric-val">${trend.engagement_potential}%</span>
                    </div>
                </div>

                <div class="drawer-metric-card">
                    <span class="drawer-metric-lbl">Audience Relevance</span>
                    <div class="drawer-metric-right">
                        <div class="drawer-metric-bar">
                            <div class="drawer-metric-bar-fill" style="width: ${trend.audience_relevance}%; background-color: var(--pink);"></div>
                        </div>
                        <span class="drawer-metric-val">${trend.audience_relevance}%</span>
                    </div>
                </div>

                <div class="final-score-card">
                    <span class="drawer-metric-lbl" style="font-weight: 700;">Final Weighted Score</span>
                    <span class="final-score-val" style="font-size: 20px; font-weight:800; color: var(--cyan);">${trend.score}/100</span>
                </div>
            </div>
        `;
        
        trendsSidePanel.classList.add('open');
        drawerBackdrop.classList.remove('hide');
    }

    function closeDrawer() {
        trendsSidePanel.classList.remove('open');
        drawerBackdrop.classList.add('hide');
    }

    closeDrawerBtn.addEventListener('click', closeDrawer);
    drawerBackdrop.addEventListener('click', closeDrawer);

    // ==========================================
    // 5. STUDIO WORKSPACE TAB SWITCHER
    // ==========================================
    studioTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabId = tab.getAttribute('id');
            const targetPanelId = `panel-${tabId.split('-')[1]}`;
            
            // Switch tabs
            studioTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // Switch panels
            studioPanels.forEach(p => p.classList.remove('active'));
            document.getElementById(targetPanelId).classList.add('active');
        });
    });

    // Clipboard copy action
    copyStudioBtn.addEventListener('click', () => {
        if (!generatedData) return;
        
        const activeTab = document.querySelector('.studio-tab-item.active').getAttribute('id');
        let textToCopy = '';
        
        if (activeTab === 'tab-ideas') {
            textToCopy = generatedData.ideas.map((id, index) => `${index+1}. ${id.title} (${id.target_audience})`).join('\n');
        } else if (activeTab === 'tab-reel') {
            textToCopy = `HOOK: ${generatedData.script.hook}\nSTORY: ${generatedData.script.story}\nINSIGHTS:\n- ${generatedData.script.insights.join('\n- ')}\nCTA: ${generatedData.script.cta}`;
        } else if (activeTab === 'tab-linkedin') {
            textToCopy = `${generatedData.linkedin.post}\n\n${generatedData.linkedin.hashtags}\n\n${generatedData.linkedin.engagement_hook}`;
        } else if (activeTab === 'tab-instagram') {
            textToCopy = `${generatedData.instagram.caption}\n\n${generatedData.instagram.hashtags}\n\n${generatedData.instagram.cta}`;
        }
        
        navigator.clipboard.writeText(textToCopy).then(() => {
            copyStudioBtn.classList.add('copied');
            const originalHTML = copyStudioBtn.innerHTML;
            copyStudioBtn.innerHTML = '<i data-lucide="check"></i> Copied!';
            lucide.createIcons();
            
            setTimeout(() => {
                copyStudioBtn.classList.remove('copied');
                copyStudioBtn.innerHTML = originalHTML;
                lucide.createIcons();
            }, 2000);
        });
    });

    // Copy Thumbnail Prompt
    copyThumbPromptBtn.addEventListener('click', () => {
        if (!generatedData) return;
        navigator.clipboard.writeText(generatedData.reel_studio.thumbnail_prompt).then(() => {
            copyThumbPromptBtn.classList.add('copied');
            const originalHTML = copyThumbPromptBtn.innerHTML;
            copyThumbPromptBtn.innerHTML = '<i data-lucide="check"></i> Copied!';
            lucide.createIcons();
            
            setTimeout(() => {
                copyThumbPromptBtn.classList.remove('copied');
                copyThumbPromptBtn.innerHTML = originalHTML;
                lucide.createIcons();
            }, 2000);
        });
    });

    // Studio regenerate blueprint
    regenStudioBtn.addEventListener('click', () => {
        if (!generatedData) return;
        runStage1Pipeline(generatedData.niche);
    });

    // Studio report export (.md) - EXPANDED CREATOR PACKAGE
    exportStudioBtn.addEventListener('click', () => {
        if (!generatedData) return;

        const dateStr = new Date().toLocaleDateString('en-US', {
            year: 'numeric', month: 'long', day: 'numeric'
        });

        const report = `# Ratefluencer AI - Campaign Content blueprint (Creator Package)
Generated: ${dateStr}
Topic / Niche: **${generatedData.niche}**

---

## 1. Selected Content Idea
- **Selected Idea Title**: "${generatedData.selected_idea.title}"
- **Target Audience Profile**: ${generatedData.selected_idea.target_audience}
- **Estimated Engagement**: ${generatedData.selected_idea.estimated_engagement}
- **Virality Potential**: ${generatedData.selected_idea.virality_potential}

---

## 2. Short-Form Video Script
- **Hook**: "${generatedData.script.hook}"
- **Story Body**: "${generatedData.script.story}"
- **Key Takeaways**:
${generatedData.script.insights.map((ins, i) => `  ${i+1}. ${ins}`).join('\n')}
- **CTA**: "${generatedData.script.cta}"

---

## 3. Automated Reel Studio storyboard
- **Thumbnail Cover Prompt**: 
  *"${generatedData.reel_studio.thumbnail_prompt}"*

- **Voiceover Narration Script**: 
  *"${generatedData.reel_studio.voiceover_script}"*

- **B-Roll Suggestions**: 
  *"${generatedData.reel_studio.b_roll_suggestions}"*

- **Scene-by-Scene Timeline Breakdown**:
${generatedData.reel_studio.scenes.map(s => `
### Scene ${s.scene_number} (${s.duration}) - ${s.title}
- **Visual Asset Prompt**: ${s.visual_prompt}
- **B-Roll Footage suggestion**: ${s.b_roll}
- **Subtitle content overlay**: "${s.subtitle}"
`).join('\n')}

---

## 4. LinkedIn Native Post
\`\`\`text
${generatedData.linkedin.post}

${generatedData.linkedin.hashtags}
${generatedData.linkedin.engagement_hook}
\`\`\`

---

## 5. Instagram Feed Caption
\`\`\`text
${generatedData.instagram.caption}

${generatedData.instagram.hashtags}
${generatedData.instagram.cta}
\`\`\`

---

## 6. XGBoost Virality Prediction report
- **Predicted Virality Score**: ${generatedData.virality.virality_score}%
- **Expected Reach Profile**:
  - Expected Views: ${generatedData.virality.expected_views.toLocaleString()}
  - Expected Likes: ${generatedData.virality.expected_likes.toLocaleString()}
  - Expected Shares: ${generatedData.virality.expected_shares.toLocaleString()}
  - Expected Saves: ${generatedData.virality.expected_saves.toLocaleString()}
`;

        const blob = new Blob([report], { type: 'text/markdown;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.setAttribute('href', url);
        link.setAttribute('download', `ratefluencer_creator_package_${generatedData.niche.toLowerCase().replace(/[^a-z0-9]+/g, '_')}.md`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        showToast("Creator Package downloaded!");
    });

    function showToast(msg) {
        studioToast.innerHTML = `<i data-lucide="check-circle"></i> ${msg}`;
        studioToast.classList.remove('hide');
        lucide.createIcons();
        setTimeout(() => {
            studioToast.classList.add('hide');
        }, 3500);
    }

    // ==========================================
    // 6. CHART.JS VISUAL ENGINE
    // ==========================================
    function renderCharts(viralityData) {
        if (gaugeChartInstance) gaugeChartInstance.destroy();
        if (lineChartInstance) lineChartInstance.destroy();
        if (barChartInstance) barChartInstance.destroy();

        // Donut gauge
        const score = Math.round(viralityData.virality_score);
        const gaugeCtx = document.getElementById('viralityGaugeChart').getContext('2d');
        
        gaugeChartInstance = new Chart(gaugeCtx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [score, 100 - score],
                    backgroundColor: ['#8b5cf6', 'rgba(255, 255, 255, 0.05)'],
                    borderWidth: 0,
                    borderRadius: [10, 0]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '82%',
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: false }
                }
            }
        });

        // Projected engagement curve
        const lineCtx = document.getElementById('engagementLineChart').getContext('2d');
        const labels = viralityData.hourly_engagement.map(h => h.hour);
        const views = viralityData.hourly_engagement.map(h => h.views);
        const likes = viralityData.hourly_engagement.map(h => h.likes);

        const purpleGradient = lineCtx.createLinearGradient(0, 0, 0, 200);
        purpleGradient.addColorStop(0, 'rgba(139, 92, 246, 0.35)');
        purpleGradient.addColorStop(1, 'rgba(139, 92, 246, 0.00)');

        lineChartInstance = new Chart(lineCtx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Projected Views',
                        data: views,
                        borderColor: '#8b5cf6',
                        backgroundColor: purpleGradient,
                        fill: true,
                        tension: 0.4,
                        borderWidth: 2,
                        pointRadius: 0
                    },
                    {
                        label: 'Projected Likes',
                        data: likes,
                        borderColor: '#06b6d4',
                        borderWidth: 1.5,
                        fill: false,
                        tension: 0.4,
                        pointRadius: 0
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: '#64748b', font: { size: 10 } }
                    },
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.03)' },
                        ticks: { color: '#64748b', font: { size: 10 } }
                    }
                }
            }
        });

        // Reach bar chart
        const barCtx = document.getElementById('platformReachBarChart').getContext('2d');
        const platforms = viralityData.platform_performance.map(p => p.platform);
        const reachValues = viralityData.platform_performance.map(p => p.expected_reach);

        barChartInstance = new Chart(barCtx, {
            type: 'bar',
            data: {
                labels: platforms,
                datasets: [{
                    data: reachValues,
                    backgroundColor: ['#e1306c', '#00f5d4', '#ff007f', '#0a66c2'],
                    borderWidth: 0,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: '#64748b', font: { size: 10 } }
                    },
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.03)' },
                        ticks: { color: '#64748b', font: { size: 10 } }
                    }
                }
            }
        });
    }

    // Initialize Router
    handleRouting();

    // Load Demo Data Immediately
    generatedData = demoData;
    generatedIdeasPayload = {
        trends: demoData.trends,
        top_trend: demoData.top_trend,
        ideas: demoData.ideas
    };
    populateStage1Outputs(demoData);
    populateStage2Outputs(demoData);
    
    // Select the second card visually in Content Studio on load
    setTimeout(() => {
        const cards = document.querySelectorAll('.idea-card-item');
        if (cards && cards[1]) cards[1].classList.add('selected');
    }, 1200);

});
