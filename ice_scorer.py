"""
ICEScorer: Prioritizes onboarding fixes using the ICE framework.
ICE = Impact x Confidence x Ease (each scored 1-10)
"""


# Scoring parameters per diagnosis category
ICE_PARAMS = {
      "Value Gap": {"impact": 9, "confidence": 8, "ease": 5},
      "Cognitive Load": {"impact": 7, "confidence": 9, "ease": 8},
      "Friction": {"impact": 6, "confidence": 8, "ease": 8},
      "Trust Gap": {"impact": 7, "confidence": 6, "ease": 6},
      "Motivation Drop": {"impact": 5, "confidence": 7, "ease": 7},
}

FIX_DESCRIPTIONS = {
      "Value Gap": "Show value preview before requiring this step; or make step optional",
      "Cognitive Load": "Reduce to single action per screen; remove optional fields",
      "Friction": "Simplify inputs, add autofill, break into micro-steps",
      "Trust Gap": "Add social proof and clear data usage explanation before this step",
      "Motivation Drop": "Add quick win before this step; show progress bar",
}


class ICEScorer:
      def score(self, diagnoses: list) -> list:
                """
                        Score each diagnosis using ICE framework.
                                Adjusts base scores by severity and drop-off magnitude.
                                        Returns sorted list of prioritized fixes.
                                                """
                results = []
                for diagnosis in diagnoses:
                              category = diagnosis.get("category", "Friction")
                              params = ICE_PARAMS.get(category, {"impact": 5, "confidence": 5, "ease": 5})

                    # Adjust impact score based on severity and drop-off rate
                              dropoff = diagnosis.get("dropoff_rate", 10)
                              severity_bonus = 2 if dropoff > 30 else 1 if dropoff > 15 else 0
                              impact = min(10, params["impact"] + severity_bonus)

                    confidence = params["confidence"]
                    ease = params["ease"]
                    ice_score = impact * confidence * ease

              results.append({
                                "step": diagnosis["step"],
                                "category": category,
                                "fix": FIX_DESCRIPTIONS.get(category, "Simplify this step"),
                                "impact": impact,
                                "confidence": confidence,
                                "ease": ease,
                                "ice_score": ice_score,
                                "dropoff_rate": dropoff,
                                "severity": diagnosis.get("severity", "MEDIUM"),
              })

        # Sort by ICE score descending, add priority ranking
        results.sort(key=lambda x: x["ice_score"], reverse=True)
        for i, r in enumerate(results):
                      r["priority"] = i + 1

        return results
