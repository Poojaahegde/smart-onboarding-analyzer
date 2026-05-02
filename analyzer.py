"""
OnboardingAnalyzer: Diagnoses drop-off root causes at each funnel step.
Operates in two modes:
  - Rule-based (default/demo): Uses threshold patterns + templates
    - LLM mode: Uses OpenAI GPT-4 for richer contextual reasoning
    """

import os
import pandas as pd
import numpy as np

# Diagnosis categories and templates
DIAGNOSIS_TEMPLATES = {
      "friction": {
                "category": "Friction",
                "diagnosis_template": "This step requires technical effort or multiple inputs that create resistance. Users are willing in principle but blocked by the mechanics of the step.",
                "rec_template": "Simplify the step: reduce form fields to the minimum required, add autofill, or break into sub-steps. Run a usability test to identify the exact friction point.",
                "alt_template": "Add progress indicators and estimated time ('This takes 2 minutes') to reduce perceived effort.",
                "improvement_range": (4, 9),
      },
      "cognitive_load": {
                "category": "Cognitive Load",
                "diagnosis_template": "Users are overwhelmed by too much information, too many choices, or unclear instructions at this step. Decision fatigue causes abandonment.",
                "rec_template": "Reduce to one primary action per screen. Remove optional fields, use progressive disclosure, and add tooltips for complex terms.",
                "alt_template": "Add a 'skip for now' option and let users complete this step later via in-app nudges.",
                "improvement_range": (5, 10),
      },
      "value_gap": {
                "category": "Value Gap",
                "diagnosis_template": "Users don't understand WHY this step is necessary before they've experienced the product's core value. This is a classic 'prerequisite before reward' problem.",
                "rec_template": "Show a value preview BEFORE asking users to complete this step. Demo what the product looks like after this step is done. Make the benefit tangible.",
                "alt_template": "Make this step optional. Let users experience the core product first, then use an in-app nudge to complete setup.",
                "improvement_range": (6, 14),
      },
      "trust_gap": {
                "category": "Trust Gap",
                "diagnosis_template": "Users aren't confident the product is worth their time, data, or commitment at this step. This often occurs at permission requests, payment steps, or data-sharing requirements.",
                "rec_template": "Add social proof (testimonials, user counts, security badges) immediately before this step. Explain exactly what data is used for and how it's protected.",
                "alt_template": "Delay high-trust steps until users have experienced enough value to justify the commitment.",
                "improvement_range": (3, 8),
      },
      "motivation_drop": {
                "category": "Motivation Drop",
                "diagnosis_template": "Users hit a wall between their initial excitement and the actual setup work required. This is an energy problem, not a UX problem — the distance between 'wanting' and 'doing' is too large.",
                "rec_template": "Add a quick win BEFORE this step — a micro-success that re-energizes the user. Show a progress bar with completion percentage to make the end feel achievable.",
                "alt_template": "Restructure the onboarding to deliver core value earlier, so users are completing setup out of enthusiasm rather than obligation.",
                "improvement_range": (2, 7),
      },
}

def _classify_dropoff(step_name: str, dropoff_rate: float, avg_dropoff: float) -> str:
      """Rule-based classification of drop-off category based on step name and rate."""
      step_lower = step_name.lower()
      severity_ratio = dropoff_rate / max(avg_dropoff, 1)

    # Keyword-based classification
      if any(k in step_lower for k in ["integrat", "connect", "sync", "link", "import"]):
                return "value_gap"
elif any(k in step_lower for k in ["profile", "setup", "configure", "settings", "fill"]):
        return "cognitive_load" if dropoff_rate > 25 else "friction"
elif any(k in step_lower for k in ["verify", "confirm", "email", "phone", "code"]):
        return "friction"
elif any(k in step_lower for k in ["payment", "card", "billing", "subscribe", "plan"]):
        return "trust_gap"
elif any(k in step_lower for k in ["invite", "team", "share", "collaborate"]):
        return "motivation_drop" if severity_ratio < 1.5 else "value_gap"
elif severity_ratio > 2.0:
        return "value_gap"  # Unusually high drops often signal value gap
elif severity_ratio > 1.5:
        return "cognitive_load"
else:
        return "friction"


class OnboardingAnalyzer:
      def __init__(self, use_llm: bool = False):
                self.use_llm = use_llm
                self.openai_available = False
                if use_llm:
                              try:
                                                import openai
                                                self.client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
                                                self.openai_available = True
except Exception:
                self.openai_available = False

    def diagnose(self, funnel_df: pd.DataFrame) -> list:
              """Generate diagnoses for each funnel step with meaningful drop-off."""
              avg_dropoff = funnel_df["dropoff_rate"].mean()
              diagnoses = []

        for _, row in funnel_df.iterrows():
                      if row["dropoff_rate"] <= 0:
                                        continue

                      category_key = _classify_dropoff(row["step"], row["dropoff_rate"], avg_dropoff)
                      template = DIAGNOSIS_TEMPLATES[category_key]

            improvement = np.random.uniform(*template["improvement_range"])
            improvement = min(improvement, row["dropoff_rate"] * 0.6)  # Cap at 60% of current drop

            if self.use_llm and self.openai_available:
                              diagnosis_text, rec_text, alt_text = self._llm_diagnose(row, avg_dropoff)
else:
                  diagnosis_text = template["diagnosis_template"]
                  rec_text = template["rec_template"]
                  alt_text = template["alt_template"]

            diagnoses.append({
                              "step": row["step"],
                              "dropoff_rate": row["dropoff_rate"],
                              "category": template["category"],
                              "diagnosis": diagnosis_text,
                              "recommendation": rec_text,
                              "alternative": alt_text,
                              "expected_improvement": improvement,
                              "severity": "HIGH" if row["dropoff_rate"] > 30 else "MEDIUM" if row["dropoff_rate"] > 15 else "LOW",
            })

        # Sort by drop-off rate descending
        diagnoses.sort(key=lambda x: x["dropoff_rate"], reverse=True)
        return diagnoses

    def _llm_diagnose(self, row, avg_dropoff):
              """Use GPT-4 to generate contextual diagnosis and recommendations."""
              prompt = f"""You are an expert SaaS product manager specializing in onboarding optimization.

      Analyze this funnel step:
      - Step Name: {row['step']}
      - Drop-off Rate: {row['dropoff_rate']:.1f}% (funnel average: {avg_dropoff:.1f}%)
      - Severity Ratio: {row['dropoff_rate']/max(avg_dropoff,1):.1f}x average

      Provide:
      1. DIAGNOSIS (2-3 sentences): Root cause of this drop-off. Be specific about the UX/product failure.
      2. PRIMARY RECOMMENDATION (2-3 sentences): The highest-leverage fix. Be concrete and actionable.
      3. ALTERNATIVE (1-2 sentences): A backup approach if the primary fix isn't feasible.

      Format your response as:
      DIAGNOSIS: [text]
      RECOMMENDATION: [text]
      ALTERNATIVE: [text]"""

        try:
                      response = self.client.chat.completions.create(
                                        model="gpt-4",
                                        messages=[{"role": "user", "content": prompt}],
                                        max_tokens=400,
                                        temperature=0.7
                      )
                      content = response.choices[0].message.content
                      lines = content.strip().split("\n")
                      diagnosis = next((l.replace("DIAGNOSIS:", "").strip() for l in lines if l.startswith("DIAGNOSIS:")), "Analysis in progress.")
                      rec = next((l.replace("RECOMMENDATION:", "").strip() for l in lines if l.startswith("RECOMMENDATION:")), "Simplify this step.")
                      alt = next((l.replace("ALTERNATIVE:", "").strip() for l in lines if l.startswith("ALTERNATIVE:")), "Make this step optional.")
                      return diagnosis, rec, alt
except Exception as e:
              template = DIAGNOSIS_TEMPLATES[_classify_dropoff(row["step"], row["dropoff_rate"], avg_dropoff)]
              return template["diagnosis_template"], template["rec_template"], template["alt_template"]
