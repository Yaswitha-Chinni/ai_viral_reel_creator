/* --------------------------------------------------------------------------
   Ratefluencer AI - Frontend Application Logic (Vanilla JS)
   Handles API Integration, Loading Experience, Charts, Clipboard & Report Export
   -------------------------------------------------------------------------- */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize Lucide Icons
    lucide.createIcons();

    // DOM Elements
    const nicheInput = document.getElementById('niche-input');
    const generateBtn = document.getElementById('generate-button');
    const quickTags = document.querySelectorAll('.tag-btn');
    
    const loadingConsole = document.getElementById('loading-console');
    const mainDashboard = document.getElementById('main-dashboard');
    
    // Action Buttons
    const copyReelBtn = document.getElementById('copy-reel-btn');
    const copyLinkedinBtn = document.getElementById('copy-linkedin-btn');
    const copyInstagramBtn = document.getElementById('copy-instagram-btn');
    const regenerateReelBtn = document.getElementById('regenerate-reel-btn');
    const exportReportBtn = document.getElementById('export-report-button');
    const exportToast = document.getElementById('export-toast');

    // Chart instances
    let gaugeChartInstance = null;
    let lineChartInstance = null;
    let barChartInstance = null;

    // Generated state store
    let generatedData = null;

    // 1. Example tag click handler
    quickTags.forEach(tag => {
        tag.addEventListener('click', () => {
            const topic = tag.getAttribute('data-topic');
            nicheInput.value = topic;
            // Add focus styling
            nicheInput.focus();
        });
    });

    // 2. Main Generation trigger
    generateBtn.addEventListener('click', () => {
        const topicVal = nicheInput.value.trim();
        triggerPipeline(topicVal || "Technology");
    });

    nicheInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const topicVal = nicheInput.value.trim();
            triggerPipeline(topicVal || "Technology");
        }
    });

    // 3. Pipeline execution manager
    function triggerPipeline(niche) {
        // Toggle view visibility
        mainDashboard.classList.add('hide');
        loadingConsole.classList.remove('hide');
        
        // Reset loading step indicator classes
        resetLoadingConsole();
        
        // Fetch API request in background
        const apiPromise = fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ topic: niche })
        }).then(res => {
            if (!res.ok) throw new Error('API Request Failed');
            return res.json();
        });

        // Run sequential loading animations (simulating agent nodes executing)
        runAgentStepLoadingSequence(apiPromise);
    }

    // Reset loading indicators
    function resetLoadingConsole() {
        for (let i = 1; i <= 6; i++) {
            const stepCard = document.getElementById(`step-loading-${i}`);
            const spinner = stepCard.querySelector('.spinner-mini');
            const checkIcon = stepCard.querySelector('.check-icon');
            
            stepCard.classList.remove('active', 'done');
            spinner.classList.add('hide');
            checkIcon.classList.add('hide');
        }
        
        // Start Node 1 active
        const card1 = document.getElementById('step-loading-1');
        card1.classList.add('active');
        card1.querySelector('.spinner-mini').classList.remove('hide');
    }

    // Step-by-step loading animation
    async function runAgentStepLoadingSequence(apiPromise) {
        const stepDurations = [1200, 1000, 1400, 800, 800, 1000];
        
        for (let i = 1; i <= 6; i++) {
            // Wait for step duration
            await new Promise(resolve => setTimeout(resolve, stepDurations[i-1]));
            
            // Mark step i as done
            const currentCard = document.getElementById(`step-loading-${i}`);
            currentCard.classList.remove('active');
            currentCard.classList.add('done');
            currentCard.querySelector('.spinner-mini').classList.add('hide');
            currentCard.querySelector('.check-icon').classList.remove('hide');
            
            // Set next step active
            if (i < 6) {
                const nextCard = document.getElementById(`step-loading-${i+1}`);
                nextCard.classList.add('active');
                nextCard.querySelector('.spinner-mini').classList.remove('hide');
            }
        }

        // Wait for both loading animations and API promise to finish
        try {
            const data = await apiPromise;
            generatedData = data;
            
            // Populate workspace widgets
            populateWorkspace(data);
            
            // Hide loader and display dashboard
            loadingConsole.classList.add('hide');
            mainDashboard.classList.remove('hide');
            
            // Trigger scroll to results
            mainDashboard.scrollIntoView({ behavior: 'smooth' });
        } catch (err) {
            console.error(err);
            alert("Error generating content. Please verify that the backend FastAPI app is running.");
            loadingConsole.classList.add('hide');
        }
    }

    // 4. Populator for workspace panels
    function populateWorkspace(data) {
        // Step 1: Trends Discovery Table
        const tbody = document.getElementById('trends-table-body').querySelector('tbody');
        tbody.innerHTML = '';
        
        data.trends.forEach((item, index) => {
            const tr = document.createElement('tr');
            if (index === 0) {
                tr.classList.add('trend-row-highlight');
            }
            
            tr.innerHTML = `
                <td>
                    <span class="trend-row-title">${item.title}</span>
                    ${index === 0 ? '<span class="trend-winner-tag">TOP SELECTION</span>' : ''}
                </td>
                <td><span class="trend-row-source">${item.source}</span></td>
                <td><span class="trend-row-growth">+${item.growth_velocity}%</span></td>
                <td><span class="trend-row-score">${item.score}/100</span></td>
            `;
            tbody.appendChild(tr);
        });

        // Step 2: Selected Trend Metrics
        const rankingContainer = document.getElementById('ranking-details-container');
        const topTrend = data.top_trend;
        
        rankingContainer.innerHTML = `
            <div class="ranking-metric-card">
                <span class="ranking-metric-lbl">Growth Velocity</span>
                <div class="ranking-metric-val-block">
                    <div class="ranking-metric-bar-outer">
                        <div class="ranking-metric-bar-inner bar-purple" style="width: ${topTrend.growth_velocity}%"></div>
                    </div>
                    <span class="ranking-metric-val">${topTrend.growth_velocity}%</span>
                </div>
            </div>
            <div class="ranking-metric-card">
                <span class="ranking-metric-lbl">Novelty index</span>
                <div class="ranking-metric-val-block">
                    <div class="ranking-metric-bar-outer">
                        <div class="ranking-metric-bar-inner bar-blue" style="width: ${topTrend.novelty}%"></div>
                    </div>
                    <span class="ranking-metric-val">${topTrend.novelty}%</span>
                </div>
            </div>
            <div class="ranking-metric-card">
                <span class="ranking-metric-lbl">Engagement Potential</span>
                <div class="ranking-metric-val-block">
                    <div class="ranking-metric-bar-outer">
                        <div class="ranking-metric-bar-inner bar-cyan" style="width: ${topTrend.engagement_potential}%"></div>
                    </div>
                    <span class="ranking-metric-val">${topTrend.engagement_potential}%</span>
                </div>
            </div>
            <div class="ranking-metric-card">
                <span class="ranking-metric-lbl">Audience Relevance</span>
                <div class="ranking-metric-val-block">
                    <div class="ranking-metric-bar-outer">
                        <div class="ranking-metric-bar-inner bar-pink" style="width: ${topTrend.audience_relevance}%"></div>
                    </div>
                    <span class="ranking-metric-val">${topTrend.audience_relevance}%</span>
                </div>
            </div>
            <div class="final-score-card">
                <span class="ranking-metric-lbl">Final Trend Score</span>
                <span class="final-score-val">${topTrend.score}/100</span>
            </div>
        `;

        // Step 3: Script Generator
        document.getElementById('script-hook').innerText = `"${data.script.hook}"`;
        document.getElementById('script-story').innerText = `"${data.script.story}"`;
        
        const insightsUl = document.getElementById('script-insights');
        insightsUl.innerHTML = '';
        data.script.insights.forEach(insight => {
            const li = document.createElement('li');
            li.innerText = insight;
            insightsUl.appendChild(li);
        });
        document.getElementById('script-cta').innerText = `"${data.script.cta}"`;

        // Step 4: LinkedIn Content
        document.getElementById('linkedin-post-body').innerText = data.linkedin.post;
        document.getElementById('linkedin-hashtags').innerText = data.linkedin.hashtags;
        document.getElementById('linkedin-engagement').innerText = `🎯 Engagement Hook: ${data.linkedin.engagement_hook}`;

        // Step 5: Instagram Content
        document.getElementById('instagram-caption-body').innerText = data.instagram.caption;
        document.getElementById('instagram-hashtags').innerText = data.instagram.hashtags;
        document.getElementById('instagram-cta').innerText = `📌 IG CTA: ${data.instagram.cta}`;

        // Step 6: Virality Analytics
        const viralityScore = Math.round(data.virality.virality_score);
        document.getElementById('virality-percentage').innerText = `${viralityScore}%`;
        
        // Expected metric counters
        document.getElementById('metric-views').innerText = formatCounter(data.virality.expected_views);
        document.getElementById('metric-likes').innerText = formatCounter(data.virality.expected_likes);
        document.getElementById('metric-shares').innerText = formatCounter(data.virality.expected_shares);
        document.getElementById('metric-saves').innerText = formatCounter(data.virality.expected_saves);
        
        const statusVerdict = document.getElementById('status-verdict');
        const statusDot = statusVerdict.previousElementSibling;
        
        if (viralityScore >= 80) {
            statusVerdict.innerText = "Highly Viral Potential";
            statusVerdict.style.color = "#10b981";
            statusDot.style.backgroundColor = "#10b981";
        } else if (viralityScore >= 60) {
            statusVerdict.innerText = "Moderate Viral Potential";
            statusVerdict.style.color = "#f59e0b";
            statusDot.style.backgroundColor = "#f59e0b";
        } else {
            statusVerdict.innerText = "Low Viral Potential";
            statusVerdict.style.color = "#ec4899";
            statusDot.style.backgroundColor = "#ec4899";
        }

        // Initialize and Update Charts
        renderCharts(data.virality);
    }

    // Helper: Number formatter
    function formatCounter(num) {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        }
        if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    }

    // 5. Chart.js Render Engine
    function renderCharts(viralityData) {
        // Destroy existing chart instances before rebuilding
        if (gaugeChartInstance) gaugeChartInstance.destroy();
        if (lineChartInstance) lineChartInstance.destroy();
        if (barChartInstance) barChartInstance.destroy();

        // 5a. Donut Gauge Chart
        const score = Math.round(viralityData.virality_score);
        const gaugeCtx = document.getElementById('viralityGaugeChart').getContext('2d');
        
        gaugeChartInstance = new Chart(gaugeCtx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [score, 100 - score],
                    backgroundColor: [
                        '#8b5cf6', // purple
                        'rgba(255, 255, 255, 0.05)' // dark transparent
                    ],
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

        // 5b. Hourly Engagement Line Chart
        const lineCtx = document.getElementById('engagementLineChart').getContext('2d');
        const hourlyLabels = viralityData.hourly_engagement.map(item => item.hour);
        const hourlyViews = viralityData.hourly_engagement.map(item => item.views);
        const hourlyLikes = viralityData.hourly_engagement.map(item => item.likes);

        const purpleGradient = lineCtx.createLinearGradient(0, 0, 0, 120);
        purpleGradient.addColorStop(0, 'rgba(139, 92, 246, 0.3)');
        purpleGradient.addColorStop(1, 'rgba(139, 92, 246, 0.0)');

        lineChartInstance = new Chart(lineCtx, {
            type: 'line',
            data: {
                labels: hourlyLabels,
                datasets: [
                    {
                        label: 'Projected Views',
                        data: hourlyViews,
                        borderColor: '#8b5cf6',
                        backgroundColor: purpleGradient,
                        fill: true,
                        tension: 0.4,
                        borderWidth: 2,
                        pointRadius: 0
                    },
                    {
                        label: 'Projected Likes',
                        data: hourlyLikes,
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

        // 5c. Cross Platform Reach Bar Chart
        const barCtx = document.getElementById('platformReachBarChart').getContext('2d');
        const platforms = viralityData.platform_performance.map(p => p.platform);
        const reachValues = viralityData.platform_performance.map(p => p.expected_reach);

        barChartInstance = new Chart(barCtx, {
            type: 'bar',
            data: {
                labels: platforms,
                datasets: [{
                    data: reachValues,
                    backgroundColor: [
                        '#e1306c', // IG Red
                        '#00f5d4', // TikTok cyan/neon
                        '#ff007f', // YT Red/pink
                        '#0a66c2'  // LinkedIn blue
                    ],
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

    // 6. Clipboard Copy Actions
    function setupCopyListener(button, getTextFunc) {
        button.addEventListener('click', () => {
            const textToCopy = getTextFunc();
            navigator.clipboard.writeText(textToCopy).then(() => {
                // Visual success feedback
                button.classList.add('copied');
                const prevInner = button.innerHTML;
                button.innerHTML = '<i data-lucide="check"></i>';
                lucide.createIcons();
                
                setTimeout(() => {
                    button.classList.remove('copied');
                    button.innerHTML = prevInner;
                    lucide.createIcons();
                }, 2000);
            });
        });
    }

    setupCopyListener(copyReelBtn, () => {
        if (!generatedData) return "";
        return `HOOK: ${generatedData.script.hook}\nSTORY: ${generatedData.script.story}\nINSIGHTS:\n- ${generatedData.script.insights.join('\n- ')}\nCTA: ${generatedData.script.cta}`;
    });

    setupCopyListener(copyLinkedinBtn, () => {
        if (!generatedData) return "";
        return `${generatedData.linkedin.post}\n\n${generatedData.linkedin.hashtags}`;
    });

    setupCopyListener(copyInstagramBtn, () => {
        if (!generatedData) return "";
        return `${generatedData.instagram.caption}\n\n${generatedData.instagram.hashtags}\n\n${generatedData.instagram.cta}`;
    });

    // 7. Regenerate content logic (triggers fetch for the same input topic)
    regenerateReelBtn.addEventListener('click', () => {
        if (!generatedData) return;
        triggerPipeline(generatedData.niche);
    });

    // 8. Markdown report generator & downloader
    exportReportBtn.addEventListener('click', () => {
        if (!generatedData) return;

        const dateStr = new Date().toLocaleDateString('en-US', {
            year: 'numeric', month: 'long', day: 'numeric'
        });

        // Formulate Markdown
        const reportContent = `# Ratefluencer AI – Content Blueprints & Virality Report
Generated on: ${dateStr}
Niche / Focus: **${generatedData.niche}**

---

## 1. Selected Trend Analysis
- **Selected Topic**: ${generatedData.top_trend.title}
- **Source**: ${generatedData.top_trend.source}
- **RandomForest Trend Score**: ${generatedData.top_trend.score}/100
- **Novelty Index**: ${generatedData.top_trend.novelty}%
- **Growth Velocity**: ${generatedData.top_trend.growth_velocity}%
- **Engagement Potential**: ${generatedData.top_trend.engagement_potential}%
- **Audience Relevance**: ${generatedData.top_trend.audience_relevance}%

---

## 2. Short-Form Video Script (Instagram Reels/TikTok/YouTube Shorts)
- **Hook**: "${generatedData.script.hook}"
- **Story Body**: "${generatedData.script.story}"
- **Insights/Bullets**:
  1. ${generatedData.script.insights[0] || ""}
  2. ${generatedData.script.insights[1] || ""}
  3. ${generatedData.script.insights[2] || ""}
- **Call to Action**: "${generatedData.script.cta}"

---

## 3. LinkedIn Native Post
\`\`\`text
${generatedData.linkedin.post}

${generatedData.linkedin.hashtags}
${generatedData.linkedin.engagement_hook}
\`\`\`

---

## 4. Instagram Feed Caption
\`\`\`text
${generatedData.instagram.caption}

${generatedData.instagram.hashtags}
${generatedData.instagram.cta}
\`\`\`

---

## 5. XGBoost Virality Forecast
- **Predicted Virality Score**: ${generatedData.virality.virality_score}%
- **Estimated Reach Profile**:
  - Expected Views: ${dataNumberFormat(generatedData.virality.expected_views)}
  - Expected Likes: ${dataNumberFormat(generatedData.virality.expected_likes)}
  - Expected Shares: ${dataNumberFormat(generatedData.virality.expected_shares)}
  - Expected Saves: ${dataNumberFormat(generatedData.virality.expected_saves)}

- **Platform Reach Forecast**:
${generatedData.virality.platform_performance.map(p => `  - ${p.platform}: ${dataNumberFormat(p.expected_reach)} expected views`).join('\n')}

---
Generated autonomously by Ratefluencer AI Engine.
`;

        // Create virtual download file
        const blob = new Blob([reportContent], { type: 'text/markdown;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        
        link.setAttribute('href', url);
        link.setAttribute('download', `ratefluencer_report_${generatedData.niche.toLowerCase().replace(/[^a-z0-9]+/g, '_')}.md`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        // Toast success message
        exportToast.classList.remove('hide');
        setTimeout(() => {
            exportToast.classList.add('hide');
        }, 3500);
    });

    function dataNumberFormat(num) {
        return num.toLocaleString();
    }

});
