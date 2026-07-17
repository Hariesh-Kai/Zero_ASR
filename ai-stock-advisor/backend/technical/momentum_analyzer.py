from technical.indicators.rsi import RSIIndicator
from technical.indicators.stochastic import StochasticIndicator
from technical.indicators.cci import CCIIndicator
from technical.indicators.williams_r import WilliamsRIndicator


class MomentumAnalyzer:
    """
    Evaluates market momentum using
    RSI, Stochastic, CCI and Williams %R.
    """

    def __init__(self):

        self.rsi = RSIIndicator()

        self.stochastic = StochasticIndicator()

        self.cci = CCIIndicator()

        self.williams = WilliamsRIndicator()

    def analyze(self, mapped):

        rsi = self.rsi.latest_value(mapped)

        stochastic = self.stochastic.latest_value(mapped)

        cci = self.cci.latest_value(mapped)

        williams = self.williams.latest_value(mapped)

        score = 0

        # RSI
        if 40 <= rsi["value"] <= 70:
            score += 1

        # Stochastic
        if 20 <= stochastic["%K"] <= 80:
            score += 1

        # CCI
        if -100 <= cci["value"] <= 100:
            score += 1

        # Williams %R
        if -80 <= williams["value"] <= -20:
            score += 1

        if score == 4:

            momentum = "Strong"

        elif score == 3:

            momentum = "Positive"

        elif score == 2:

            momentum = "Neutral"

        elif score == 1:

            momentum = "Weak"

        else:

            momentum = "Very Weak"

        confidence = round(
            (score / 4) * 100,
            2,
        )

        return {

            "momentum": momentum,

            "score": score,

            "max_score": 4,

            "confidence": confidence,

            "rsi": rsi,

            "stochastic": stochastic,

            "cci": cci,

            "williams_r": williams,
        }