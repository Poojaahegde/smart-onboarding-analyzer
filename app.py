import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from analyzer import OnboardingAnalyzer
from simulator import ImpactSimulator
from ice_scorer import ICEScorer

st.set_page_config(
      page_title="Smart Onboarding Analyzer",
      page_icon="🚀",
      layout="wide"
)

st.title("🚀 Smart Onboarding Analyzer")
st.markdown("**LLM-Powered Activation Funnel Intelligence** — Diagnose drop-offs, get AI fix recommendations, simulate ARR impact.")
st.markdown("---")

# Sidebar configuration
st.sidebar.header("⚙️ Configuration")
monthly_signups = st.sidebar.number_input("Monthly New Signups", value=10000, step=500)
avg_ltv = st.sidebar.number_input("Average LTV per Activated User ($)", value=50, step=5)
use_llm = st.sidebar.checkbox("Use LLM Mode (requires OPENAI_API_KEY)", value=False)

st.sidebar.markdown("---")
st.sidebar.markdown("**Mode:** " + ("🤖 LLM" if use_llm else "📐 Rule-Based (Demo)"))

# Default funnel template
DEFAULT_STEPS = [
      {"step": "Landing Page Visit", "users": 10000},
      {"step": "Start Signup", "users": 6200},
      {"step": "Email Verification", "users": 4960},
      {"step": "Profile Setup", "users": 3224},
      {"step": "Connect Integration", "users": 1612},
      {"step": "Invite Team Member", "users": 1370},
      {"step": "Complete First Action", "users": 1096},
]

st.header("📥 Funnel Data Input")
use_default = st.checkbox("Use default 7-step SaaS onboarding template", value=True)

if use_default:
      funnel_df = pd.DataFrame(DEFAULT_STEPS)
else:
      st.info("Enter your funnel steps and user counts below.")
      funnel_input = []
      num_steps = st.number_input("Number of funnel steps", min_value=3, max_value=12, value=5)
      for i in range(num_steps):
                col1, col2 = st.columns(2)
                with col1:
                              step_name = st.text_input(f"Step {i+1} name", value=f"Step {i+1}", key=f"step_{i}")
                          with col2:
                    users = st.number_input(f"Users at Step {i+1}", min_value=1, value=max(100, 10000 - i*1500), key=f"users_{i}")
                                    funnel_input.append({"step": step_name, "users": users})
                                funnel_df = pd.DataFrame(funnel_input)

                            # Calculate conversions and drop-offs
                            funnel_df["conversion_rate"] = funnel_df["users"] / funnel_df["users"].iloc[0] * 100
                            funnel_df["step_conversion"] = funnel_df["users"].pct_change().fillna(0) * 100 + 100
                            funnel_df["dropoff_rate"] = 100 - funnel_df["step_conversion"].clip(upper=100)
                            funnel_df.loc[0, "dropoff_rate"] = 0

                            st.markdown("---")
                            st.header("📊 Funnel Visualization")

                            col1, col2 = st.columns(2)

                            with col1:
                                # Funnel chart
                                  fig_funnel = go.Figure(go.Funnel(
                                            y=funnel_df["step"],
                                            x=funnel_df["users"],
                                            textinfo="value+percent initial",
                                            marker=dict(color=px.colors.sequential.Blues_r[:len(funnel_df)])
                                  ))
                                  fig_funnel.update_layout(title="Onboarding Funnel", height=400)
                                  st.plotly_chart(fig_funnel, use_container_width=True)

                            with col2:
                                # Drop-off bar chart
                                  dropoff_data = funnel_df[funnel_df["dropoff_rate"] > 0].copy()
                                  colors = ["red" if r > 30 else "orange" if r > 15 else "steelblue" for r in dropoff_data["dropoff_rate"]]
                                  fig_drop = go.Figure(go.Bar(
                                      x=dropoff_data["step"],
                                      y=dropoff_data["dropoff_rate"],
                                      marker_color=colors,
                                      text=[f"{r:.1f}%" for r in dropoff_data["dropoff_rate"]],
                                      textposition="outside"
                                  ))
                                  fig_drop.update_layout(title="Drop-off Rate by Step (%)", height=400, yaxis_title="Drop-off %")
                                  st.plotly_chart(fig_drop, use_container_width=True)

                            # Key metrics
                            activation_rate = funnel_df["users"].iloc[-1] / funnel_df["users"].iloc[0] * 100
                            biggest_drop_idx = funnel_df["dropoff_rate"].idxmax()
                            biggest_drop_step = funnel_df.loc[biggest_drop_idx, "step"]
                            biggest_drop_rate = funnel_df.loc[biggest_drop_idx, "dropoff_rate"]

                            m1, m2, m3, m4 = st.columns(4)
                            m1.metric("Overall Activation Rate", f"{activation_rate:.1f}%", delta=None)
                            m2.metric("Users Activated / Month", f"{int(funnel_df['users'].iloc[-1] * monthly_signups / funnel_df['users'].iloc[0]):,}")
                            m3.metric("Biggest Drop-off Step", biggest_drop_step, delta=f"-{biggest_drop_rate:.0f}%")
                            m4.metric("Monthly Revenue at Risk", f"${int(funnel_df['users'].iloc[0] * monthly_signups / funnel_df['users'].iloc[0] * (1 - activation_rate/100) * avg_ltv):,}")

                            st.markdown("---")
                            st.header("🧠 AI Diagnosis")

                            analyzer = OnboardingAnalyzer(use_llm=use_llm)

                            if st.button("🔍 Run Diagnosis", type="primary"):
                                  with st.spinner("Analyzing funnel drop-offs..."):
                                            diagnoses = analyzer.diagnose(funnel_df)

                                  st.subheader("Drop-off Diagnosis by Step")
                                  for diagnosis in diagnoses:
                                            if diagnosis["dropoff_rate"] > 5:
                                                          severity = "🚨" if diagnosis["dropoff_rate"] > 30 else "⚠️" if diagnosis["dropoff_rate"] > 15 else "ℹ️"
                                                          with st.expander(f"{severity} **{diagnosis['step']}** — {diagnosis['dropoff_rate']:.1f}% drop-off | Root cause: {diagnosis['category']}"):
                                                                            st.markdown(f"**Diagnosis:** {diagnosis['diagnosis']}")
                                                                            st.markdown(f"**Primary Recommendation:** {diagnosis['recommendation']}")
                                                                            st.markdown(f"**Alternative:** {diagnosis['alternative']}")

                                                  # ICE scoring
                                                  st.markdown("---")
                                        st.subheader("🎯 ICE-Prioritized Fix List")
                                  scorer = ICEScorer()
                                  ice_results = scorer.score(diagnoses)
                                  ice_df = pd.DataFrame(ice_results)
                                  if not ice_df.empty:
                                            st.dataframe(ice_df[["priority", "step", "fix", "impact", "confidence", "ease", "ice_score"]].rename(columns={
                                                          "priority": "Priority", "step": "Step", "fix": "Recommended Fix",
                                                          "impact": "Impact (1-10)", "confidence": "Confidence (1-10)",
                                                          "ease": "Ease (1-10)", "ice_score": "ICE Score"
                                            }), use_container_width=True)

                                  # Impact simulation
                                  st.markdown("---")
                                  st.subheader("💰 Revenue Impact Simulation")
                                  simulator = ImpactSimulator(monthly_signups=monthly_signups, avg_ltv=avg_ltv)
                                  sim_results = simulator.simulate(funnel_df, diagnoses[:3])  # Top 3 fixes

    col1, col2, col3 = st.columns(3)
    col1.metric("Conservative Impact", f"+{sim_results['conservative_arr']:,.0f} ARR/yr", delta=f"+{sim_results['conservative_activation']:.1f}% activation")
    col2.metric("Realistic Impact", f"+{sim_results['realistic_arr']:,.0f} ARR/yr", delta=f"+{sim_results['realistic_activation']:.1f}% activation")
    col3.metric("Optimistic Impact", f"+{sim_results['optimistic_arr']:,.0f} ARR/yr", delta=f"+{sim_results['optimistic_activation']:.1f}% activation")

    # Waterfall chart
    fig_waterfall = go.Figure(go.Waterfall(
              name="Activation Improvement",
              orientation="v",
              measure=["absolute"] + ["relative"] * len(diagnoses[:3]) + ["total"],
              x=["Baseline"] + [d["step"][:20] for d in diagnoses[:3]] + ["Projected"],
              y=[activation_rate] + [d["expected_improvement"] for d in diagnoses[:3]] + [0],
              connector={"line": {"color": "rgb(63, 63, 63)"}},
              increasing={"marker": {"color": "green"}},
              decreasing={"marker": {"color": "red"}},
              totals={"marker": {"color": "blue"}}
    ))
    fig_waterfall.update_layout(title="Activation Rate Improvement by Fix", yaxis_title="Activation Rate (%)", height=350)
    st.plotly_chart(fig_waterfall, use_container_width=True)

else:
    st.info("👆 Click **Run Diagnosis** to analyze your funnel and get AI-powered recommendations.")

st.markdown("---")
st.caption("Smart Onboarding Analyzer | Built for AI PM portfolio | [GitHub](https://github.com/Poojaahegde/smart-onboarding-analyzer)")
