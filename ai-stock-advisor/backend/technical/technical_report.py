from datetime import datetime
from typing import Dict, Any


class TechnicalReport:
    """
    Builds the final Technical Analysis report.
    Standardized format shared across all engines.
    """

    @staticmethod
    def build(
        ticker: str,
        analysis: Dict[str, Any],
        scores: Dict[str, Any],
        recommendation: Dict[str, Any],
    ):

        return {

            # -------------------------------------------------
            # Engine Metadata
            # -------------------------------------------------

            "engine": "Technical",

            "version": "1.0",

            "generated_at": datetime.utcnow().isoformat(),

            "ticker": ticker,

            # -------------------------------------------------
            # Technical Analysis
            # -------------------------------------------------

            "analysis": {

                "trend": analysis.get("trend"),

                "momentum": analysis.get("momentum"),

                "volume": analysis.get("volume"),

                "volatility": analysis.get("volatility"),

            },

            # -------------------------------------------------
            # Scores
            # -------------------------------------------------

            "scores": scores,

            # -------------------------------------------------
            # Recommendation
            # -------------------------------------------------

            "recommendation": recommendation,

        }