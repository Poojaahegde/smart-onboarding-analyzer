"""
ImpactSimulator: Monte Carlo simulation of activation improvement scenarios.
Models conservative / realistic / optimistic outcomes for applying onboarding fixes.
"""

import numpy as np
import pandas as pd


class ImpactSimulator:
      def __init__(self, monthly_signups: int = 10000, avg_ltv: float = 50.0, n_simulations: int = 1000):
                self.monthly_signups = monthly_signups
                self.avg_ltv = avg_ltv
                self.n_simulations = n_simulations

      def simulate(self, funnel_df: pd.DataFrame, diagnoses: list) -> dict:
                """
                        Run Monte Carlo simulation for the top N fixes.
                                Returns conservative, realistic, and optimistic outcomes.
                                        """
                baseline_activation = funnel_df["users"].iloc[-1] / funnel_df["users"].iloc[0]
                total_users = funnel_df["users"].iloc[0]

          # Simulate improvement distributions for each fix
                simulated_improvements = []
                for diagnosis in diagnoses:
                              base_improvement = diagnosis.get("expected_improvement", 5.0)
                              # Model uncertainty: actual improvement follows a distribution around expected
                              severity_multiplier = {"HIGH": 1.2, "MEDIUM": 1.0, "LOW": 0.8}.get(diagnosis.get("severity", "MEDIUM"), 1.0)
                              std_dev = base_improvement * 0.35 * severity_multiplier
                              samples = np.random.normal(base_improvement, std_dev, self.n_simulations)
                              samples = np.clip(samples, 0, diagnosis["dropoff_rate"] * 0.8)
                              simulated_improvements.append(samples)

                # Total improvement per simulation run (sum of fixes, with diminishing returns)
                if simulated_improvements:
                              total_improvements = np.zeros(self.n_simulations)
                              for i, improvement in enumerate(simulated_improvements):
                                                diminishing_factor = 0.9 ** i  # Each subsequent fix has slightly less impact
                total_improvements += improvement * diminishing_factor

              # Convert percentage point improvements in drop-off to activation rate improvement
                    activation_improvements = total_improvements / 100  # pp drop-off reduction -> activation gain

            # Scenario percentiles
                    conservative_improvement = np.percentile(activation_improvements, 25)
                    realistic_improvement = np.percentile(activation_improvements, 50)
                    optimistic_improvement = np.percentile(activation_improvements, 75)
else:
            conservative_improvement = realistic_improvement = optimistic_improvement = 0.0

        def calc_arr(activation_delta):
                      new_activation_rate = min(baseline_activation + activation_delta, 1.0)
                      additional_activations_per_month = (new_activation_rate - baseline_activation) * self.monthly_signups
                      return additional_activations_per_month * self.avg_ltv * 12  # Annual

        return {
                      "baseline_activation": baseline_activation * 100,
                      "conservative_activation": conservative_improvement * 100,
                      "realistic_activation": realistic_improvement * 100,
                      "optimistic_activation": optimistic_improvement * 100,
                      "conservative_arr": calc_arr(conservative_improvement),
                      "realistic_arr": calc_arr(realistic_improvement),
                      "optimistic_arr": calc_arr(optimistic_improvement),
                      "n_simulations": self.n_simulations,
        }
