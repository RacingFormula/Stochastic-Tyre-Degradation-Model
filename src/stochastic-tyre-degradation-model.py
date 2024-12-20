import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class StochasticTyreDegradationModel:
    def __init__(self, config):
        self.tyre_compound = config.get("tyre_compound", "soft")
        self.base_degradation_rate = config.get("base_degradation_rate", 0.005)  # percentage per lap
        self.variation_range = config.get("variation_range", 0.002)  # max random variation
        self.race_distance = config.get("race_distance", 50)  # laps
        self.track_temperature = config.get("track_temperature", 25)  # degrees Celsius
        self.iterations = config.get("iterations", 10000)
        self.temperature_factor = config.get("temperature_factor", 0.0002)  # degradation rate per °C
        self.force_variation_range = config.get("force_variation_range", 1000)  # Newtons
        self.lateral_force = config.get("lateral_force", 4000)  # Base lateral force in Newtons

    def simulate_degradation(self):
        results = []

        for _ in range(self.iterations):
            lap_data = []
            remaining_tyre = 100  # starting percentage

            for lap in range(1, self.race_distance + 1):
                # Randomised forces for each lap
                lateral_force = np.random.uniform(self.lateral_force - self.force_variation_range, 
                                                   self.lateral_force + self.force_variation_range)

                # Calculate temperature effect on degradation
                temp_adjustment = (self.track_temperature - 25) * self.temperature_factor

                # Stochastic degradation calculation
                random_variation = np.random.uniform(-self.variation_range, self.variation_range)
                actual_degradation = self.base_degradation_rate + temp_adjustment + random_variation

                # Include lateral force impact
                force_impact = (lateral_force / 10000) * actual_degradation
                actual_degradation += force_impact

                # Update tyre percentage
                remaining_tyre -= actual_degradation * 100
                remaining_tyre = max(0, remaining_tyre)  # avoid negative values

                lap_data.append({
                    "lap": lap,
                    "remaining_tyre": remaining_tyre,
                    "degradation_rate": actual_degradation * 100,
                    "lateral_force": lateral_force
                })

            results.append(lap_data)

        return results

    def analyse_results(self, simulation_data):
        average_tyre_wear = []
        degradation_distribution = []

        for lap in range(self.race_distance):
            lap_wear = [run[lap]["remaining_tyre"] for run in simulation_data]
            lap_degradation = [run[lap]["degradation_rate"] for run in simulation_data]

            average_tyre_wear.append(np.mean(lap_wear))
            degradation_distribution.append(np.mean(lap_degradation))

        return average_tyre_wear, degradation_distribution

    def plot_results(self, average_tyre_wear, degradation_distribution):
        plt.figure(figsize=(12, 6))

        # Plot remaining tyre wear
        plt.subplot(2, 1, 1)
        plt.plot(range(1, self.race_distance + 1), average_tyre_wear, label="Average Tyre Wear", color="blue")
        plt.xlabel("Lap")
        plt.ylabel("Remaining Tyre (%)")
        plt.title("Average Tyre Wear Over Race Distance")
        plt.legend()
        plt.grid(True)

        # Plot degradation distribution
        plt.subplot(2, 1, 2)
        plt.plot(range(1, self.race_distance + 1), degradation_distribution, label="Degradation Rate (per lap)", color="red")
        plt.xlabel("Lap")
        plt.ylabel("Degradation Rate (%)")
        plt.title("Degradation Distribution Over Race Distance")
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    config = {
        "tyre_compound": "soft",
        "base_degradation_rate": 0.005,
        "variation_range": 0.002,
        "race_distance": 50,
        "track_temperature": 30,
        "iterations": 10000,
        "temperature_factor": 0.0002,
        "lateral_force": 4000,
        "force_variation_range": 1000
    }

    model = StochasticTyreDegradationModel(config)
    simulation_data = model.simulate_degradation()
    average_tyre_wear, degradation_distribution = model.analyse_results(simulation_data)

    print("Average Tyre Wear Over Laps:")
    print(average_tyre_wear)

    model.plot_results(average_tyre_wear, degradation_distribution)