from typing import List, Dict


class PredictionAggregator:

    def __init__(self):
        pass

    # ============================================================
    # SIMPLE AVERAGE
    # ============================================================

    def average(self, predictions: List[Dict]) -> float:

        if not predictions:
            raise ValueError(
                "No predictions available for aggregation."
            )

        probabilities = []

        for item in predictions:

            probability = float(
                item["probability"]
            )

            probability = max(
                0.0,
                min(1.0, probability)
            )

            probabilities.append(probability)

        return sum(probabilities) / len(probabilities)

    # ============================================================
    # WEIGHTED AVERAGE
    # ============================================================

    def weighted_average(
        self,
        predictions: List[Dict]
    ) -> float:

        if not predictions:
            raise ValueError(
                "No predictions available for aggregation."
            )

        weighted_sum = 0.0
        total_weight = 0.0

        for item in predictions:

            probability = float(
                item["probability"]
            )

            weight = float(
                item.get("weight", 1.0)
            )

            probability = max(
                0.0,
                min(1.0, probability)
            )

            if weight < 0:
                weight = 0.0

            weighted_sum += (
                probability * weight
            )

            total_weight += weight

        if total_weight == 0:

            raise ValueError(
                "Total aggregation weight cannot be zero."
            )

        return weighted_sum / total_weight

    # ============================================================
    # CLASSIFICATION
    # ============================================================

    def classify(
        self,
        probability: float,
        threshold: float = 0.5
    ) -> str:

        if probability >= threshold:
            return "HIGH RISK"

        return "LOW RISK"

    # ============================================================
    # SUMMARY
    # ============================================================

    def summary(
        self,
        predictions: List[Dict],
        final_probability: float
    ) -> Dict:

        return {

            "participating_clients": [
                item["client"]
                for item in predictions
            ],

            "client_count": len(predictions),

            "individual_probabilities": {
                item["client"]: round(
                    float(item["probability"]),
                    6
                )
                for item in predictions
            },

            "final_probability": round(
                final_probability,
                6
            ),

            "final_percentage": round(
                final_probability * 100,
                2
            )
        }

    # ============================================================
    # USER-FACING RESULT
    # ============================================================

    def format_result(
        self,
        predictions: List[Dict],
        final_probability: float,
        risk: str,
        threshold: float = 0.5
    ) -> str:

        percentage = max(
            0.0,
            min(100.0, final_probability * 100)
        )

        bar_width = 24
        filled_width = round(
            percentage / 100 * bar_width
        )
        probability_bar = (
            "#" * filled_width
            + "-" * (bar_width - filled_width)
        )

        interpretation = (
            "The combined model result is above the "
            f"{threshold * 100:.0f}% risk threshold."
            if final_probability >= threshold
            else
            "The combined model result is below the "
            f"{threshold * 100:.0f}% risk threshold."
        )

        clients = ", ".join(
            item["client"]
            for item in predictions
        )

        def line(content: str = "") -> str:
            return f"| {content:<58} |"

        return (
            "\n"
            "+------------------------------------------------------------+\n"
            f"|{'FINAL PREDICTION RESULT':^60}|\n"
            "+------------------------------------------------------------+\n"
            + line(f"Assessment : {risk}")
            + "\n"
            + line(
                f"Probability: {percentage:>6.2f}%  "
                f"[{probability_bar}]"
            )
            + "\n"
            + line(f"Clients    : {len(predictions)}")
            + "\n"
            "+------------------------------------------------------------+\n"
            + line(interpretation)
            + "\n"
            + line(
                "This is an experimental model result, not a medical"
            )
            + "\n"
            + line(
                "diagnosis. Please consult a qualified healthcare"
            )
            + "\n"
            + line("professional for medical advice.")
            + "\n"
            "+------------------------------------------------------------+\n"
            + line(f"Participating clients: {clients}")
            + "\n"
            "+------------------------------------------------------------+"
        )