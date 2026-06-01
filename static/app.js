/* --------------------------------------------------------------------------
   Ratefluencer AI - Core Frontend Logic (Multi-Page SaaS Router & Wizard)
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

    // Chart instances
    let gaugeChartInstance = null;
    let lineChartInstance = null;
    let barChartInstance = null;

    // Generated data store
    let generatedData = null;

    // Premium Demo Data (Loaded on startup to ensure hackathon judges see a full app instantly)
    const demoData = {
        niche: "AI & Autonomous Agents",
        top_trend: {
            title: "Agentic Workflows are replacing standard chat interfaces in SaaS",
            source: "TechCrunch",
            upvotes: 1840,
            num_comments: 310,
            score: 94.6,
            growth_velocity: 88.5,
            novelty: 92.0,
            engagement_potential: 89.2,
            audience_relevance: 96.0
        },
        trends: [
            {
                title: "Agentic Workflows are replacing standard chat interfaces in SaaS",
                source: "TechCrunch",
                upvotes: 1840,
                num_comments: 310,
                score: 94.6,
                growth_velocity: 88.5,
                novelty: 92.0,
                engagement_potential: 89.2,
                audience_relevance: 96.0
            },
            {
                title: "New open source models outperform proprietary giants on local hardware",
                source: "r/MachineLearning",
                upvotes: 2150,
                num_comments: 420,
                score: 89.8,
                growth_velocity: 82.1,
                novelty: 87.5,
                engagement_potential: 94.0,
                audience_relevance: 85.0
            },
            {
                title: "How developers are building entire SaaS projects in 10 minutes with AI tools",
                source: "r/startups",
                upvotes: 1100,
                num_comments: 195,
                score: 84.2,
                growth_velocity: 78.4,
                novelty: 75.0,
                engagement_potential: 82.0,
                audience_relevance: 91.5
            },
            {
                title: "Apple launches local agentic Siri framework on next-gen devices",
                source: "The Verge",
                upvotes: 1620,
                num_comments: 280,
                score: 81.5,
                growth_velocity: 72.0,
                novelty: 80.0,
                engagement_potential: 78.5,
                audience_relevance: 88.0
            },
            {
                title: "SaaS seed funding pivots entirely towards agentic infrastructure startups",
                source: "TechCrunch",
                upvotes: 950,
                num_comments: 80,
                score: 79.1,
                growth_velocity: 64.2,
                novelty: 85.0,
                engagement_potential: 62.0,
                audience_relevance: 75.0
            },
            {
                title: "Developers report high burnout as coding LLMs change team speed expectations",
                source: "r/technology",
                upvotes: 1350,
                num_comments: 340,
                score: 76.4,
                growth_velocity: 68.0,
                novelty: 65.0,
                engagement_potential: 84.5,
                audience_relevance: 82.0
            },
            {
                title: "Vector database workloads hit record spikes across cloud service engines",
                source: "Wired",
                upvotes: 680,
                num_comments: 52,
                score: 71.0,
                growth_velocity: 55.4,
                novelty: 72.0,
                engagement_potential: 48.0,
                audience_relevance: 62.0
            },
            {
                title: "Hackers leverage multi-agent frameworks to automate database testing",
                source: "r/technology",
                upvotes: 1050,
                num_comments: 160,
                score: 68.5,
                growth_velocity: 58.0,
                novelty: 76.0,
                engagement_potential: 65.0,
                audience_relevance: 55.0
            },
            {
                title: "How to properly audit agent loops to prevent recursive API bills",
                source: "r/startups",
                upvotes: 520,
                num_comments: 95,
                score: 65.0,
                growth_velocity: 45.0,
                novelty: 68.0,
                engagement_potential: 54.0,
                audience_relevance: 79.0
            },
            {
                title: "UX researchers argue that text prompts are a temporary step in AI evolution",
                source: "Twitter",
                upvotes: 890,
                num_comments: 110,
                score: 58.2,
                growth_velocity: 49.0,
                novelty: 74.0,
                engagement_potential: 50.0,
                audience_relevance: 68.0
            }
        ],
        script: {
            hook: "Stop building chat interfaces! The future of software is completely agentic.",
            story: "We are officially moving from text chatbots to autonomous agents that execute tasks. Developers are now using loops to construct full SaaS projects in under 10 minutes.",
            insights: [
                "Agentic workflows automate complex multi-step reasoning models.",
                "It reduces deployment cycles from weeks to simple execution loops.",
                "SaaS companies adopting loop nodes are cutting operation bills by 60%."
            ],
            cta: "Comment 'AGENT' and I'll send the source!"
        },
        linkedin: {
            post: "The conversational AI era is ending. The agentic loops are taking over. 🤖\n\nFor the past two years, we've focused on text chatbots. Now, developers are deploying autonomous agent pipelines that write code, debug databases, and deploy SaaS apps in under 10 minutes.\n\nHere are the 3 major impacts:\n1️⃣ Prompting is fading: Task executors will replace basic chat input boxes.\n2️⃣ Solo operators can scale: Loop systems allow single devs to operate like a 10-person team.\n3️⃣ Operational costs are falling: Task automation reduces execution times by 3x.\n\nAre you building chat panels, or are you deploying agentic workflows?",
            hashtags: "#ArtificialIntelligence #SaaS #FutureOfWork #ProductManagement",
            engagement_hook: "How is your engineering team adapting to autonomous agent nodes? Let's discuss below!"
        },
        instagram: {
            caption: "Chatbots are officially legacy tech. ⚡ Agentic workflows are replacing simple text interfaces, enabling systems to execute full development pipelines in minutes. Check out the blueprint below to see how to adapt your workflow! 👇",
            hashtags: "#aiagents #agenticai #techtrends #startupfounder #softwaredev #futureofcoding",
            cta: "Link in bio to read the full loop framework! 📌"
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
        
        // Remove active class from all links and hide all sections
        navItems.forEach(item => item.classList.remove('active'));
        viewSections.forEach(section => section.classList.add('hide'));
        
        // Find matching view container and show it
        const targetViewId = `${hash.slice(1)}-view`;
        const targetSection = document.getElementById(targetViewId);
        const targetNavLink = document.getElementById(`nav-${hash.slice(1)}`);
        
        if (targetSection && targetNavLink) {
            targetSection.classList.remove('hide');
            targetNavLink.classList.add('active');
            window.scrollTo(0, 0);
        } else {
            // Fallback to Dashboard
            document.getElementById('dashboard-view').classList.remove('hide');
            document.getElementById('nav-dashboard').classList.add('active');
        }

        // Close drawer if route changes
        closeDrawer();
    }

    // Bind events
    window.addEventListener('hashchange', handleRouting);
    
    // Quick tags filling input
    quickTags.forEach(tag => {
        tag.addEventListener('click', () => {
            nicheInput.value = tag.getAttribute('data-topic');
            nicheInput.focus();
        });
    });

    // ==========================================
    // 2. WORKFLOW WIZARD CONTROLLER
    // ==========================================
    generateBtn.addEventListener('click', () => {
        const topic = nicheInput.value.trim() || "Technology";
        runWizardPipeline(topic);
    });

    nicheInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const topic = nicheInput.value.trim() || "Technology";
            runWizardPipeline(topic);
        }
    });

    function runWizardPipeline(niche) {
        // Reset and display wizard overlay
        wizardModal.classList.remove('hide');
        wizardProgressBar.style.width = '0%';
        resetWizardSteps();
        
        // Trigger fetch API
        const apiPromise = fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ topic: niche })
        }).then(res => {
            if (!res.ok) throw new Error("API call failed");
            return res.json();
        });

        executeStepAnimationChain(apiPromise);
    }

    function resetWizardSteps() {
        for (let i = 1; i <= 6; i++) {
            const node = document.getElementById(`wstep-${i}`);
            node.classList.remove('active', 'done');
            node.querySelector('.spinner-mini').classList.add('hide');
            node.querySelector('.check-icon').classList.add('hide');
        }
        // Step 1 active first
        const step1 = document.getElementById('wstep-1');
        step1.classList.add('active');
        step1.querySelector('.spinner-mini').classList.remove('hide');
    }

    async function executeStepAnimationChain(apiPromise) {
        const stepTimings = [1000, 1200, 1200, 800, 800, 1000];
        const statusPhrases = [
            "Registering niche topic parameters...",
            "Crawling RSS feeds and subreddits...",
            "Scoring harvested trends using RandomForest...",
            "Writing short-form video scripts via Gemini...",
            "Drafting LinkedIn post and Instagram caption copywriting...",
            "Predicting final virality index using XGBoost..."
        ];

        for (let i = 1; i <= 6; i++) {
            wizardGlobalStatus.innerText = statusPhrases[i-1];
            
            // Wait for step timer
            await new Promise(resolve => setTimeout(resolve, stepTimings[i-1]));
            
            // Mark step i as done
            const currentStep = document.getElementById(`wstep-${i}`);
            currentStep.classList.remove('active');
            currentStep.classList.add('done');
            currentStep.querySelector('.spinner-mini').classList.add('hide');
            currentStep.querySelector('.check-icon').classList.remove('hide');
            
            // Update progress bar
            wizardProgressBar.style.width = `${Math.round((i / 6) * 100)}%`;
            
            // Set next step active
            if (i < 6) {
                const nextStep = document.getElementById(`wstep-${i+1}`);
                nextStep.classList.add('active');
                nextStep.querySelector('.spinner-mini').classList.remove('hide');
            }
        }

        try {
            const data = await apiPromise;
            generatedData = data;
            
            // Populate all data fields
            populateWorkspace(data);
            
            // Transition out wizard
            setTimeout(() => {
                wizardModal.classList.add('hide');
                showToast("SaaS Blueprint generated! Explore Trends, Content Studio & Analytics.");
            }, 500);

        } catch (err) {
            console.error(err);
            wizardModal.classList.add('hide');
            alert("Generation failed. Check that the FastAPI server is running.");
        }
    }

    // ==========================================
    // 3. WORKSPACE POPULATION ENGINE
    // ==========================================
    function populateWorkspace(data) {
        // Update Dashboard Stat Cards
        document.getElementById('stat-total-trends').innerText = data.trends.length;
        
        // Average trend score
        const avgTrendScore = (data.trends.reduce((sum, item) => sum + item.score, 0) / data.trends.length).toFixed(1);
        document.getElementById('stat-avg-trend-score').innerText = `${avgTrendScore}`;
        
        // Virality score
        const viralityVal = Math.round(data.virality.virality_score);
        document.getElementById('stat-avg-virality-score').innerText = `${viralityVal}%`;
        document.getElementById('stat-content-count').innerText = "3 Assets";

        // Update Trends Grid
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
            
            // Add click details handler
            card.addEventListener('click', () => {
                openSidePanel(item);
            });
            
            trendsCardsContainer.appendChild(card);
        });
        
        // Update Content Studio inputs
        // Tab 1: Reel
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

        // Update Analytics elements
        document.getElementById('virality-percentage').innerText = `${viralityVal}%`;
        document.getElementById('metric-views').innerText = formatCounter(data.virality.expected_views);
        document.getElementById('metric-likes').innerText = formatCounter(data.virality.expected_likes);
        document.getElementById('metric-shares').innerText = formatCounter(data.virality.expected_shares);
        document.getElementById('metric-saves').innerText = formatCounter(data.virality.expected_saves);
        
        const verdictLbl = document.getElementById('status-verdict');
        const verdictDot = verdictLbl.previousElementSibling;
        
        if (viralityVal >= 80) {
            verdictLbl.innerText = "Highly Viral Potential";
            verdictLbl.style.color = "#10b981";
            verdictDot.style.backgroundColor = "#10b981";
        } else if (viralityVal >= 60) {
            verdictLbl.innerText = "Moderate Viral Potential";
            verdictLbl.style.color = "#f59e0b";
            verdictDot.style.backgroundColor = "#f59e0b";
        } else {
            verdictLbl.innerText = "Low Viral Potential";
            verdictLbl.style.color = "#ec4899";
            verdictDot.style.backgroundColor = "#ec4899";
        }

        // Render Charts
        renderCharts(data.virality);

        // Refresh icons
        lucide.createIcons();
    }

    // Helper views formatter
    function formatCounter(num) {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        }
        if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
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
                            <div class="drawer-metric-bar-fill bar-purple" style="width: ${trend.growth_velocity}%; background-color: var(--purple);"></div>
                        </div>
                        <span class="drawer-metric-val">${trend.growth_velocity}%</span>
                    </div>
                </div>

                <div class="drawer-metric-card">
                    <span class="drawer-metric-lbl">Novelty index</span>
                    <div class="drawer-metric-right">
                        <div class="drawer-metric-bar">
                            <div class="drawer-metric-bar-fill bar-blue" style="width: ${trend.novelty}%; background-color: var(--blue);"></div>
                        </div>
                        <span class="drawer-metric-val">${trend.novelty}%</span>
                    </div>
                </div>

                <div class="drawer-metric-card">
                    <span class="drawer-metric-lbl">Engagement Potential</span>
                    <div class="drawer-metric-right">
                        <div class="drawer-metric-bar">
                            <div class="drawer-metric-bar-fill bar-cyan" style="style: width: ${trend.engagement_potential}%; background-color: var(--cyan);"></div>
                        </div>
                        <span class="drawer-metric-val">${trend.engagement_potential}%</span>
                    </div>
                </div>

                <div class="drawer-metric-card">
                    <span class="drawer-metric-lbl">Audience Relevance</span>
                    <div class="drawer-metric-right">
                        <div class="drawer-metric-bar">
                            <div class="drawer-metric-bar-fill bar-pink" style="width: ${trend.audience_relevance}%; background-color: var(--pink);"></div>
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
        
        if (activeTab === 'tab-reel') {
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

    // Studio regenerate blueprint
    regenStudioBtn.addEventListener('click', () => {
        if (!generatedData) return;
        runWizardPipeline(generatedData.niche);
    });

    // Studio report export (.md)
    exportStudioBtn.addEventListener('click', () => {
        if (!generatedData) return;

        const dateStr = new Date().toLocaleDateString('en-US', {
            year: 'numeric', month: 'long', day: 'numeric'
        });

        const report = `# Ratefluencer AI - Campaign Content blueprint
Generated: ${dateStr}
Topic / Niche: **${generatedData.niche}**

---

## 1. Top Content Script (Vertical Reels)
- **Hook**: "${generatedData.script.hook}"
- **Story Body**: "${generatedData.script.story}"
- **Key Takeaways**:
${generatedData.script.insights.map((ins, i) => `  ${i+1}. ${ins}`).join('\n')}
- **CTA**: "${generatedData.script.cta}"

---

## 2. LinkedIn Post
\`\`\`text
${generatedData.linkedin.post}

${generatedData.linkedin.hashtags}
${generatedData.linkedin.engagement_hook}
\`\`\`

---

## 3. Instagram Caption
\`\`\`text
${generatedData.instagram.caption}

${generatedData.instagram.hashtags}
${generatedData.instagram.cta}
\`\`\`

---

## 4. Virality Prediction Overview
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
        link.setAttribute('download', `ratefluencer_campaign_${generatedData.niche.toLowerCase().replace(/[^a-z0-9]+/g, '_')}.md`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        showToast("Report download initialized!");
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

        // 6a. Virality Score gauge donut
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

        // 6b. Line Chart for projected engagement
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

        // 6c. Horizontal Bar Chart for Platform performance reach
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

    // Load Demo Data Immediately (Prevents empty pages, ensuring premium layout on load)
    generatedData = demoData;
    populateWorkspace(demoData);

});
