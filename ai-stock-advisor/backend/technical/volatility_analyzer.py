from technical.indicators.atr import ATRIndicator
from technical.indicators.adx import ADXIndicator
from technical.indicators.bollinger import BollingerBandsIndicator


class VolatilityAnalyzer:
    """
    Evaluates market volatility using
    ATR, ADX and Bollinger Bands.
    """

    def __init__(self):

        self.atr = ATRIndicator()

        self.adx = ADXIndicator()

        self.bb = BollingerBandsIndicator()

    def analyze(self, mapped):

        atr = self.atr.latest_value(mapped)

        adx = self.adx.latest_value(mapped)

        bb = self.bb.latest_value(mapped)

        score = 0

        # ATR
        if atr["value"] is not None and atr["value"] > 0:
            score += 1

        # ADX
        if adx["strength"] in [
            "Strong",
            "Very Strong",
            "Extremely Strong",
        ]:
            score += 1

        # Bollinger Bands
        if bb["signal"] == "Neutral":
            score += 1

        if score == 3:

            volatility = "Healthy"

        elif score == 2:

            volatility = "Moderate"

        elif score == 1:

            volatility = "High"

        else:

            volatility = "Extreme"

        confidence = round(
            (score / 3) * 100,
            2,
        )

        return {

            "volatility": volatility,

            "score": score,

            "max_score": 3,

            "confidence": confidence,

            "atr": atr,

            "adx": adx,

            "bollinger": bb,
        }