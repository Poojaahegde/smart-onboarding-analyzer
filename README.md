# Smart Onboarding Analyzer 🚀 — LLM-Powered Activation Funnel Intelligence

Stop losing users in your onboarding funnel. Get AI-generated diagnosis of every drop-off step — with prioritized fix recommendations in seconds.

## 🚀 Product Overview

### The Problem
Onboarding is the highest-leverage moment in the user lifecycle — and the most commonly botched. The average SaaS product loses **60–70% of new users in the first week**, mostly during onboarding. PMs know *that* users drop off; they rarely know *why* at each specific step, and they have no system to generate fix hypotheses at scale.

### The Solution
Smart Onboarding Analyzer takes your funnel step data (step names + conversion rates), applies an LLM-powered reasoning engine to diagnose the root cause of each drop-off, generates prioritized recommendations, and simulates the revenue impact of fixing each step — all in an interactive Streamlit dashboard.

### The Impact
- 🔍 **Diagnoses drop-off root causes** at every funnel step automatically
- - 🤖 **Generates LLM-style fix recommendations** per step (friction, cognitive load, value gap, trust gap)
  - - 📊 **Simulates activation improvement scenarios** — "if we fix step 3, activation improves by +8.2%"
    - - 💰 **Quantifies revenue impact** — connects activation improvement to ARR
      - - 🎯 **Prioritizes fixes** by expected impact × implementation effort
       
        - ---

        ## 🎯 Why This Matters (Product Perspective)

        Onboarding optimization is consistently one of the **highest-ROI product investments** a PM can make. A 10% improvement in activation rate typically drives 10–15% improvement in 30-day retention, which compounds into significant LTV gains.

        This tool demonstrates that I don't just track activation metrics — I can diagnose *why* activation fails and generate structured, prioritized hypotheses for fixing it. The LLM layer is what makes it a product insight engine, not just a funnel chart.

        **The key insight:** Most PM tools show you *what* happened. This one tells you *why* it happened and *what to do next*.

        ---

        ## 🧠 AI/ML Explanation

        | Component | Technique | Why It Was Chosen |
        |---|---|---|
        | Drop-off Diagnosis | Rule-based + LLM prompt reasoning | Combines statistical patterns (big drops) with contextual reasoning (why this step, not just that it dropped) |
        | Recommendation Generation | Template-based LLM synthesis | Produces structured, actionable fixes — not vague suggestions |
        | Impact Simulation | Monte Carlo scenario modeling | Shows range of outcomes (optimistic/realistic/conservative) for each fix |
        | Fix Prioritization | ICE scoring (Impact × Confidence × Ease) | Standard PM prioritization framework — gives a defensible ranking |
        | Pattern Detection | Threshold-based anomaly detection | Flags steps where drop-off exceeds 2x the funnel average |

        **Diagnosis Categories (LLM classifies each drop-off into one):**
        - **Friction** — The step is technically hard or has too many fields
        - - **Cognitive Load** — Too much information or too many decisions at once
          - - **Value Gap** — User doesn't understand why they should complete this step
            - - **Trust Gap** — User isn't confident the product is worth their time/data
              - - **Motivation Drop** — User hit a wall between initial excitement and actual setup work
               
                - ---

                ## 🛠 Tech Stack

                | Layer | Technology |
                |---|---|
                | UI | Streamlit |
                | LLM Reasoning | OpenAI API (GPT-4) with rule-based fallback for demo |
                | Data Generation | NumPy, Pandas (synthetic funnel data) |
                | Visualization | Plotly (funnel charts, waterfall charts) |
                | Scenario Modeling | NumPy Monte Carlo simulation |
                | Language | Python 3.8+ |

                ---

                ## 📊 Sample Output

                **Input:** 7-step SaaS onboarding funnel

                | Step | Users | Conversion | Drop-off | Diagnosis |
                |---|---|---|---|---|
                | Landing page visit | 10,000 | — | — | — |
                | Start signup | 6,200 | 62.0% | 38.0% | — |
                | Email verification | 4,960 | 80.0% | 20.0% | Friction (email step adds latency) |
                | Profile setup | 3,224 | 65.0% | 35.0% | ⚠️ Cognitive Load (too many fields) |
                | Connect first integration | 1,612 | 50.0% | **50.0%** | 🚨 Value Gap (unclear why needed) |
                | Invite team member | 1,370 | 85.0% | 15.0% | — |
                | Complete first action | 1,096 | 80.0% | 20.0% | Friction (setup wizard unclear) |

                **LLM Diagnosis for Step "Connect first integration" (50% drop-off):**
                > *"This step has the highest drop-off in your funnel at 50%, which is 2.8x the funnel average. The likely root cause is a Value Gap: users don't understand why connecting an integration is required before they can experience the product's core value. This is a classic 'prerequisite before reward' problem. Recommendation: Add a value preview — show users a demo of what the product looks like after integration, then ask them to connect. Alternative: Make this step optional and let users experience the product first, with an in-app nudge to connect later."*
                >
                > **ICE-Prioritized Fix List:**
                > | Priority | Fix | Step | Impact | Confidence | Ease | ICE Score |
                > |---|---|---|---|---|---|---|
                > | 1 | Add integration value preview | Step 5 | 9 | 8 | 6 | 432 |
                > | 2 | Reduce profile form to 3 fields | Step 4 | 7 | 9 | 8 | 504 |
                > | 3 | Progressive email verification | Step 3 | 5 | 7 | 7 | 245 |
                >
                > **Simulated Impact:**
                > - Fix Steps 4 + 5: Activation rate improves from **11.0% → 18.4%** (+67% relative)
                > - - At 10,000 monthly signups × $50 LTV: **+$37,000/month projected ARR impact**
                >  
                >   - ---
                >
                > ## 📸 Demo Instructions
                >
                > ```bash
                > # 1. Clone the repo
                > git clone https://github.com/Poojaahegde/smart-onboarding-analyzer.git
                > cd smart-onboarding-analyzer
                >
                > # 2. Install dependencies
                > pip install -r requirements.txt
                >
                > # 3. (Optional) Set OpenAI API key for LLM mode
                > export OPENAI_API_KEY=sk-...
                >
                > # 4. Launch the app
                > streamlit run app.py
                > ```
                >
                > Open `http://localhost:8501` in your browser.
                >
                > **Two modes:**
                > - **Demo mode** (no API key): Uses rule-based diagnosis engine — full functionality, no API cost
                > - - **LLM mode** (with API key): Uses GPT-4 for richer, context-aware diagnosis and recommendations
                >  
                >   - **Inputs:**
                >   - - Funnel step names (comma-separated or use the default 7-step SaaS template)
                >     - - Users at each step (or use auto-generated synthetic data)
                >       - - Monthly new user volume (for ARR impact calculation)
                >         - - Average LTV per activated user
                >          
                >           - ---
                >
                > ## 🎯 Product Thinking Layer
                >
                > ### 👥 Target Users
                > - **Product Managers** at SaaS companies with new-user drop-off problems in the first 7 days
                > - - **Growth PMs** running activation optimization sprints
                >   - - **Startup founders** doing early-stage onboarding analysis before they have a data team
                >    
                >     - ### 😣 Pain Points Solved
                >     - - **"We know people drop off at step 3, but we don't know why"** — LLM diagnosis provides the *why*, not just the *what*
                >       - - **Analysis paralysis** — Multiple drop-off steps with no prioritization framework; ICE scoring resolves this
                >         - - **No impact estimation** — PMs can't justify engineering time without a revenue impact estimate; simulation provides this
                >           - - **Waiting for data science** — Small teams can't get custom funnel analysis without queuing a data request; this tool is self-serve
                >            
                >             - ### 🧩 Key Product Decisions Made
                >            
                >             - **Rule-based fallback (no API required for demo):** LLM calls cost money and require keys — a PM portfolio tool that breaks without an API key has zero audience reach. The rule-based engine provides 80% of the value for 0% of the cost in demo mode.
                >            
                >             - **ICE scoring over RICE:** RICE requires a "Reach" estimate that's hard to calculate without data. ICE (Impact × Confidence × Ease) is self-contained and works with PM intuition — more usable without a data team.
                > 
                **Plotly over Matplotlib:** Funnel visualization needs interactivity (hover tooltips, zoom). Plotly gives this for free; Matplotlib would require custom JS.

                **Monte Carlo simulation (not point estimates):** Showing "activation will improve by exactly 7.3%" is false precision. Monte Carlo shows a range (5.1%–9.8%) that reflects real uncertainty — more honest and more defensible to executives.

                ### 🗺 Future Roadmap

                | Priority | Feature | Expected Impact |
                |---|---|---|
                | P0 | Connect to real funnel data via CSV upload | Transform demo into production-ready tool |
                | P0 | Session recording integration signals (Hotjar, FullStory) | Add behavioral evidence to LLM diagnosis |
                | P1 | A/B test generator — auto-generate test variants for each fix | Close the loop: diagnosis → experiment |
                | P1 | Cohort comparison — compare onboarding funnel by signup week | Detect whether onboarding is improving or regressing |
                | P2 | Amplitude / Mixpanel API integration | Live funnel data without CSV export |
                | P2 | Slack alert: "Activation dropped 8% this week vs. last" | Proactive PM monitoring |
                | P3 | Multi-product funnel comparison | Benchmark onboarding across product lines |

                ---

                ## 📁 Project Structure

                ```
                smart-onboarding-analyzer/
                ├── app.py                  # Main Streamlit dashboard
                ├── analyzer.py             # Core diagnosis engine (rule-based + LLM)
                ├── simulator.py            # Monte Carlo impact simulation
                ├── ice_scorer.py           # ICE prioritization engine
                ├── requirements.txt        # Python dependencies
                └── README.md               # This file
                ```

                ---

                ## 🔗 Related Projects in This Portfolio
                - [A/B Test Analyzer](https://github.com/Poojaahegde/ab-test-analyzer) — Statistical significance calculator for PM experiments
                - - [Churn Prediction Dashboard](https://github.com/Poojaahegde/churn-prediction-dashboard) — ML-powered user retention intelligence
                  - - [Product Metrics Dashboard](https://github.com/Poojaahegde/product-metrics-dashboard) — DAU, retention & conversion tracker
                   
                    - ---

                    *Built as part of an AI PM portfolio — demonstrating that activation optimization requires both data diagnosis and AI-powered insight generation, not just funnel charts.*
